Game developer and FDE, working at the seam between artificial intelligence and music theory.

[![wakatime](https://wakatime.com/badge/user/67d1aacd-464b-4a54-979b-a139888cabf5.svg)](https://wakatime.com/@67d1aacd-464b-4a54-979b-a139888cabf5)
[![X / Twitter](https://img.shields.io/badge/-@HsiangNianian-57606a?logo=x&logoColor=white)](https://twitter.com/HsiangNianian)
[![Academic](https://img.shields.io/badge/-academic.jyunko.cn-57606a?logo=googlescholar&logoColor=white)](https://academic.jyunko.cn)
[![GitHub Roast 评分徽章](https://ghfind.com/api/badge/hsiangnianian)](https://ghfind.com/u/hsiangnianian?ref=badge)

> On the score, we learn the theory; but only through interacting with others do we understand the music.

I've always had one absurd idea — compose music in a programming language, and program in a music language. It turns out we can really try it: **[aria](https://github.com/AICMUniversity/aria)**. Beyond that I'm active in [HydroRoll-Team](https://github.com/HydroRoll-Team), and I keep up terminal agents, chatbot runtimes, game tooling, and Chinese documentation for languages I care about.

## Research

- **aria** — a music DSL in Rust: compose in code, program in music ([AICMUniversity](https://github.com/AICMUniversity))
- **Interval algebra** — formalizing interval relations with category theory ([notes](https://academic.jyunko.cn/2025/02/01/Interval-Algebra))
- **Compiler front-end** — from MIDI to music-theory logic
- **Audio synthesis** — a real-time backend, targetable to WebAssembly
- **Game engines** — formal verification through the Rust type system

## Projects

- **[soon](https://github.com/HsiangNianian/soon)** — local-first terminal agent that learns your routines and predicts the next full command
- **[iamai](https://github.com/retrofor/iamai)** — cross-platform AI agent & chatbot runtime with a Rust core and Python plugins
- **[DropOut](https://github.com/HydroRoll-Team/DropOut)** — modern, fast Rust Minecraft launcher; a reproducible Minecraft workspace manager
- **[GlyphWeave](https://github.com/HsiangNianian/GlyphWeave)** — infinite-canvas ASCII roguelike tilemap editor
- **[dsh-auto-continue](https://github.com/HsiangNianian/dsh-auto-continue)** — DSH Web UI plugin that auto-resumes requests interrupted by non-human causes
- **[swi-prolog-docs](https://github.com/HsiangNianian/swi-prolog-docs)** — unofficial SWI-Prolog documentation in Chinese

…and more in [released projects](releases.md).

## This week

<!--START_SECTION:waka-->
📊 **This Week I Spent My Time On** 

```text
💬 Programming Languages: 
Bash                     8 mins              █████████████████░░░░░░░░   69.24 % 
Markdown                 2 mins              █████░░░░░░░░░░░░░░░░░░░░   18.88 % 
Other                    1 min               ███░░░░░░░░░░░░░░░░░░░░░░   11.30 % 
env                      0 secs              ░░░░░░░░░░░░░░░░░░░░░░░░░   00.57 % 

🔥 Editors: 
Neovim                   11 mins             █████████████████████████   100.00 % 

💻 Operating System: 
Mac                      11 mins             █████████████████████████   100.00 % 
```

🤖 **AI Coding This Week** 

```text
No AI Coding Activity Tracked This Week
```


 Last Updated on 01/10/2026 22:22:46 UTC
<!--END_SECTION:waka-->

## Recent releases

<!-- recent_releases starts -->
- [swi-prolog-docs nightly](https://github.com/HsiangNianian/swi-prolog-docs/releases/tag/nightly) · 2026-09-30
- [dsh-auto-continue v0.12.1](https://github.com/HsiangNianian/dsh-auto-continue/releases/tag/v0.12.1) · 2026-09-30
- [jev-turtle-soup v0.41.0 — Compact play across web and native apps](https://github.com/HsiangNianian/jev-turtle-soup/releases/tag/v0.41.0) · 2026-09-29
- [IntelligentMixVideo v0.4.2](https://github.com/HsiangNianian/IntelligentMixVideo/releases/tag/v0.4.2) · 2026-09-28
- [DropOut dropout v0.2.0-rc.2](https://github.com/HydroRoll-Team/DropOut/releases/tag/dropout-v0.2.0-rc.2) · 2026-09-07
- [iamai v1.0.0](https://github.com/retrofor/iamai/releases/tag/v1.0.0) · 2026-08-29
- [GlyphWeave v0.2.0](https://github.com/HsiangNianian/GlyphWeave/releases/tag/v0.2.0) · 2026-08-27
- [soon v0.5.0](https://github.com/HsiangNianian/soon/releases/tag/v0.5.0) · 2026-07-30
- [proof-pr v0.1.1](https://github.com/HsiangNianian/proof-pr/releases/tag/v0.1.1) · 2026-07-18
- [hacktyper 🚀 v0.2.7](https://github.com/HsiangNianian/hacktyper/releases/tag/v0.2.7) · 2026-01-13
<!-- recent_releases ends -->

## Recent posts

<!-- blog starts -->
<details><summary>2026-09-28 <a href="https://academic.jyunko.cn/2026/09/28/qqbot-cryptomining-incident-en.html">I meant to fix a QQ bot. A wall of migration threads led me to two cryptominers.</a></summary><p>Investigating a cryptomining incident with Codex: a QQ bot feature request, disguised miners, separate SSH and RAGFlow intrusion trails, and the limits of cont…</p></details>

<details><summary>2026-09-28 <a href="https://academic.jyunko.cn/2026/09/28/qqbot-cryptomining-incident.html">给 QQ bot 加个功能，顺着一排 migration 抓出两个矿工：我这需求又做偏了</a></summary><p>一次与 Codex 共同完成的服务器挖矿事件排查记录：从 QQ bot 功能开发，到识别伪装矿工、关联 SSH 与 RAGFlow 模板注入证据，再到隔离、取证和清理。</p></details>

<details><summary>2026-09-27 <a href="https://academic.jyunko.cn/2026/09/27/cloudflare-worker-incident-en.html">I only meant to fix a deployment: the Cortex Cloudflare incident</a></summary><p>Working through the Cortex Cloudflare incident with Codex: a failed pnpm install, a Worker rewriting HTML, a hard-to-find account token and the checks after cl…</p></details>

<details><summary>2026-09-27 <a href="https://academic.jyunko.cn/2026/09/27/cloudflare-worker-incident-zh.html">本来只是想修一次部署：Cortex 的 Cloudflare 事件记录</a></summary><p>一次和 Codex 共同排查的记录：从 pnpm 安装失败，到发现前置 Worker 改写 HTML，再到寻找、撤销令牌与恢复 Cortex。</p></details>

<details><summary>2026-02-21 <a href="https://academic.jyunko.cn/2026/02/21/New-Album-Malkuth.html">New Album: Malkuth</a></summary><p>Info</p></details>

<details><summary>2025-10-08 <a href="https://academic.jyunko.cn/2025/10/08/Maillard-Reaction.html">Maillard Reaction</a></summary><p>The Maillard reaction, a complex series of chemical reactions between amino acids and reducing sugars, is responsible for the browning and flavor development i…</p></details>

<details><summary>2025-02-01 <a href="https://academic.jyunko.cn/2025/02/01/Interval-Algebra.html">Interval Algebra: When Category Theory Reshapes Musical DNA</a></summary><p>While debugging an AI composition system at dawn, I encountered the 42nd "parallel fifth paradox": when optimizing harmonic consonance, the model persistently…</p></details>
<!-- blog ends -->

## Contact

PGP [`5DE2131F AD104AEB A3D36BDF 519BB819 4D892FD0`](https://keys.openpgp.org/search?q=5DE2131FAD104AEBA3D36BDF519BB8194D892FD0) · mail `i@jyunko.cn`
