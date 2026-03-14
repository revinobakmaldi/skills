# Skills

Claude Code skills by Revino Bakmaldi.

## minimax-research

Fast parallel web research using Minimax M2.5 with real-time web search.

- Decomposes queries into 2-3 sub-queries run in parallel
- Reuses a single MCP subprocess per session
- Tight system prompt: max 3 searches, concise answers
- Typical response time: 10-20s

### Setup

1. Copy `minimax-research/minimax-research.py` to `~/.local/bin/minimax-research`
2. Make executable: `chmod +x ~/.local/bin/minimax-research`
3. Set `MINIMAX_API_KEY` in your environment or `.env` file
4. Copy `minimax-research/SKILL.md` to `~/.claude/skills/minimax-research/SKILL.md`
