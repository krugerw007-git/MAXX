# MAXX - AI-Orchestrated Unity Game Development Project

[![Project Status](https://img.shields.io/badge/Status-INITIALIZATION-yellow)]()
[![Unity Version](https://img.shields.io/badge/Unity-2022.3%20LTS-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()
[![Docs](https://img.shields.io/badge/Docs-Live-brightgreen)]()

> **MAXX** is a from-scratch Unity game development project architected as an **AI-orchestrated, multi-agent platform**. Multiple AI agents (Claude Code, Codex, Minimax, Meshy) collaborate via MCP with persistent memory (Agent Brain), version-controlled via GitHub, containerized via Docker, with 3D asset generation via Meshy AI.

---

## 🎯 Project Vision

Build a **complete game development pipeline** where AI agents autonomously handle:
- **Architecture & Planning** (Claude Code - Primary Orchestrator)
- **Implementation & Testing** (Codex CLI - Code Execution Specialist)
- **3D Asset Generation** (Meshy AI - Text/Image/Video → 3D)
- **Video/Audio Generation** (Minimax AI - Cutscenes, Music, Voice)
- **Persistent Memory & Coordination** (Agent Brain - Cross-session memory, checkpoints, mailbox)

---

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR (Claude Code)                    │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────────┐   │
│  │Agent Brain│ │ MCP Hub  │ │ GitHub   │ │ Docker (Local)   │   │
│  │(Memory)  │◄─│ (MCP Hub)│◄─│(krugerw007)│ │(Containers)     │   │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────────┬─────────┘   │
│       │            │            │                 │             │
│  ┌────▼────────────▼────────────▼─────────────────▼──────┐     │
│  │              SUB-AGENT ORCHESTRATION                   │     │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────────────┐  │     │
│  │  │ CLAUDE │ │ CODEX  │ │MINIMAX │ │   MESHY AI     │  │     │
│  │  │  CODE  │ │ (CLI)  │ │ (API)  │ │  (3D Gen API)  │  │     │
│  │  │ (MCP)  │ │        │ │        │ │  (3D Assets)   │  │     │
│  │  └────────┘ └────────┘ └────────┘ └────────────────┘  │     │
│  └────────────────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│                      UNITY PROJECT (MAXX)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌───────┐ │
│  │ Assets/  │ │ Code/    │ │ Assets/  │ │ Docs/    │ │Tools/ │ │
│  │ Scripts  │ │ (C#)     │ │ 3D/2D    │ │ (Live)   │ │(Auto) │ │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └───────┘ │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Agent Roles

| Agent | Role | Access | Memory | Checkpoints |
|-------|------|--------|--------|-------------|
| **Claude Code** | Primary Orchestrator | Full MCP (Agent Brain, GitHub, Docker, FS) | Agent Brain (native) | Mandatory via MCP |
| **Codex CLI** | Code Execution Specialist | Local FS, GitHub CLI, Docker CLI, Agent Brain (curl) | Agent Brain (curl fallback) | Via `ab-checkpoint` wrapper |
| **Meshy AI** | 3D Asset Generation | Meshy REST API, Agent Brain (curl) | Agent Brain (curl) | Via orchestrator |
| **Minimax AI** | Video/Audio Generation | Minimax REST API, Agent Brain (curl) | Agent Brain (curl) | Via orchestrator |

---

## 📁 Project Structure

```
MAXX/
├── .github/              # GitHub Actions, workflows
├── .vscode/              # VS Code workspace
├── .devcontainer/        # DevContainer for consistent env
├── .opencode/            # OpenCode configuration
├── .agent-brain/         # Agent Brain local config
├── docs/                 # 📚 DOCUMENTATION (Source of Truth)
│   ├── architecture/
│   ├── planning/         # Roadmap, sprints, tasks, research
│   ├── api/              # API documentation
│   ├── development/      # Standards, workflows
│   ├── agents/           # Agent specifications
│   ├── infrastructure/   # Docker, K8s, Terraform
│   ├── project/          # Charter, manifest, decisions
│   └── runtime/          # Session logs, checkpoints, daily logs
├── src/                  # 🎮 UNITY SOURCE (C#)
│   └── Assets/
├── tools/                # 🔧 AUTOMATION (Python/PS/Bash)
│   ├── python/
│   ├── powershell/
│   └── bash/
├── infrastructure/       # 🐳 INFRASTRUCTURE
│   ├── docker/
│   ├── kubernetes/
│   └── terraform/
├── assets/               # 🎨 GAME ASSETS
│   ├── 3d/
│   ├── 2d/
│   ├── audio/
│   └── video/
├── tests/                # 🧪 TESTS
├── scripts/              # 📜 ENTRY POINT SCRIPTS
├── config/               # ⚙️ CONFIGURATION
├── logs/                 # 📋 RUNTIME LOGS
└── PROJECT_MANIFEST.md   # 📋 MASTER MANIFEST
```

---

## 📋 Current Status (Live)

| Area | Status | Progress | Last Updated |
|------|--------|----------|--------------|
| **Project Manifest** | ✅ Complete | 100% | 2026-07-16 |
| **Directory Structure** | ✅ Complete | 100% | 2026-07-16 |
| **GitHub Repository** | 🔄 In Progress | 0% | - |
| **Agent Brain Integration** | 📋 Planned | 0% | - |
| **MCP Setup (Claude Code)** | 📋 Planned | 0% | - |
| **Codex Integration** | 📋 Planned | 0% | - |
| **Docker Infrastructure** | 📋 Planned | 0% | - |
| **Unity Project Init** | 📋 Planned | 0% | - |
| **Research Phase** | 🔬 Starting | 0% | 2026-07-16 |

---

## 🚀 Quick Start

### Prerequisites
- **Docker Desktop** (latest)
- **Python 3.11+** with `uv` or `pip`
- **Node.js 20+** (for any tooling)
- **Unity 2022.3 LTS** (or 6000.x LTS)
- **Agent Brain** running on `localhost:3030`
- **GitHub CLI** (`gh`) authenticated

### Environment Setup
```bash
# 1. Clone repository
git clone https://github.com/krugerw007-git/MAXX.git
cd MAXX

# 2. Copy environment template
cp .env.example .env
# Edit .env with your API keys

# 3. Start infrastructure
docker-compose up -d agent-brain

# 4. Verify Agent Brain
curl http://localhost:3030/health

# 5. Install Python tools
cd tools/python
pip install -e ".[dev]"

# 6. Run development environment
docker-compose --profile agents --profile workers up -d
```

### Agent Brain Project Key
```
Project Key: -Users-WERNER-My Drive (krugerw007-gmail-com)-GAMEDEV-MAXX
```

---

## 📊 Task Management

### Sprint 001: Project Initialization & Infrastructure
| ID | Task | Status | Owner |
|----|------|--------|-------|
| T001 | Create PROJECT_MANIFEST.md | ✅ Done | Claude |
| T002 | Initialize GitHub repo | 🔄 In Progress | Codex |
| T003 | Setup GitHub Actions CI/CD | 📋 Planned | Codex |
| T004 | Setup Docker infrastructure | 📋 Planned | Codex |
| T005 | Setup Agent Brain integration | 📋 Planned | Claude |
| T006 | Setup Meshy AI integration | 📋 Planned | Meshy |
| T007 | Setup Minimax API integration | 📋 Planned | Minimax |
| T008 | Setup Agent Brain MCP for Claude | 📋 Planned | Claude |
| T009 | Setup Codex Agent Brain (curl) | 📋 Planned | Codex |
| T010 | Create project directory structure | ✅ Done | Claude |

> **Full Task Index**: [`docs/planning/TASKS_INDEX.md`](docs/planning/TASKS_INDEX.md)

---

## 🔬 Research Phase

All implementation tasks require **completed research** first:

| Research Doc | Status | Owner |
|--------------|--------|-------|
| AI Orchestration Patterns | 🔬 Starting | Claude |
| MCP Integration Patterns | 📋 Planned | Claude |
| Unity Architecture Patterns | 📋 Planned | Unity |
| Meshy AI Integration | 📋 Planned | Meshy |
| Agent Brain Integration | 📋 Planned | Claude |
| Docker Orchestration | 📋 Planned | Codex |
| GitHub Workflow Standards | 📋 Planned | Codex |
| Unity C# Standards | 📋 Planned | Unity |

> **Research Index**: [`docs/planning/RESEARCH/RESEARCH_INDEX.md`](docs/planning/RESEARCH/RESEARCH_INDEX.md)

---

## 🛠️ Development Standards

### Quality Gates (ALL MUST PASS)
| Gate | Tool | Threshold |
|------|------|-----------|
| C# Compilation | `dotnet build` | 0 errors, 0 warnings |
| C# Style | `dotnet format` / `csharpier` | 0 violations |
| C# Analysis | `Roslynator` / SonarCloud | 0 critical, 0 major |
| Unit Tests | `dotnet test` | 100% pass, ≥80% coverage |
| Python Lint | `ruff` | 0 errors |
| Python Types | `mypy` | 0 errors |
| Python Tests | `pytest` | 100% pass, ≥80% coverage |
| Docker Build | `docker build` | Success, <500MB |
| Security | `trivy` / `snyk` | 0 critical, 0 high |
| Docs | `markdownlint` | 0 errors |

### Git Workflow
```
main (protected) ← PR ← feature/TASK-ID-description ← developer
     ↑
CI/CD Pipeline: Build → Test → Lint → Security → Docs → Deploy (staging)
```

### Commit Convention
```
<type>(<scope>): <subject>

<body>

<footer>
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`

---

## 🐳 Docker Services

```bash
# Core infrastructure
docker-compose up -d agent-brain

# Agent runners
docker-compose --profile agents up -d

# 3D/Video workers
docker-compose --profile workers up -d

# Unity builder
docker-compose --profile builders up -d

# Database (optional)
docker-compose --profile database up -d

# Monitoring (optional)
docker-compose --profile monitoring up -d
```

---

## 🔐 Required Secrets

| Secret | Purpose | Where |
|--------|---------|-------|
| `GITHUB_TOKEN` | GitHub API access | GitHub Secrets, `.env` |
| `MESHY_API_KEY` | Meshy AI 3D generation | GitHub Secrets, `.env` |
| `MINIMAX_API_KEY` | Minimax video/audio | GitHub Secrets, `.env` |
| `UNITY_LICENSE` | Unity build license | GitHub Secrets (CI) |
| `DOCKER_HUB_TOKEN` | Docker registry | GitHub Secrets |
| `AGENT_BRAIN_URL` | Agent Brain endpoint | `.env` (default: http://localhost:3030) |

---

## 📈 Success Metrics

| Metric | Target | Current |
|--------|--------|---------|
| Task Completion Rate | ≥95% | 0% |
| First-Pass Test Pass | 100% | - |
| Code Coverage | ≥80% | - |
| Build Success Rate | 100% | - |
| Doc Coverage | 100% | 10% |
| Checkpoint Compliance | 100% | - |
| Research per Task | 100% | 0% |
| Asset Pipeline Success | 100% | - |

---

## 📚 Key Documents

| Document | Purpose |
|----------|---------|
| [`PROJECT_MANIFEST.md`](PROJECT_MANIFEST.md) | Master architecture & governance |
| [`docs/planning/TASKS_INDEX.md`](docs/planning/TASKS_INDEX.md) | Master task tracker |
| [`docs/planning/RESEARCH/RESEARCH_INDEX.md`](docs/planning/RESEARCH/RESEARCH_INDEX.md) | Research tracker |
| [`docs/project/DECISION_LOG.md`](docs/project/DECISION_LOG.md) | Architecture decisions |
| [`docs/architecture/ARCHITECTURE.md`](docs/architecture/ARCHITECTURE.md) | System design (TODO) |
| [`docs/development/DEVELOPMENT_STANDARDS.md`](docs/development/DEVELOPMENT_STANDARDS.md) | Coding standards (TODO) |

---

## 🤝 Contributing

This project uses **AI-agent orchestration** with **human-in-the-loop checkpoints**. See:
- [`CONTRIBUTING.md`](CONTRIBUTING.md) - Contribution guidelines
- [`docs/development/GIT_WORKFLOW.md`](docs/development/GIT_WORKFLOW.md) - Git workflow
- [`docs/agents/AGENT_ORCHESTRATION.md`](docs/agents/AGENT_ORCHESTRATION.md) - Agent protocols

---

## 📄 License

MIT License - See [`LICENSE`](LICENSE) for details.

---

## 🔗 Links

- **GitHub**: [krugerw007-git/MAXX](https://github.com/krugerw007-git/MAXX)
- **Agent Brain**: http://localhost:3030
- **Project Manifest**: [`PROJECT_MANIFEST.md`](PROJECT_MANIFEST.md)
- **Task Index**: [`docs/planning/TASKS_INDEX.md`](docs/planning/TASKS_INDEX.md)

---

*Last Updated: 2026-07-16 | Generated by Claude Code (Primary Orchestrator)*