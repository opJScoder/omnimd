# OmniMD ⚡

A lightning-fast, zero-config local CLI tool that automatically creates and updates project markdown documentation using local open-weight AI models.

## 🌟 Overview

OmniMD solves the most tedious part of software engineering: writing and maintaining documentation. With a single command, it recursively scans your workspace codebase, constructs a secure contextual tree map, and automatically generates required open-source markdown assets like `README.md` and `skills.md`. 

If documentation already exists, OmniMD introduces a revolutionary **Smart Sync** loop engine to merge new module architecture context without overwriting custom human developer text.

## 🎨 Core Features

*   **Zero Cloud Dependencies:** Operates 100% locally on your machine. Your enterprise intellectual property and source files never touch an external internet connection.
*   **Flash-Speed Local Execution:** Optimized directory-walking token parsers keep data blocks small, allowing lightweight models to render outputs seamlessly on standard developer laptops.
*   **Interactive System Prompting:** Built using high-fidelity terminal components featuring step-by-step progress spinners and beautiful menu checklist interfaces.
*   **Smart Revision Memory System:** Detects structural drift across code modules and updates modified dependency blocks while preserving your unique manually-written documentation.

## 🛠️ Tech Stack & Architecture

*   **Language Runtime:** Python 3
*   **Local AI Orchestration Engine:** Ollama Framework
*   **Target Open-Weight Foundation Model:** `Qwen2.5-Coder (1.5B)`
*   **Visual Interface Layout & Styling:** Rich Component Framework
*   **Interactive Prompter System Terminal:** Questionary SDK
*   **Version Control Hook Engine:** Git & GitHub integrations

## 🚀 Installation & Setup

1. **Verify Local Pre-requisites:** Ensure the Ollama background engine service is active on your host system:
   ```bash
   ollama --version
   ```

2. **Pull the Coding Model Binaries:** Run the ultra-fast lightweight code weight partition layer:
   ```bash
   ollama pull qwen2.5-coder:1.5b
   ```

3. **Install Environment Package Dependencies:**
   ```bash
   pip install rich questionary ollama
   ```

## 💻 Usage

To execute document generation, drop the script file into your target workspace project folder and run:
```bash
python omnimd.py
```

### Flow Sequences:
*   **Fresh Run:** Automatically generates professional-grade, structured `README.md` and Hacktoberfest layout `skills.md` files from scratch.
*   **Incremental Run:** If old versions are found, it triggers an interactive picker prompt choice to launch **Smart Sync** or wipe-overwrite clean.

## ⚖️ License

Distributed completely under the **MIT License**. Check the enclosed `LICENSE` document file for details.
