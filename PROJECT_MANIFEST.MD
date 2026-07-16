# PROJECT_MANIFEST.MD
# MAXX - AI-Orchestrated Unity Game Development Project
# ========================================================
# Project Manifest & Architecture Manifest
# Version: 1.0.0 | Status: INITIALIZATION | Date: 2026-07-16

---

## PROJECT VISION & MISSION

**MAXX** is a **from-scratch Unity game development project** architected as an **AI-orchestrated, multi-agent orchestration platform**. This project establishes an **industry-standard AI orchestration infrastructure** for game development, integrating multiple AI agents (Claude Code, Codex, Minimax, etc.) via **MCP (Model Context Protocol)** with persistent memory via **Agent Brain**, version-controlled via **GitHub (krugerw007-git)**, containerized via **Docker Desktop**, with **3D asset generation via MESHY AI**, all orchestrated autonomously with human-in-the-loop checkpoints.

---

## ARCHITECTURE OVERVIEW

```
MAXX PROJECT ARCHITECTURE

+--------------------------------------------------------------------------+
|                        ORCHESTRATOR (Claude Code)                         |
|  +----------+  +-----------+  +----------+  +-----------+               |
|  |Agent Brain|  |  MCP Hub  |  |  GitHub  |  |  Docker   |               |
|  | (Memory) |<-|  (MCP Hub)|<-| (krugerw|  |  (Local)  |               |
|  +----+-----+  +-----+-----+  +-----+----+  +-----+-----+               |
|       |            |             |             |                        |
|  +----v------------v-------------v-------------v------+                 |
|  |              SUB-AGENT ORCHESTRATION                  |             |
|  |  +---------+  +---------+  +---------+  +------------+  |            |
|  |  | CLAUDE  |  |  CODEX  |  | MINIMAX |  |   MESHY AI |  |            |
|  |  |  CODE   |  |  (CLI)  |  |  (API)  |  |  (3D Gen)  |  |            |
|  |  |  (MCP)  |  |         |  |         |  |  (3D Asset)|  |            |
|  |  +---------+  +---------+  +---------+  +------------+  |            |
|  +--------------------------------------------------------+             |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
|                       UNITY PROJECT (MAXX)                                |
|  +----------+ +----------+ +----------+ +----------+ +----------+       |
|  |  Assets/ | |  Code/   | |  Assets/ | |  Docs/   | | Tools/   |       |
|  | Scripts  | |  (C#)    | |  3D/2D   | |  (Docs)  | | (Tools)  |       |
|  +----------+ +----------+ +----------+ +----------+ +----------+       |
+--------------------------------------------------------------------------+
                                    |
                                    v
+--------------------------------------------------------------------------+
|                       INFRASTRUCTURE LAYER                                |
|  +----------+ +----------+ +----------+ +----------+ +----------+       |
|  | GitHub   | |  Agent   | |  Docker  | |  Meshy   | |  Agent   |       |
|  | (GitHub) | |  Brain   | |  Desktop | |  AI API  | |  Brain   |       |
|  +----------+ +----------+ +----------+ +----------+ +----------+       |
+--------------------------------------------------------------------------+
```

---

## AI AGENT ORCHESTRATION ARCHITECTURE

### Primary Orchestrator: **Claude Code** (Primary Orchestrator)
- **Role**: Primary orchestrator, task planner, code reviewer, checkpoint gatekeeper
- **MCP Access**: Full Agent Brain MCP, GitHub MCP, Docker MCP, Filesystem MCP
- **Memory**: Agent Brain (persistent cross-session memory)
- **Checkpoints**: Mandatory checkpoints via Agent Brain checkpoint system
- **Responsibilities**: Task planning, code review, checkpoint gates, documentation, git operations

### Sub-Agent: **Codex CLI** (Code Execution Specialist)
- **Role**: Code execution, testing, refactoring, implementation
- **Access**: Local filesystem, GitHub CLI, Docker CLI, Agent Brain (via curl fallback)
- **Memory**: Agent Brain via curl fallback (no native MCP)
- **Checkpoints**: Via `ab-checkpoint` wrapper or curl to Agent Brain
- **Responsibilities**: Implementation, testing, refactoring, CI/CD scripts, Docker ops

### Sub-Agent: **Meshy AI** (3D Asset Generation)
- **Role**: 3D asset generation via Meshy AI API
- **Access**: Meshy AI REST API, Agent Brain via curl
- **Responsibilities**: 3D model generation from text/image/video, texture generation, optimization

### Sub-Agent: **Minimax API** (Video/Audio Generation)
- **Role**: Video generation, audio generation, music generation
- **Access**: Minimax API, Agent Brain via curl
- **Responsibilities**: Cutscene generation, audio assets, promotional content

