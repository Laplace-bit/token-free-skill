---
name: token-free-skill
description: Install and configure Magpie with the third-party Our Free Model plugin so coding agents can use currently available free, subscribed, API, or local model providers. Use when a user asks to set up or troubleshoot this workflow.
---

# Token-Free Setup

Help the user install and use [Magpie](https://usemagpie.ai/zh/) with [magpie-our-free-model](https://github.com/mu-zi-lee/magpie-our-free-model). Read [platform-and-usage.md](references/platform-and-usage.md) before installing; recheck the linked upstream instructions when release details or platform support may have changed.

## Setup workflow

1. If the user explicitly asks to install or set up this workflow, proceed with the normal user-level installation. Detect the operating system, CPU architecture, existing Magpie version, and whether the plugin is already installed. Reuse working installations; do not overwrite user data, replace an existing install unnecessarily, or move a plugin directory that Magpie already uses.
2. Install Magpie from its official site using the matching OS/architecture path in the reference. Prefer user-space installation. Inspect any downloaded installer script before running it and use only the official source. Do not use `sudo` or administrator privileges for optional dependencies without first explaining the exact system change and getting approval. Never disable Windows SmartScreen or other OS security controls.
3. Install the plugin from the exact GitHub repository in a stable, user-owned directory, then add that directory to Magpie. Follow the repository's current README; normal setup does not require `npm install`, compiling, or manually starting Our Free Model. If Git is unavailable, use the repository's GitHub ZIP and Magpie's documented folder-add flow instead of silently installing more system tools.
4. Verify installation without signing into the user's accounts: confirm Magpie starts, the plugin is enabled, and “Our Free Model” appears as a provider. Stop at any browser sign-in, GitHub authorization, vendor login, or consent step and tell the user exactly what to complete. Never ask them to paste passwords, OAuth codes, cookies, API keys, or one-time management links into chat.
5. Teach first use: enable the plugin, open its management page, complete any user-owned authorization or provider login, return to Magpie and refresh models, select an `our-free-model/<model>` in the desired agent, then start a new agent session. Explain which processes must stay running and any OS-specific limitation encountered.

## Honest scope and safety

- “Token-free” means using a currently available free model, an already-paid subscription, or a local model where eligible. It does not mean unlimited, guaranteed, or universally zero-cost usage. API providers can bill; free pools, eligibility, quotas, and login flows can change.
- The Our Free Model integration is a third-party adapter, not an official Magpie release. Do not bypass provider authentication, GitHub/Star checks, quotas, rate limits, or terms of service. A connected provider only proves the plugin is enabled; refresh and verify model availability separately.
- Keep credentials in the provider's own login flow or local Magpie UI. Do not put secrets in shell history, public links, repository files, or the skill's logs. Treat the plugin's temporary remote-console URL as a one-time secret and do not share it.
- Before removing or uninstalling the plugin, warn that its cleanup may delete its locally stored accounts and data; proceed only when the user asked for removal.
- If an install is blocked, unsupported on the detected OS/architecture, needs admin access, or would overwrite existing data, stop at that boundary, report the exact issue and the safest next step, and continue with any independent user education.
