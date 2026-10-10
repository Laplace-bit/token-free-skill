---
name: token-free-skill
description: Install, configure, update, or troubleshoot Magpie with the Our Free Model plugin on macOS, Windows, or Linux, and guide users through model selection and first use. Apply to this specific workflow rather than generic free-model recommendations.
---

# Token-Free Setup

Help the user install and use [Magpie](https://usemagpie.ai/zh/) with [magpie-our-free-model](https://github.com/mu-zi-lee/magpie-our-free-model). Read [platform-and-usage.md](references/platform-and-usage.md) before installing; recheck the linked upstream instructions when release details or platform support may have changed.

Use [execution-and-recovery.md](references/execution-and-recovery.md) for concrete shell commands, reruns, verification and failures. Treat release versions in the references as dated observations, not versions to install indefinitely. If current docs conflict, use the selected release's metadata and current plugin requirements; disclose an unresolved conflict instead of guessing.

## Setup workflow

1. If the user explicitly asks to install or set up this workflow, proceed with the normal user-level installation. Establish the intended host (desktop, WSL, SSH or container) and target agent. When Python 3 is already available, run `scripts/preflight.py` using its absolute path; otherwise use the shell checks in the execution reference without installing Python just for this helper. Detect native OS/architecture, existing Magpie version and plugin registration. Inspect known destinations even when Magpie is absent from PATH. Reuse working installations and registered plugin paths.
2. Install Magpie from its official site using the matching OS/architecture path in the reference. Prefer user-space installation. Inspect any downloaded installer script before running it and use only the official source. Do not use `sudo` or administrator privileges for optional dependencies without first explaining the exact system change and getting approval. Never disable Windows SmartScreen or other OS security controls.
3. Install the plugin from the exact GitHub repository in a stable, user-owned directory, then add that directory to Magpie only if it is not already registered. Follow the rerun branches in the execution reference. Normal setup does not require `npm install`, compiling, or manually starting Our Free Model. If Git is unavailable, use the repository's GitHub ZIP and Magpie's documented folder-add flow. Record the installed Magpie version and plugin commit/package version for diagnosis.
4. Keep a persistent Magpie host running; verify registration, runtime startup, management-page access and model discovery separately. At browser sign-in or account consent, let the user complete it directly and continue independent work. Never collect passwords, OAuth codes, cookies, API keys or management links in chat. Do not declare the workflow usable merely because a provider appears.
5. Refresh models and select an actual discovered `our-free-model/<model>` for the user's target agent. Before changing that agent's configuration, save a private local backup of the affected files and record the previous model/provider without printing credentials. Use Magpie's supported configuration flow; do not replace the whole configuration or change other agents. If the target agent is missing, finish the two requested tool installs and report that separate prerequisite; do not silently install additional agents.
6. Teach first use, explain the persistent host and new-session requirement, and report the highest verified stage plus anything awaiting user action. If the user asks to test or confirm working model access, that scope includes at most one minimal request to a confirmed free model. Installation alone does not require inference; if cost or eligibility is unclear, leave inference unverified. Never silently route to a paid model. On failure, follow the recovery reference and preserve progress.

## Honest scope and safety

- “Token-free” means using a currently available free model, an already-paid subscription, or a local model where eligible. It does not mean unlimited, guaranteed, or universally zero-cost usage. API providers can bill; free pools, eligibility, quotas, and login flows can change.
- The Our Free Model integration is a third-party adapter, not an official Magpie release. Do not bypass provider authentication, GitHub/Star checks, quotas, rate limits, or terms of service. A connected provider only proves the plugin is enabled; refresh and verify model availability separately.
- Keep credentials in the provider's own login flow or local Magpie UI. Do not put secrets in shell history, public links, repository files, or the skill's logs. Treat the plugin's temporary remote-console URL as a one-time secret and do not share it.
- Before removing or uninstalling the plugin, warn that its cleanup may delete its locally stored accounts and data; proceed only when the user asked for removal.
- If an install is blocked, unsupported on the detected OS/architecture, needs admin access, or would overwrite existing data, stop at that boundary, report the exact issue and the safest next step, and continue with any independent user education.