### Shared Infrastructure: **Agent Brain (localhost:3030)**
- **Purpose**: Persistent cross-session memory, cross-agent mailbox, checkpoints, daily logs
- **Project Key**: `C:\Users\WERNER\My Drive (krugerw007@gmail.com)\GAMEDEV\MAXX` -> `-Users-WERNER-My Drive (krugerw007-gmail-com)-GAMEDEV-MAXX`
- **MCP Tools**: `agent_brain_memory_read`, `agent_brain_memory_write`, `agent_brain_checkpoint`, `agent_brain_mailbox_*`, `agent_brain_daily_log`

---

## PROJECT STRUCTURE (AI Industry Standard)

```
MAXX/
├── .github/                          # GitHub Actions, workflows, issue templates
│   ├── workflows/
│   │   ├── ci.yml
│   │   ├── cd.yml
│   │   ├── code-quality.yml
│   │   ├── docker-build.yml
│   │   └── documentation.yml
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .vscode/                          # VS Code workspace settings
│   ├── settings.json
│   ├── launch.json
│   ├── tasks.json
│   └── extensions.json
│
├── .devcontainer/                    # DevContainer for consistent dev env
│   ├── devcontainer.json
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .github-copilot/                  # GitHub Copilot instructions
│   └── instructions.md
│
├── .opencode/                        # OpenCode configuration
│   ├── opencode.json
│   ├── agents/
│   ├── skills/
│   └── plugins/
│
├── .agent-brain/                     # Agent Brain local config
│   ├── config.json
│   └── project-key.txt
│
├── docs/                             # DOCUMENTATION (Source of Truth)
│   ├── architecture/
│   │   ├── ARCHITECTURE.md
│   │   ├── ARCHITECTURE_DECISIONS.md
│   │   ├── SYSTEM_DESIGN.md
│   │   └── DATA_FLOW.md
│   ├── planning/
│   │   ├── ROADMAP.md
│   │   ├── SPRINTS/
│   │   │   ├── SPRINT_001_INIT.md
│   │   │   ├── SPRINT_002_CORE.md
│   │   │   └── ...
│   │   ├── TASKS_INDEX.md            # Master task index with status
│   │   └── RESEARCH/
│   │       ├── RESEARCH_INDEX.md
│   │       ├── AI_ORCHESTRATION_RESEARCH.md
│   │       ├── MCP_INTEGRATION_RESEARCH.md
│   │       ├── UNITY_ARCHITECTURE_RESEARCH.md
│   │       ├── MESHY_INTEGRATION_RESEARCH.md
│   │       ├── AGENT_BRAIN_INTEGRATION_RESEARCH.md
│   │       ├── DOCKER_ORCHESTRATION_RESEARCH.md
│   │       ├── GITHUB_WORKFLOW_RESEARCH.md
│   │       └── UNITY_CSHARP_STANDARDS_RESEARCH.md
│   ├── api/
│   │   ├── MESHY_API.md
│   │   ├── MINIMAX_API.md
│   │   ├── AGENT_BRAIN_API.md
│   │   ├── GITHUB_API.md
│   │   └── UNITY_API.md
│   ├── development/
│   │   ├── DEVELOPMENT_STANDARDS.md
│   │   ├── CODING_STANDARDS_CS.md
│   │   ├── CODING_STANDARDS_PY.md
│   │   ├── GIT_WORKFLOW.md
│   │   ├── DOCKER_WORKFLOW.md
│   │   ├── TESTING_STRATEGY.md
│   │   ├── CI_CD_PIPELINE.md
│   │   └── DOCUMENTATION_STANDARDS.md
│   ├── agents/
│   │   ├── AGENT_ORCHESTRATION.md
│   │   ├── CLAUDE_CODE_AGENT.md
│   │   ├── CODEX_AGENT.md
│   │   ├── MINIMAX_AGENT.md
│   │   ├── MESHY_AGENT.md
│   │   └── AGENT_BRAIN_INTEGRATION.md
│   ├── infrastructure/
│   │   ├── DOCKER_INFRASTRUCTURE.md
│   │   ├── GITHUB_INFRASTRUCTURE.md
│   │   ├── AGENT_BRAIN_INFRASTRUCTURE.md
│   │   └── MESHY_INFRASTRUCTURE.md
│   ├── project/
│   │   ├── PROJECT_CHARTER.md
│   │   ├── PROJECT_MANIFEST.md (THIS FILE)
│   │   ├── ROADMAP.md
│   │   └── DECISION_LOG.md
│   └── runtime/
│       ├── AGENT_SESSIONS/
│       ├── CHECKPOINTS/
│       ├── DAILY_LOGS/
│       └── CHECKPOINTS_LOG.md
│
├── src/                              # UNITY SOURCE CODE (C#)
│   ├── Assets/
│   │   ├── Scripts/
│   │   │   ├── Core/
│   │   │   │   ├── Architecture/
│   │   │   │   ├── Events/
│   │   │   │   ├── DI/
│   │   │   │   └── Initialization/
│   │   │   ├── Gameplay/
│   │   │   │   ├── Player/
│   │   │   │   ├── Enemies/
│   │   │   │   ├── Systems/
│   │   │   │   └── Mechanics/
│   │   │   ├── AI/
│   │   │   │   ├── BehaviorTrees/
│   │   │   │   ├── GOAP/
│   │   │   │   └── UtilityAI/
│   │   │   ├── Networking/
│   │   │   ├── UI/
│   │   │   ├── Audio/
│   │   │   ├── VFX/
│   │   │   ├── Editor/
│   │   │   └── Tests/
│   │   ├── Scenes/
│   │   ├── Prefabs/
│   │   ├── ScriptableObjects/
│   │   ├── Resources/
│   │   ├── StreamingAssets/
│   │   └── Shaders/
│   └── Packages/
│       └── manifest.json
│
├── tools/                            # TOOLS & AUTOMATION (Python/PS/Bash)
│   ├── python/
│   │   ├── scripts/
│   │   │   ├── agent_orchestration/
│   │   │   │   ├── orchestrator.py
│   │   │   │   ├── agent_brain_client.py
│   │   │   │   ├── checkpoint_manager.py
│   │   │   │   ├── task_orchestrator.py
│   │   │   │   └── agent_mailbox.py
│   │   │   ├── github_automation/
│   │   │   │   ├── github_client.py
│   │   │   │   ├── pr_automation.py
│   │   │   │   ├── issue_automation.py
│   │   │   │   └── release_automation.py
│   │   │   ├── docker_automation/
│   │   │   │   ├── docker_manager.py
│   │   │   │   ├── compose_manager.py
│   │   │   │   └── image_builder.py
│   │   │   ├── meshy_integration/
│   │   │   │   ├── meshy_client.py
│   │   │   │   ├── asset_generator.py
│   │   │   │   └── asset_optimizer.py
│   │   │   ├── minimax_integration/
│   │   │   │   ├── minimax_client.py
│   │   │   │   ├── video_generator.py
│   │   │   │   └── audio_generator.py
│   │   │   ├── unity_automation/
│   │   │   │   ├── unity_builder.py
│   │   │   │   ├── unity_test_runner.py
│   │   │   │   └── asset_processor.py
│   │   │   ├── agent_brain/
│   │   │   │   ├── memory_client.py
│   │   │   │   ├── checkpoint_client.py
│   │   │   │   └── mailbox_client.py
│   │   │   ├── documentation/
│   │   │   │   ├── doc_generator.py
│   │   │   │   ├── index_generator.py
│   │   │   │   └── manifest_updater.py
│   │   │   └── utils/
│   │   │       ├── logger.py
│   │   │       ├── config_loader.py
│   │   │       ├── file_utils.py
│   │   │       └── git_utils.py
│   │   ├── requirements.txt
│   │   ├── requirements-dev.txt
│   │   └── pyproject.toml
│   │
│   ├── powershell/
│   │   ├── scripts/
│   │   │   ├── unity_build.ps1
│   │   │   ├── unity_test.ps1
│   │   │   ├── docker_deploy.ps1
│   │   │   ├── github_sync.ps1
│   │   │   └── agent_launch.ps1
│   │   └── modules/
│   │       └── UnityBuild.psm1
│   │
│   └── bash/
│       ├── scripts/
│       │   ├── setup.sh
│       │   ├── dev-start.sh
│       │   └── cleanup.sh
│       └── lib/
│
├── infrastructure/                   # INFRASTRUCTURE (Docker, K8s, Terraform)
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.dev.yml
│   │   ├── docker-compose.prod.yml
│   │   ├── docker-compose.agents.yml
│   │   ├── Dockerfile.unity-builder
│   │   ├── Dockerfile.agent-runner
│   │   ├── Dockerfile.meshy-worker
│   │   ├── Dockerfile.minimax-worker
│   │   └── .dockerignore
│   ├── kubernetes/
│   │   ├── base/
│   │   ├── overlays/
│   │   │   ├── dev/
│   │   │   ├── staging/
│   │   │   └── prod/
│   │   └── helm/
│   └── terraform/
│       ├── main.tf
│       ├── variables.tf
│       └── modules/
│
├── assets/                           # GAME ASSETS (Source & Generated)
│   ├── 3d/
│   │   ├── source/
│   │   ├── generated/
│   │   │   ├── models/
│   │   │   ├── textures/
│   │   │   └── animations/
│   │   ├── optimized/
│   │   └── imports/
│   │
│   ├── 2d/
│   │   ├── source/
│   │   ├── generated/
│   │   ├── atlases/
│   │   └── ui/
│   │
│   ├── audio/
│   │   ├── source/
│   │   ├── generated/
│   │   ├── music/
│   │   └── sfx/
│   │
│   └── video/
│       ├── source/
│       ├── generated/
│       └── cutscenes/
│
├── tests/                            # TESTS (Cross-project)
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   ├── performance/
│   └── contract/
│
├── scripts/                          # PROJECT SCRIPTS (Entry points)
│   ├── setup.py
│   ├── dev.py
│   ├── build.py
│   ├── test.py
│   ├── deploy.py
│   └── docs.py
│
├── config/                           # CONFIGURATION
│   ├── unity/
│   │   ├── ProjectSettings/
│   │   └── Packages/
│   ├── agents/
│   │   ├── claude_code.json
│   │   ├── codex.json
│   │   ├── minimax.json
│   │   └── meshy.json
│   ├── docker/
│   ├── github/
│   └── agent_brain/
│
├── logs/                             # LOGS (Runtime)
│   ├── agents/
│   ├── builds/
│   ├── tests/
│   └── deployments/
│
├── .gitignore
├── .gitattributes
├── .editorconfig
├── README.md                         # LIVE PROJECT STATUS
├── PROJECT_MANIFEST.md               # THIS FILE
├── LICENSE
├── CONTRIBUTING.md
├── CHANGELOG.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── package.json
├── docker-compose.yml
├── Makefile
└── .env.example
```

