# RESEARCH INDEX - MAXX Project

## Research Status Overview

| Research Doc | Status | Owner | Priority | Started | Completed |
|--------------|--------|-------|----------|---------|-----------|
| AI_ORCHESTRATION_RESEARCH.md | 🔬 In Progress | Claude | Critical | 2026-07-16 | - |
| MCP_INTEGRATION_RESEARCH.md | 📋 Planned | Claude | Critical | - | - |
| UNITY_ARCHITECTURE_RESEARCH.md | 📋 Planned | Unity | High | - | - |
| MESHY_INTEGRATION_RESEARCH.md | 📋 Planned | Meshy | High | - | - |
| AGENT_BRAIN_INTEGRATION_RESEARCH.md | 📋 Planned | Claude | Critical | - | - |
| DOCKER_ORCHESTRATION_RESEARCH.md | 📋 Planned | Codex | High | - | - |
| GITHUB_WORKFLOW_RESEARCH.md | 📋 Planned | Codex | High | - | - |
| UNITY_CSHARP_STANDARDS_RESEARCH.md | 📋 Planned | Unity | Medium | - | - |

---

## Research Requirements

### For EACH Research Document:
1. **Problem Statement** - What are we solving?
2. **Current Landscape** - Existing solutions, patterns, tools
3. **Evaluation Criteria** - How we choose
4. **Options Analysis** - Pros/cons of each approach
5. **Recommendation** - Selected approach with justification
6. **Implementation Plan** - Steps to integrate
7. **Risks & Mitigations** - Known issues
8. **References** - Links to sources, examples

### Research Quality Gates:
- [ ] Minimum 3 sources referenced
- [ ] At least 2 implementation examples reviewed
- [ ] Decision matrix with scored options
- [ ] Clear recommendation with rationale
- [ ] Implementation checklist created
- [ ] Peer reviewed by another agent

---

## Research Templates

### Template: AI_ORCHESTRATION_RESEARCH.md
```markdown
# AI Orchestration Patterns Research

## Problem Statement
How to orchestrate multiple AI agents (Claude, Codex, Minimax, Meshy) for Unity game development with persistent memory, checkpoint gates, and cross-agent communication.

## Current Landscape
- LangChain/LangGraph orchestration
- AutoGen multi-agent framework
- CrewAI role-based agents
- Custom MCP-based orchestration
- Agent Brain memory system

## Evaluation Criteria
| Criterion | Weight |
|-----------|--------|
| Memory persistence | 25% |
| Checkpoint support | 20% |
| Cross-agent comms | 20% |
| Unity integration | 15% |
| Local-first | 10% |
| Extensibility | 10% |

## Options Analysis
| Approach | Memory | Checkpoints | Comms | Unity | Local | Extensible | Score |
|----------|--------|-------------|-------|-------|-------|------------|-------|
| LangGraph | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 3.2 |
| AutoGen | ⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | 2.1 |
| CrewAI | ⭐⭐ | ⭐ | ⭐⭐ | ⭐ | ⭐⭐ | ⭐⭐ | 2.0 |
| Custom MCP + Agent Brain | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 4.8 |

## Recommendation
**Custom MCP + Agent Brain** - Purpose-built for our requirements, full control, local-first, integrates with all our tools.

## Implementation Plan
1. Define agent roles and MCP interfaces
2. Implement Agent Brain memory schema
3. Build checkpoint protocol
4. Create mailbox system
5. Build orchestrator (Python)
6. Integrate with Claude Code MCP
7. Integrate Codex (curl fallback)
8. Test with sample tasks

## Risks
- Agent Brain availability (mitigation: local fallback)
- MCP protocol changes (mitigation: version pinning)
- Cross-agent sync complexity (mitigation: event-driven)

## References
- MCP Spec: https://modelcontextprotocol.io
- Agent Brain: http://localhost:3030/docs
- Unity MCP examples: https://github.com/unity-mcp
```

---

## Research Dependencies

```
AI_ORCHESTRATION_RESEARCH.md
    ├── MCP_INTEGRATION_RESEARCH.md (depends on)
    ├── AGENT_BRAIN_INTEGRATION_RESEARCH.md (depends on)
    └── → ARCHITECTURE.md

UNITY_ARCHITECTURE_RESEARCH.md
    ├── UNITY_CSHARP_STANDARDS_RESEARCH.md (depends on)
    └── → ARCHITECTURE.md, src/ structure

MESHY_INTEGRATION_RESEARCH.md
    └── → tools/python/scripts/meshy_integration/

MINIMAX_INTEGRATION_RESEARCH.md (to be added)
    └── → tools/python/scripts/minimax_integration/

DOCKER_ORCHESTRATION_RESEARCH.md
    └── → infrastructure/docker/

GITHUB_WORKFLOW_RESEARCH.md
    └── → .github/workflows/
```

---

## Research Completion Checklist

- [ ] AI_ORCHESTRATION_RESEARCH.md
- [ ] MCP_INTEGRATION_RESEARCH.md
- [ ] UNITY_ARCHITECTURE_RESEARCH.md
- [ ] MESHY_INTEGRATION_RESEARCH.md
- [ ] AGENT_BRAIN_INTEGRATION_RESEARCH.md
- [ ] DOCKER_ORCHESTRATION_RESEARCH.md
- [ ] GITHUB_WORKFLOW_RESEARCH.md
- [ ] UNITY_CSHARP_STANDARDS_RESEARCH.md

**All research must be COMPLETE before Sprint 002 begins.**