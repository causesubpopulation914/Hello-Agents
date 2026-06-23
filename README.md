<div align="center">

<img src="https://raw.githubusercontent.com/datawhalechina/Hello-Agents/main/docs/images/hello-agents.png" alt="Hello Agents Banner" width="100%">

# Hello-Agents

### 🤖 Building AI Agent Systems from Scratch

*From foundational theory to production-grade multi-agent applications*

[![GitHub Stars](https://img.shields.io/github/stars/Reyzowter/Hello-Agents?style=for-the-badge&logo=github&color=FFD700)](https://github.com/Reyzowter/Hello-Agents/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Reyzowter/Hello-Agents?style=for-the-badge&logo=github&color=blue)](https://github.com/Reyzowter/Hello-Agents/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/Reyzowter/Hello-Agents?style=for-the-badge&logo=github&color=red)](https://github.com/Reyzowter/Hello-Agents/issues)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey?style=for-the-badge)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Website](https://img.shields.io/badge/Website-helloagents.org-brightgreen?style=for-the-badge&logo=internet-explorer)](http://helloagents.org/)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-orange?style=for-the-badge)](CONTRIBUTING.md)

[🌐 Website](http://helloagents.org/) · [📖 Read Online](#-quick-start) · [🐛 Report Bug](https://github.com/Reyzowter/Hello-Agents/issues/new?template=bug_report.md) · [💡 Request Feature](https://github.com/Reyzowter/Hello-Agents/issues/new?template=feature_request.md)

</div>

---

## 📌 Why Hello-Agents?

> If 2024 was the year of the **Battle of Foundation Models**, then 2025 is undeniably the **Year of Agents**.

The AI landscape is shifting fast — from training bigger models to building smarter **agent systems**. Yet systematic, hands-on learning resources remain scarce. **Hello-Agents** bridges that gap.

This is a complete, open-source curriculum that takes you from zero to building production-grade multi-agent systems. We don't just teach you to *use* agent frameworks — we teach you to *build* them from the ground up.

### ✨ What Sets This Apart

| Feature | Description |
|---|---|
| 🔬 **First-principles approach** | Understand *why* agents work, not just *how* to call APIs |
| 🏗️ **Build your own framework** | Implement a full agent framework from scratch using OpenAI native API |
| 🌐 **Protocol-level coverage** | Deep dives into MCP, A2A, ANP communication protocols |
| 🎓 **Interview-ready** | Curated agent interview questions from top tech companies |
| 💻 **100% runnable code** | Every chapter has tested, working code in the `/code` folder |
| 🤝 **Community-driven** | Active co-creation, open PRs, and community extra chapters |

---

## 🚀 Quick Start

### Option 1 — Read Online (Recommended)

👉 **[http://helloagents.org/](http://helloagents.org/)** — No setup required. Start learning immediately.

### Option 2 — Clone & Run Locally

```bash
# Clone the repository
git clone https://github.com/Reyzowter/Hello-Agents.git
cd Hello-Agents

# Install Python dependencies (for code examples)
pip install -r code/requirements.txt

# Run your first agent
python code/chapter4/react_agent.py
```

### Option 3 — Download PDF

📄 Get the complete tutorial as a beautifully formatted PDF:
> [**Download Latest PDF Release →**](https://github.com/Reyzowter/Hello-Agents/releases/latest)

---

## 📚 Curriculum Overview

The curriculum is divided into **5 structured parts** — each one a solid step forward.

```
Hello-Agents
├── Part 1: Agent & LLM Fundamentals        (Chapters 1–3)
├── Part 2: Building Your First LLM Agent   (Chapters 4–7)
├── Part 3: Advanced Techniques             (Chapters 8–12)
├── Part 4: Real-World Case Studies         (Chapters 13–15)
└── Part 5: Capstone & Future Outlook       (Chapter 16)
```

### 📖 Chapter Index

| # | Chapter | Topics | Status |
|---|---------|--------|--------|
| 0 | [Preface](./docs/Preface.md) | Project origin, background, how to use this book | ✅ |
| **Part 1** | **Agent & Language Model Fundamentals** | | |
| 1 | [Introduction to Agents](./docs/chapter1/Chapter1-Introduction-to-Agents.md) | Agent definition, types, paradigms, real-world applications | ✅ |
| 2 | [History of Agents](./docs/chapter2/Chapter2-History-of-Agents.md) | Symbolic AI → neural nets → LLM-driven agents | ✅ |
| 3 | [LLM Fundamentals](./docs/chapter3/Chapter3-Fundamentals-of-Large-Language-Models.md) | Transformer, prompting, mainstream LLMs and limitations | ✅ |
| **Part 2** | **Building Your LLM Agent** | | |
| 4 | [Classic Agent Paradigms](./docs/chapter4/Chapter4-Building-Classic-Agent-Paradigms.md) | Implement ReAct, Plan-and-Solve, Reflection from scratch | ✅ |
| 5 | [Low-Code Agent Platforms](./docs/chapter5/Chapter5-Building-Agents-with-Low-Code-Platforms.md) | Coze, Dify, n8n — no-code agent building | ✅ |
| 6 | [Framework Development](./docs/chapter6/Chapter6-Framework-Development-Practice.md) | AutoGen, AgentScope, LangGraph in practice | ✅ |
| 7 | [Build Your Own Framework](./docs/chapter7/Chapter7-Building-Your-Agent-Framework.md) | Implement a full agent framework from zero | ✅ |
| **Part 3** | **Advanced Knowledge** | | |
| 8 | [Memory & Retrieval](./docs/chapter8/Chapter8-Memory-and-Retrieval.md) | Memory systems, RAG pipelines, vector storage | ✅ |
| 9 | [Context Engineering](./docs/chapter9/Chapter9-Context-Engineering.md) | Contextual understanding for continuous interaction | ✅ |
| 10 | [Agent Communication Protocols](./docs/chapter10/Chapter10-Agent-Communication-Protocols.md) | MCP, A2A, ANP deep-dives | ✅ |
| 11 | [Agentic-RL](./docs/chapter11/Chapter11-Agentic-RL.md) | LLM training: SFT → GRPO full pipeline | ✅ |
| 12 | [Agent Evaluation](./docs/chapter12/Chapter12-Agent-Performance-Evaluation.md) | Metrics, benchmarks, evaluation frameworks | ✅ |
| **Part 4** | **Real-World Case Studies** | | |
| 13 | [Intelligent Travel Assistant](./docs/chapter13/Chapter13-Intelligent-Travel-Assistant.md) | MCP + multi-agent collaboration in production | ✅ |
| 14 | [Deep Research Agent](./docs/chapter14/Chapter14-Automated-Deep-Research-Agent.md) | Reproducing and extending DeepResearch Agent | ✅ |
| 15 | [Cyber Town Simulation](./docs/chapter15/Chapter15-Building-Cyber-Town.md) | Agents + games, simulating social dynamics | ✅ |
| **Part 5** | **Capstone** | | |
| 16 | [Graduation Project](./docs/chapter16/Chapter16-Graduation-Project.md) | Build your complete multi-agent application | ✅ |

---

## 🎁 Community Extra Chapters

| # | Extra Chapter | Summary |
|---|---------------|---------|
| 00 | [Co-creation Capstone Projects](./Co-creation-projects/) | Community-built multi-agent applications |
| 01 | Agent Interview Questions & Answers | Top agent interview Q&A with detailed answers |
| 02 | Context Engineering Supplement | Extended deep-dive into context management |
| 03 | Dify Agent Step-by-Step Tutorial | Complete Dify agent creation walkthrough |
| 04 | Hello-Agents FAQ | Common questions from the learning community |
| 05 | Agent Skills vs MCP Comparison | Technical comparison of agent skill systems |
| 06 | GUI Agent: Principles & Practice | GUI-driven agent concepts and implementation |
| 07 | Environment Configuration Guide | Setting up your dev environment correctly |
| 08 | Writing Effective Agent Skills | Best practices for skill authoring |
| 09 | Agent Development Pitfalls | Real-world lessons from building a Code Agent |
| 10 | Agent Self-Evolution | Four closed loops of agent self-improvement |
| 11 | Web Agent: Principles & Practice | Web automation, anti-bot, HelloAgents integration |
| 12 | Trip Planner Post-Training | Fine-tuning a trip-planner for real-world use |
| 13 | Video Course Co-creation | Resources for video course contributors |

---

## 🗺️ Who Is This For?

<table>
<tr>
<td align="center" width="200">

**🧑‍💻 AI Developers**

Building agent-powered products and need systematic foundations

</td>
<td align="center" width="200">

**👩‍🎓 Students & Researchers**

Exploring LLM agents for research or coursework

</td>
<td align="center" width="200">

**🏗️ Software Engineers**

Transitioning into AI-native application development

</td>
<td align="center" width="200">

**🎯 Job Seekers**

Preparing for AI engineer interviews at top companies

</td>
</tr>
</table>

**Prerequisites:** Basic Python · Familiarity with calling LLM APIs

---

## 🤝 Contributing

We welcome every form of contribution — from fixing a typo to writing an entire Extra Chapter.

1. **Fork** this repository
2. **Create** your branch: `git checkout -b feat/your-contribution`
3. **Commit**: `git commit -m 'feat: add chapter on X'`
4. **Push**: `git push origin feat/your-contribution`
5. **Open a Pull Request**

📋 Read the full [**Contributing Guide →**](CONTRIBUTING.md)

| Type | How |
|------|-----|
| 🐛 Found a bug | [Open an Issue](https://github.com/Reyzowter/Hello-Agents/issues/new?template=bug_report.md) |
| 💡 Feature idea | [Start a Discussion](https://github.com/Reyzowter/Hello-Agents/discussions) |
| 📝 Improve content | Submit a Pull Request |
| 🌍 Translate | Open an issue to coordinate |

---

## 📊 Star History

<div align="center">

[![Star History Chart](https://api.star-history.com/svg?repos=Reyzowter/Hello-Agents&type=Date)](https://star-history.com/#Reyzowter/Hello-Agents&Date)

</div>

---

## 📜 Citation

```bibtex
@misc{hello_agents2025,
  title     = {Hello-Agents: Building an AI Agent System from Scratch},
  author    = {Reyzowter and Hello-Agents Contributors},
  year      = {2025},
  url       = {https://github.com/Reyzowter/Hello-Agents},
  note      = {GitHub repository — http://helloagents.org/}
}
```

---

## 📄 License

Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) — free for learning, not for commercial resale.

---

<div align="center">

**⭐ If Hello-Agents helps you, please star the repo — it helps others find it!**

Made with ❤️ · [Website](http://helloagents.org/) · [Issues](https://github.com/Reyzowter/Hello-Agents/issues) · [Discussions](https://github.com/Reyzowter/Hello-Agents/discussions)

</div>