---

## TASK MANAGEMENT SYSTEM

### Task Status Legend
| Status | Emoji | Meaning |
|--------|-------|---------|
| COMPLETE | [DONE] | 100% done, tested, documented, committed |
| IN_PROGRESS | [WIP] | Currently being worked on |
| PENDING | [PEND] | Queued, dependencies not met |
| UNCERTAIN | [?] | Blocked, needs clarification |
| IN_REVIEW | [REVIEW] | Code review / QA in progress |
| BLOCKED | [BLOCK] | Blocked by external dependency |
| PLANNED | [PLAN] | Planned, not yet started |
| RESEARCH | [RSCH] | Research phase |
| DOCUMENTING | [DOC] | Documentation phase |
| TESTING | [TEST] | Testing phase |
| DEPLOYING | [DEPLOY] | Deployment phase |

### Task Index Format (TASKS_INDEX.md)

```
# TASKS INDEX - MAXX Project

## SPRINT 001: PROJECT INITIALIZATION & INFRASTRUCTURE
| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |
|----|------|--------|---|----------|------|-------|-----|-------|
| T001 | Create PROJECT_MANIFEST.md | [DONE] | 100% | Claude | [DONE] | N/A | N/A | This file |
| T002 | Initialize GitHub repo (krugerw007-git/MAXX) | [WIP] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T003 | Setup GitHub Actions CI/CD | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T004 | Setup Docker infrastructure | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T005 | Setup Agent Brain integration | [PLAN] | 0% | Claude | [PEND] | [PEND] | [PEND] | |
| T006 | Setup Meshy AI integration | [PLAN] | 0% | Meshy | [PEND] | [PEND] | [PEND] | |
| T007 | Setup Minimax API integration | [PLAN] | 0% | Minimax | [PEND] | [PEND] | [PEND] | |
| T008 | Setup Agent Brain MCP for Claude Code | [PLAN] | 0% | Claude | [PEND] | [PEND] | [PEND] | |
| T009 | Setup Codex Agent Brain integration (curl) | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T010 | Create project directory structure | [WIP] | 10% | Claude | [WIP] | N/A | N/A | In progress |

## SPRINT 002: UNITY PROJECT FOUNDATION
| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |
|----|------|--------|---|----------|------|-------|-----|-------|
| T020 | Initialize Unity project (2022.3 LTS) | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T021 | Setup Unity Package Manager | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T022 | Setup Core Architecture (DI, Events, Core) | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T023 | Setup Dependency Injection (VContainer) | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T024 | Setup Event System (R3/UniRx) | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T025 | Setup Addressables/Asset Management | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T026 | Setup Unit Test Framework (NUnit) | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T027 | Setup CI for Unity builds | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |

## SPRINT 003: AGENT ORCHESTRATION INFRASTRUCTURE
| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |
|----|------|--------|---|----------|------|-------|-----|-------|
| T030 | Build Agent Orchestrator (Python) | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T031 | Build Agent Brain Python Client | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T032 | Build Checkpoint Manager | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T033 | Build Task Orchestrator | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T034 | Build Agent Mailbox System | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T035 | Build GitHub Automation Client | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T036 | Build Docker Manager | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T037 | Build Meshy AI Client | [PLAN] | 0% | Meshy | [PEND] | [PEND] | [PEND] | |
| T038 | Build Minimax Client | [PLAN] | 0% | Minimax | [PEND] | [PEND] | [PEND] | |
| T039 | Build Unity Automation Tools | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |

## SPRINT 004: DOCUMENTATION & RESEARCH FOUNDATION
| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |
|----|------|--------|---|----------|------|-------|-----|-------|
| T040 | Research: AI Orchestration Patterns | [RSCH] | 0% | Claude | [RSCH] | N/A | N/A | |
| T041 | Research: MCP Integration Patterns | [RSCH] | 0% | Claude | [RSCH] | N/A | N/A | |
| T042 | Research: Unity Architecture Patterns | [RSCH] | 0% | Unity | [RSCH] | N/A | N/A | |
| T043 | Research: Meshy AI Integration | [RSCH] | 0% | Meshy | [RSCH] | N/A | N/A | |
| T044 | Research: Agent Brain Integration | [RSCH] | 0% | Claude | [RSCH] | N/A | N/A | |
| T045 | Research: Docker Orchestration | [RSCH] | 0% | Codex | [RSCH] | N/A | N/A | |
| T046 | Research: GitHub Workflow Standards | [RSCH] | 0% | Codex | [RSCH] | N/A | N/A | |
| T047 | Research: Unity C# Standards | [RSCH] | 0% | Unity | [RSCH] | N/A | N/A | |
| T048 | Create ARCHITECTURE.md | [PLAN] | 0% | Claude | [PLAN] | N/A | N/A | |
| T049 | Create DEVELOPMENT_STANDARDS.md | [PLAN] | 0% | Claude | [PLAN] | N/A | N/A | |
| T050 | Create GIT_WORKFLOW.md | [PLAN] | 0% | Codex | [PLAN] | N/A | N/A | |
| T051 | Create DOCUMENTATION_STANDARDS.md | [PLAN] | 0% | Claude | [PLAN] | N/A | N/A | |
| T052 | Create TESTING_STRATEGY.md | [PLAN] | 0% | Codex | [PLAN] | N/A | N/A | |

## SPRINT 005: CORE GAMEPLAY FOUNDATION
| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |
|----|------|--------|---|----------|------|-------|-----|-------|
| T060 | Design Core Gameplay Loop | [PLAN] | 0% | GameDesigner | [PEND] | [PEND] | [PEND] | |
| T061 | Implement Player Controller | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T062 | Implement Camera System | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T063 | Implement Input System (New Input System) | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T064 | Implement Game State Machine | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T065 | Implement Save/Load System | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T066 | Implement Settings/Config System | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |

## SPRINT 006: AI INTEGRATION (GAME AI)
| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |
|----|------|--------|---|----------|------|-------|-----|-------|
| T070 | Design Game AI Architecture | [PLAN] | 0% | AIEng | [PEND] | [PEND] | [PEND] | |
| T071 | Implement Behavior Tree System | [PLAN] | 0% | AIEng | [PEND] | [PEND] | [PEND] | |
| T072 | Implement GOAP Planner | [PLAN] | 0% | AIEng | [PEND] | [PEND] | [PEND] | |
| T073 | Implement Utility AI | [PLAN] | 0% | AIEng | [PEND] | [PEND] | [PEND] | |
| T074 | Integrate Agent Brain for Game AI Memory | [PLAN] | 0% | AIEng | [PEND] | [PEND] | [PEND] | |

## SPRINT 007: 3D ASSET PIPELINE (MESHY)
| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |
|----|------|--------|---|----------|------|-------|-----|-------|
| T080 | Meshy Asset Generation Pipeline | [PLAN] | 0% | Meshy | [PEND] | [PEND] | [PEND] | |
| T081 | Asset Optimization Pipeline | [PLAN] | 0% | Meshy | [PEND] | [PEND] | [PEND] | |
| T082 | Unity Import Pipeline | [PLAN] | 0% | Unity | [PEND] | [PEND] | [PEND] | |
| T083 | LOD Generation | [PLAN] | 0% | Meshy | [PEND] | [PEND] | [PEND] | |
| T084 | Texture Baking Pipeline | [PLAN] | 0% | Meshy | [PEND] | [PEND] | [PEND] | |

## SPRINT 008: CI/CD & DEPLOYMENT
| ID | Task | Status | % | Assignee | Docs | Tests | PR | Notes |
|----|------|--------|---|----------|------|-------|-----|-------|
| T090 | GitHub Actions CI Pipeline | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T091 | GitHub Actions CD Pipeline | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T092 | Docker Build Pipeline | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T093 | Unity Build Pipeline | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T094 | Test Automation Pipeline | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T095 | Documentation Generation Pipeline | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
| T096 | Release Automation | [PLAN] | 0% | Codex | [PEND] | [PEND] | [PEND] | |
```

