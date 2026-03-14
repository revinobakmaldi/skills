#!/usr/bin/env python3
"""
Delegates web research to Minimax M2.5 agent.
Optimized: single MCP subprocess reused per session, parallel tool calls,
tight system prompt for fast concise answers.
"""

import sys
import os
import json
import asyncio
from pathlib import Path

import httpx


def load_api_key() -> str:
    if key := os.environ.get("MINIMAX_API_KEY"):
        return key
    for f in [Path.home() / "english-coach/.env", Path.home() / "memory-mcp/.env"]:
        if f.exists():
            for line in f.read_text().splitlines():
                if line.startswith("MINIMAX_API_KEY="):
                    return line.split("=", 1)[1].strip()
    raise RuntimeError("MINIMAX_API_KEY not found")


API_KEY = load_api_key()
HOST = "https://api.minimax.io"
MODEL = "MiniMax-M2.5"

SYSTEM_PROMPT = (
    "You are a fast web research assistant. "
    "Do at most 3 web searches total. "
    "Prioritize speed: if 1-2 searches are enough, stop. "
    "Answer concisely — use bullet points or a short paragraph. "
    "No long preambles, no repeated disclaimers, no padding. "
    "Include sources inline (site name + brief URL) only if highly relevant."
)

TOOLS = [
    {
        "name": "web_search",
        "description": (
            "Search the web for real-time or current information. "
            "Use this whenever the query requires up-to-date facts, versions, news, or data."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "3-5 keyword search query"}
            },
            "required": ["query"],
        },
    },
    {
        "name": "understand_image",
        "description": "Analyze or describe an image from a URL or local file path.",
        "input_schema": {
            "type": "object",
            "properties": {
                "prompt": {"type": "string"},
                "image_source": {"type": "string"},
            },
            "required": ["prompt", "image_source"],
        },
    },
]


def call_minimax(messages: list) -> dict:
    resp = httpx.post(
        f"{HOST}/anthropic/v1/messages",
        headers={
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 2048,
            "system": SYSTEM_PROMPT,
            "tools": TOOLS,
            "messages": messages,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()


class MCPSession:
    """A single reusable MCP subprocess for the duration of one research session."""

    def __init__(self):
        self.proc = None
        self._lock = asyncio.Lock()
        self._msg_id = 10

    async def start(self):
        env = {**os.environ, "MINIMAX_API_KEY": API_KEY, "MINIMAX_API_HOST": HOST}
        self.proc = await asyncio.create_subprocess_exec(
            "uvx", "minimax-coding-plan-mcp", "-y",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.DEVNULL,
            env=env,
        )
        await self._send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                          "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                                     "clientInfo": {"name": "minimax-research", "version": "2.0"}}})
        await self._recv()
        await self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})

    async def _send(self, msg: dict):
        self.proc.stdin.write((json.dumps(msg) + "\n").encode())
        await self.proc.stdin.drain()

    async def _recv(self) -> dict:
        return json.loads(await self.proc.stdout.readline())

    async def call_tool(self, tool_name: str, tool_input: dict) -> str:
        async with self._lock:  # serialize MCP calls (single stdin/stdout)
            self._msg_id += 1
            await self._send({"jsonrpc": "2.0", "id": self._msg_id,
                               "method": "tools/call",
                               "params": {"name": tool_name, "arguments": tool_input}})
            result = await self._recv()

        if "result" in result:
            return "\n".join(
                c.get("text", "") for c in result["result"].get("content", [])
                if c.get("type") == "text"
            )
        return f"MCP error: {result.get('error', 'unknown')}"

    async def close(self):
        if self.proc:
            self.proc.stdin.close()
            await self.proc.wait()


async def research(query: str) -> str:
    session = MCPSession()
    await session.start()

    try:
        messages = [{"role": "user", "content": query}]

        for _ in range(6):  # max 6 rounds (was 15)
            response = call_minimax(messages)

            if "error" in response:
                return f"Minimax API error: {response['error']}"

            content = response.get("content", [])
            stop_reason = response.get("stop_reason", "")
            tool_uses = [b for b in content if b.get("type") == "tool_use"]

            if stop_reason == "end_turn" and not tool_uses:
                return "\n".join(b.get("text", "") for b in content if b.get("type") == "text").strip()

            if not tool_uses:
                return "\n".join(b.get("text", "") for b in content if b.get("type") == "text").strip()

            messages.append({"role": "assistant", "content": content})

            # Run all tool calls in parallel
            results = await asyncio.gather(*[
                session.call_tool(tu["name"], tu.get("input", {}))
                for tu in tool_uses
            ])

            tool_results = [
                {"type": "tool_result", "tool_use_id": tu["id"], "content": res}
                for tu, res in zip(tool_uses, results)
            ]
            messages.append({"role": "user", "content": tool_results})

        return "Max iterations reached without a final answer."
    finally:
        await session.close()


def main():
    query = " ".join(sys.argv[1:]).strip() if len(sys.argv) > 1 else sys.stdin.read().strip()
    if not query:
        print("Usage: minimax-research <query>", file=sys.stderr)
        sys.exit(1)
    print(asyncio.run(research(query)))


if __name__ == "__main__":
    main()
