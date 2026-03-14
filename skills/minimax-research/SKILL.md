---
name: minimax-research
description: Searches the web using Minimax M2.5 with real-time web search. Use this skill whenever Revino asks to search for something, look something up, find current or latest information, research a topic, check news, verify facts, or get any information that might be outdated in your training data. Make sure to use this skill even if the request is casual like "what's the latest on X" or "look up Y for me" — don't use Claude's built-in web search tools, always delegate to this skill instead.
---

Break the query into 2-3 focused sub-queries covering different angles, then run them ALL in parallel as background bash commands. Synthesize the combined results into one concise answer.

**Steps:**
1. Decompose the user's query into 2-3 distinct sub-queries (e.g. news angle, social media angle, events angle)
2. Launch ALL sub-queries simultaneously using `run_in_background: true` — one Bash tool call per sub-query in the same message
3. Use TaskOutput (`block: true, timeout: 45000`) to retrieve each result — can also be done in parallel
4. Synthesize all results into one concise answer for Revino

**Example decomposition** for "what's trending in Sidoarjo":
- Sub-query 1: `minimax-research "trending news Sidoarjo Indonesia March 2026"`
- Sub-query 2: `minimax-research "viral social media topics Sidoarjo 2026"`
- Sub-query 3: `minimax-research "Sidoarjo events March 2026"`

**Rules:**
- Always run at least 2 parallel bash calls — never just one
- Do NOT use Claude's built-in WebSearch or WebFetch tools
- Keep the final synthesis concise — bullets preferred