---

## RESEARCH REQUIREMENTS

**Every task MUST have:**
1. **Research Phase** - Documented in `docs/planning/RESEARCH/`
2. **Planning Phase** - Documented in `docs/planning/SPRINTS/`
3. **Execution Phase** - Tracked in `TASKS_INDEX.md` with %
4. **Testing Phase** - All tests pass (100%)
5. **Documentation Phase** - Updated in `docs/`
6. **Review Phase** - Code review + checkpoint
7. **Completion** - [DONE] Only when ALL above are [DONE]

### Required Research Documents
| Doc | Status | Owner |
|-----|--------|-------|
| AI_ORCHESTRATION_RESEARCH.md | [RSCH] | Claude |
| MCP_INTEGRATION_RESEARCH.md | [RSCH] | Claude |
| UNITY_ARCHITECTURE_RESEARCH.md | [RSCH] | Unity |
| MESHY_INTEGRATION_RESEARCH.md | [RSCH] | Meshy |
| AGENT_BRAIN_INTEGRATION_RESEARCH.md | [RSCH] | Claude |
| DOCKER_ORCHESTRATION_RESEARCH.md | [RSCH] | Codex |
| GITHUB_WORKFLOW_RESEARCH.md | [RSCH] | Codex |
| UNITY_CSHARP_STANDARDS_RESEARCH.md | [RSCH] | Unity |

