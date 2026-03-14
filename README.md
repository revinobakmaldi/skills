# skills

Claude Code skills by Revino Bakmaldi.

## Install

Add as a marketplace in Claude Code:

```
/plugin marketplace add revinobakmaldi/skills
```

Then install:

```
/plugin install minimax-research@revinobakmaldi-skills
```

---

## minimax-research

Fast parallel web research using Minimax M2.5 with real-time web search.

- Decomposes queries into 2-3 sub-queries run in parallel
- Reuses a single MCP subprocess per session
- Typical response time: 10-20s

**Requirements before installing:**
1. `pip install httpx uv`
2. Set `MINIMAX_API_KEY` as an environment variable
3. Copy the script to your local bin:
   ```bash
   cp skills/minimax-research/minimax-research.py ~/.local/bin/minimax-research
   chmod +x ~/.local/bin/minimax-research
   ```
