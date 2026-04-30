# 🤖 Antigravity Memory Protocol

> [!NOTE]
> Bahasa Indonesia? Baca [README_ID.md](./README_ID.md)

**Antigravity Memory Protocol** is an automated knowledge management system designed for AI Coding Agents (such as Google Deepmind Antigravity). It enables AI to maintain a "long-term memory" of architectural decisions, code changes, and project evolution directly within your repository.

## 🌟 Key Features
- **Automated Harvesting**: Automatically records function and logic changes every time you commit.
- **Universal Language Support**: Supports multiple programming languages (Python, JS/TS, Go, Rust, PHP, etc.).
- **Initial Discovery Scan**: Capable of "ingesting" data from existing projects to build instant knowledge context.
- **Graphify Integration**: Builds a *Knowledge Graph* to link relationships between files and architectural decisions (ADR).
- **Self-Healing Documentation**: Automatically keeps `KNOWLEDGE_MAP.md` and `STATE_OF_THE_UNION.md` up-to-date.

## 🚀 Quick Start

1. **Copy Files**: Copy all files from this package to your project's root directory.
2. **Run Installer**: Open a terminal in the root directory and run:
   ```bash
   python setup.py
   ```
3. **Follow Prompts**: 
   - The installer will automatically set up structure and dependencies.
   - Choose **"Y"** if you want to perform an *Initial Scan* on an existing project.

## 📁 Folder Structure
```plaintext
your-project/
├── .agent/
│   ├── rules/
│   │   └── GEMINI.md          # AI Agent protocol rules
│   └── scripts/
│       └── antigravity_mem/   # Core engine (Harvester, Backfill, etc.)
├── scripts/
│   └── sync_knowledge.py      # Main Orchestrator
└── setup.py                   # Auto-installer
```

## 🛠️ Daily Usage

### 1. Agent Activation
When starting a new session with an AI Agent, give the following instruction:
> "Activate **Automated Memory Protocol** as per `.agent/rules/GEMINI.md`."

### 2. Automated Sync
The system is designed to run after every commit. You can tell the AI:
> "Commit and push these changes, then run memory synchronization."

Or run it manually:
```bash
python scripts/sync_knowledge.py
```

## 📝 Important Notes
- **Graphify**: Requires an internet connection during the first installation to pull the package from GitHub.
- **SQLite3**: All data is stored locally in `.agent/memory.db`. Your data remains yours.

---
*Created with ❤️ by Antigravity AI for the Global Developer Community.*