---

## DEVELOPMENT STANDARDS

### Code Quality Gates (ALL MUST PASS)
| Gate | Tool | Threshold |
|------|------|-----------|
| C# Compilation | `dotnet build` | 0 errors, 0 warnings |
| C# Style | `dotnet format` / `csharpier` | 0 violations |
| C# Analysis | `sonarscanner` / `Roslynator` | 0 critical, 0 major |
| Unit Tests | `dotnet test` | 100% pass, >=80% coverage |
| Integration Tests | `dotnet test` | 100% pass |
| Python Lint | `ruff` / `pylint` | 0 errors |
| Python Type Check | `mypy` | 0 errors |
| Python Tests | `pytest` | 100% pass, >=80% coverage |
| Docker Build | `docker build` | Success, <500MB |
| Security Scan | `trivy` / `snyk` | 0 critical, 0 high |
| Documentation | `markdownlint` | 0 errors |

### Git Workflow (GitFlow + Trunk-Based)
```
main (protected) <-- PR <-- feature/* <-- developer
                    ^
              CI/CD Pipeline
              - Build
              - Test
              - Lint
              - Security
              - Docs
              - Deploy (staging)
```

### Commit Convention (Conventional Commits)
```
<type>(<scope>): <subject>

<body>

<footer>
```
Types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `chore`, `ci`, `build`

