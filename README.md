# skills

Claude Code skills by Revino Bakmaldi.

## Install

In Claude Code, run `/plugin` and enter:

```
https://github.com/revinobakmaldi/skills.git
```

## Skills

### minimax-research

Fast parallel web research using Minimax M2.5 with real-time web search.

- Decomposes queries into 2-3 sub-queries run in parallel
- Reuses a single MCP subprocess per session
- Typical response time: 10-20s

**Requirements:**
- `pip install httpx`
- `uvx` available (`pip install uv`)
- `MINIMAX_API_KEY` set as an environment variable
- The `minimax-research` script installed to `~/.local/bin/`:
  ```bash
  cp skills/minimax-research/minimax-research.py ~/.local/bin/minimax-research
  chmod +x ~/.local/bin/minimax-research
  ```
