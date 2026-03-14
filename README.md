# Skills

Claude Code skills by Revino Bakmaldi.

## minimax-research

Fast parallel web research using Minimax M2.5 with real-time web search.

- Decomposes queries into 2-3 sub-queries run in parallel
- Reuses a single MCP subprocess per session
- Tight system prompt: max 3 searches, concise answers
- Typical response time: 10-20s

### Prerequisites

- Python 3.8+
- `pip install httpx`
- `uvx` installed (`pip install uv`)
- A [Minimax API key](https://www.minimax.io)

### Setup

1. Copy the script to your local bin and make it executable:
   ```bash
   cp minimax-research/minimax-research.py ~/.local/bin/minimax-research
   chmod +x ~/.local/bin/minimax-research
   ```

2. Set your API key — pick one of:
   ```bash
   # Option A: environment variable (add to ~/.bashrc or ~/.zshrc)
   export MINIMAX_API_KEY=your_key_here

   # Option B: .env file in one of these locations
   echo "MINIMAX_API_KEY=your_key_here" >> ~/english-coach/.env
   # or
   echo "MINIMAX_API_KEY=your_key_here" >> ~/memory-mcp/.env
   ```
   > Note: The script only auto-reads from `~/english-coach/.env` or `~/memory-mcp/.env`. To use a different path, edit the `load_api_key()` function in the script.

3. Install the Claude Code skill:
   ```bash
   mkdir -p ~/.claude/skills/minimax-research
   cp minimax-research/SKILL.md ~/.claude/skills/minimax-research/SKILL.md
   ```

4. Test it:
   ```bash
   minimax-research "latest news today"
   ```