### Branch Naming
- `feature/TASK-ID-short-description`
- `fix/TASK-ID-short-description`
- `docs/TASK-ID-short-description`
- `refactor/TASK-ID-short-description`
- `test/TASK-ID-short-description`
- `chore/TASK-ID-short-description`

---

## DOCKER INFRASTRUCTURE (Local-First)

### Services (docker-compose.yml)
```yaml
services:
  # Core Infrastructure
  agent-brain:
    image: agent-brain:latest
    ports: ["3030:3030"]
    volumes: ["./agent-brain-data:/data"]
    healthcheck: [...]
  
  # Agent Runners
  claude-code-runner:
    build: ./infrastructure/docker/Dockerfile.claude-runner
    volumes: [".:/workspace", "/var/run/docker.sock:/var/run/docker.sock"]
    depends_on: [agent-brain]
  
  codex-runner:
    build: ./infrastructure/docker/Dockerfile.codex-runner
    volumes: [".:/workspace"]
    depends_on: [agent-brain]
  
  # 3D Generation Workers
  meshy-worker:
    build: ./infrastructure/docker/Dockerfile.meshy-worker
    environment: [MESHY_API_KEY]
    depends_on: [agent-brain]
  
  minimax-worker:
    build: ./infrastructure/docker/Dockerfile.minimax-worker
    environment: [MINIMAX_API_KEY]
    depends_on: [agent-brain]
  
  # Unity Builder
  unity-builder:
    build: ./infrastructure/docker/Dockerfile.unity-builder
    volumes: ["./src:/project", "./builds:/builds"]
  
  # Database (if needed)
  postgres:
    image: postgres:16-alpine
    environment: [POSTGRES_DB=maxx, POSTGRES_USER=maxx, POSTGRES_PASSWORD]
    volumes: ["postgres-data:/var/lib/postgresql/data"]
  
  redis:
    image: redis:7-alpine
    volumes: ["redis-data:/data"]

volumes:
  agent-brain-data:
  postgres-data:
  redis-data:
```

---

## UNITY PROJECT SPECIFICATIONS

### Unity Version: **2022.3 LTS** (or 6000.x LTS when stable)
### Target Platforms: **PC (Windows), Mac, Linux** (Console later)
### Render Pipeline: **URP (Universal Render Pipeline)**
### Physics: **Unity Physics (Havok)** or **PhysX**
### Networking: **Netcode for GameObjects** / **Netcode for Entities**
### UI: **UI Toolkit** (Runtime) + **UI Builder** (Editor)
### Input: **New Input System** (1.7+)
### DI: **VContainer** (VContainer.Unity)
### Events: **R3 (R3.Observable)** or **UniRx**
### Testing: **NUnit** + **Unity Test Framework** + **NSubstitute**
### Addressables: **Addressable Asset System** (1.23+)
### DOTS/ECS: **Optional** (for high-performance systems only)

