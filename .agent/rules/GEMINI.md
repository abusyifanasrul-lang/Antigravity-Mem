---
trigger: always_on
---

# GEMINI.md - Antigravity Memory Protocol

> This file defines the automated memory behavior for AI Agents in this workspace.

---

## 🚀 SESSION START PROTOCOL (MANDATORY)

**Every time a new session starts, the Agent MUST perform the following steps BEFORE responding:**

1. **Read `STATE_OF_THE_UNION.md`**: Understand the latest status, project focus, and key architectural decisions.
2. **Read `KNOWLEDGE_MAP.md`**: Use as a primary reference for historical context and project structure.
3. **Internalize Context**: Do not provide solutions or perform research before understanding the "State of the Union" from these files.
4. **Provide "Understanding Receipt"**: In the first response, include a brief summary of the project status to prove the files have been read. Format: `🤖 Status: [Brief summary of latest status/focus]`.

---

## 🧠 AUTOMATED MEMORY PROTOCOL (MANDATORY)

**Trigger**: Whenever the user gives a "commit and push" command (or similar variations).

**Mandatory Action**: The AI **MUST** run the memory synchronization and graphify scripts before or after the Git operation:
`python scripts/sync_knowledge.py`

This ensures that `KNOWLEDGE_MAP.md` and the **Knowledge Graph (Graphify)** are always updated with the latest architectural decisions before the code is sent to the repository.

---

## 🧹 CLEAN CODE & DOCUMENTATION

- **Documentation Integrity**: Maintain all existing comments and docstrings.
- **KNOWLEDGE_MAP.md**: Update this file only via the provided scripts to maintain structural integrity.
- **Manual Observations**: If the agent makes a significant discovery not caught by the auto-harvester, it should be manually recorded in `memory.db` using the available tools.

---

## 🛑 EXPLICIT CONTROL & TRANSPARENCY

1. **No Phantom Changes**: Do not modify files unrelated to the active task unless handling informed dependencies.
2. **Action Transparency**: Explain "Why" and "What the impact is" BEFORE executing tools that massively change the codebase.
3. **Context Recovery**: At the start of a session, only READ context. Changes should only happen after user confirmation or explicit command.

---
*Failure to follow this protocol results in loss of project context and inconsistent AI behavior.*