### Core Packages (Packages/manifest.json)
```json
{
  "dependencies": {
    "com.unity.render-pipelines.universal": "16.0.0",
    "com.unity.inputsystem": "1.7.0",
    "com.unity.ugui": "1.0.0",
    "com.unity.uitoolkit": "1.0.0",
    "com.unity.addressables": "1.23.0",
    "com.unity.netcode.gameobjects": "1.8.0",
    "com.unity.transport": "1.8.0",
    "com.unity.cinemachine": "2.9.0",
    "com.unity.timeline": "1.7.0",
    "com.unity.recorder": "5.0.0",
    "com.unity.test-framework": "1.1.33",
    "com.unity.nunit": "1.0.0",
    "com.unity.subsystems": "1.0.0",
    "com.unity.entities": "1.2.0",
    "com.unity.collections": "2.0.0",
    "com.unity.mathematics": "1.2.0",
    "com.unity.burst": "1.8.0",
    "com.unity.jobs": "0.7.0",
    "hadsi.vcontainer": "1.18.0",
    "cysharp.r3": "1.2.0"
  }
}
```

---

## AGENT BRAIN INTEGRATION SPECIFICATION

### Project Key
```
Project Key: -Users-WERNER-My Drive (krugerw007-gmail-com)-GAMEDEV-MAXX
```

### Session Startup (Claude Code - MCP)
```python
# At session start
project_key = "-Users-WERNER-My Drive (krugerw007-gmail-com)-GAMEDEV-MAXX"

# 1. Read project memory
memory = agent_brain_memory_read(project=project_key)

# 2. Check mailbox
broadcast_msgs = agent_brain_mailbox_check(project="broadcast", unread=True)
project_msgs = agent_brain_mailbox_check(project=project_key, unread=True)

# 3. Read relevant sections
arch_memory = agent_brain_memory_read(project=project_key, sections=["architecture", "next-steps"])
```

### Session Shutdown (Claude Code - MCP)
```python
# Before session end
agent_brain_memory_write(project=project_key, content=updated_memory)
agent_brain_daily_log(project=project_key, content=daily_log_content)
```

### Checkpoint Protocol (MANDATORY)
```python
# Before ANY major decision or task completion
response = agent_brain_checkpoint(
    project=project_key,
    question="Task complete: <summary>. What would you like me to work on next?",
    options=["Continue with next task", "Review current work", "Change direction", "End session"],
    claude_session_id=extract_session_id()
)

if response.status == "responded":
    # Process user response
    pass
elif response.status == "timeout":
    # Save progress, note what was waiting on
    pass
```

### Cross-Agent Communication
```python
# Send message to another agent
agent_brain_mailbox_send(
    from_session=project_key,
    to_session="target-project-key",  # or "broadcast"
    subject="Task Handoff: T030 - Agent Orchestrator",
    body="Completed agent orchestrator core. Ready for Codex to implement GitHub automation. Details in memory section 'agent-orchestration'."
)
```

---

## MESHY AI INTEGRATION

### API Configuration
```python
# config/agents/meshy.json
{
  "api_key": "${MESHY_API_KEY}",
  "base_url": "https://api.meshy.ai/v1",
  "endpoints": {
    "text_to_3d": "/text-to-3d",
    "image_to_3d": "/image-to-3d",
    "video_to_3d": "/video-to-3d",
    "text_to_texture": "/text-to-texture",
    "image_to_texture": "/image-to-texture",
    "task_status": "/tasks/{task_id}",
    "model_download": "/models/{model_id}/download"
  },
  "defaults": {
    "text_to_3d": {
      "mode": "preview",
      "art_style": "realistic",
      "topology": "quad",
      "target_polycount": 30000,
      "should_remesh": true,
      "symmetrize": true
    }
  },
  "rate_limits": {
    "requests_per_minute": 30,
    "concurrent_tasks": 5
  }
}
```

### Asset Pipeline
```
Input (Text/Image/Video) 
    -> Meshy API (Async Task)
    -> Poll Task Status
    -> Download GLB/USDZ
    -> Optimize (MeshOptimizer, Draco)
    -> Generate LODs (3 levels)
    -> Bake Textures (PBR)
    -> Unity Import Settings (.meta)
    -> Addressables Build
    -> Asset Database
```

---

## MINIMAX INTEGRATION

### API Configuration
```python
# config/agents/minimax.json
{
  "api_key": "${MINIMAX_API_KEY}",
  "base_url": "https://api.minimax.chat/v1",
  "endpoints": {
    "video_generation": "/video/generation",
    "audio_generation": "/audio/generation",
    "music_generation": "/music/generation",
    "voice_cloning": "/voice/clone",
    "task_status": "/tasks/{task_id}"
  },
  "video": {
    "model": "video-01",
    "resolution": "1280x720",
    "duration": 6,
    "fps": 24
  },
  "audio": {
    "model": "speech-01",
    "voice": "male-qn-qingse",
    "speed": 1.0,
    "pitch": 0
  }
}
```

---

## MONITORING & OBSERVABILITY

### Metrics Collection
- **Agent Performance**: Task duration, success rate, token usage
- **Build Metrics**: Build time, size, test coverage
- **Asset Pipeline**: Generation time, file size, quality metrics
- **Unity Build**: Compile time, asset import time, bundle size

### Logging Structure
```
logs/
├── agents/
│   ├── claude-code/
│   │   ├── YYYY-MM-DD.jsonl
│   │   └── checkpoints.jsonl
│   ├── codex/
│   ├── meshy/
│   └── minimax/
├── builds/
│   └── YYYY-MM-DD_build_*.log
├── tests/
│   └── YYYY-MM-DD_test_*.log
└── deployments/
    └── YYYY-MM-DD_deploy_*.log
```

---

## SECURITY & SECRETS

### Secret Management
- **Local**: `.env` (gitignored), `.env.local`
- **CI/CD**: GitHub Secrets (Repository & Environment)
- **Docker**: Docker Secrets / BuildKit secrets
- **Agent Brain**: Stored in Agent Brain memory (encrypted at rest)

### Required Secrets
| Secret | Purpose | Location |
|--------|---------|----------|
| `GITHUB_TOKEN` | GitHub API | GitHub Secrets, .env |
| `MESHY_API_KEY` | Meshy AI API | GitHub Secrets, .env |
| `MINIMAX_API_KEY` | Minimax API | GitHub Secrets, .env |
| `AGENT_BRAIN_URL` | Agent Brain URL | .env (default: http://localhost:3030) |
| `UNITY_LICENSE` | Unity License | GitHub Secrets (CI) |
| `DOCKER_HUB_TOKEN` | Docker Registry | GitHub Secrets |

---

## SUCCESS METRICS & KPIs

| Metric | Target | Measurement |
|--------|--------|-------------|
| Task Completion Rate | 95%+ | Completed / Total tasks |
| First-Pass Test Pass Rate | 100% | CI pipeline |
| Code Coverage | >=80% | Coverage reports |
| Build Success Rate | 100% | CI/CD pipeline |
| Documentation Coverage | 100% | Doc coverage tool |
| Agent Checkpoint Compliance | 100% | Checkpoint logs |
| Research Documentation | 100% per task | Research index |
| Asset Pipeline Success | 100% | Meshy/Minimax logs |
| Cross-Agent Sync | Real-time | Agent Brain logs |

---

## IMMEDIATE NEXT STEPS (SPRINT 001)

| Priority | Task | Owner | Checkpoint Required |
|----------|------|-------|---------------------|
| 1 | [DONE] Create PROJECT_MANIFEST.md | Claude | [DONE] |
| 2 | Initialize GitHub repo (krugerw007-git/MAXX) | Codex | [WIP] |
| 3 | Setup project directory structure | Codex | [WIP] |
| 4 | Configure Agent Brain MCP for Claude Code | Claude | [WIP] |
| 5 | Setup Codex Agent Brain integration (curl) | Codex | [WIP] |
| 6 | Create GitHub Actions CI workflow | Codex | [PLAN] |
| 7 | Setup Docker Compose infrastructure | Codex | [PLAN] |
| 8 | Research: AI Orchestration Patterns | Claude | [RSCH] |
| 9 | Research: MCP Integration Patterns | Claude | [RSCH] |
| 10 | Research: Agent Brain Integration | Claude | [RSCH] |

---

## CHANGELOG

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-16 | Claude Code | Initial project manifest creation |

---

## PROJECT CONTROL FILES

| File | Purpose | Location |
|------|---------|----------|
| PROJECT_MANIFEST.md | This file - Master manifest | Root |
| README.md | Live project status | Root |
| TASKS_INDEX.md | Master task tracker | docs/planning/ |
| RESEARCH_INDEX.md | Research tracker | docs/planning/RESEARCH/ |
| DECISION_LOG.md | Architecture decisions | docs/project/ |
| AGENT_SESSIONS/ | Agent session logs | docs/runtime/ |
| CHECKPOINTS_LOG.md | Checkpoint history | docs/runtime/ |
| DAILY_LOGS/ | Daily session logs | docs/runtime/ |

---

## MANIFEST VALIDATION CHECKLIST

- [x] Project vision & mission defined
- [x] Architecture diagram documented
- [x] AI Agent roles defined
- [x] Project structure defined (AI industry standard)
- [x] Task management system defined
- [x] Research requirements defined
- [x] Development standards defined
- [x] Git workflow defined
- [x] Docker infrastructure defined
- [x] Unity specifications defined
- [x] Agent Brain integration specified
- [x] Meshy AI integration specified
- [x] Minimax integration specified
- [x] Monitoring & observability defined
- [x] Security & secrets defined
- [x] Success metrics defined
- [x] Immediate next steps prioritized
- [x] Control files documented

---

**Manifest Status**: [DONE] **ACTIVE** - This document is the single source of truth for project architecture and governance. All agents MUST read this at session start and update it at session end.

**Next Checkpoint**: After GitHub repo initialization and directory structure creation.

---
*Generated by Claude Code (Primary Orchestrator) | Project: MAXX | Date: 2026-07-16*