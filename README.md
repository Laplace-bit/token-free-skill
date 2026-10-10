# token-free-skill

A portable Agent Skills workflow for setting up [Magpie](https://usemagpie.ai/zh/) and the third-party [Our Free Model Magpie plugin](https://github.com/mu-zi-lee/magpie-our-free-model) across macOS, Windows, and Linux, then connecting the user's chosen agent and guiding first use.

The executor can be any agent that reads Markdown instructions and has suitable local installation tools. Model clients use a Magpie adapter where available, or their documented OpenAI, Anthropic or Gemini custom endpoint settings. See [agent integration](references/agent-integration.md). Clients that do not allow a compatible custom provider cannot be made compatible by a skill alone.

The skill checks the host platform and existing installation, uses official download sources, adds the plugin from a stable local directory, verifies that it is enabled, and hands account sign-in back to the user. It explains the difference between free model pools, existing subscriptions, API billing, and local models.

## Install the skill

Clone the repository, then place it in your agent's documented skill directory or tell the agent to read the downloaded `SKILL.md` directly:

```sh
git clone https://github.com/Laplace-bit/token-free-skill.git
```

Use the invocation supported by that agent (named skill, slash command, or a direct request). For example: “Read `/path/to/token-free-skill/SKILL.md`, install Magpie and Our Free Model on this machine, and configure my chosen agent.” The workflow does not depend on Codex tools or OpenAI services. The optional `agents/openai.yaml` only provides UI metadata for clients that recognize it.

For Codex specifically, an installation example on macOS/Linux is:

```sh
git clone https://github.com/Laplace-bit/token-free-skill.git ~/.codex/skills/token-free-skill
```

For Codex on Windows, clone or copy to `%USERPROFILE%\.codex\skills\token-free-skill`. For Claude Code, OpenCode, Gemini CLI and other executors, use their own current skill-discovery instructions; the repository entrypoint stays `SKILL.md`.

## What to expect

- The Our Free Model repository is a community adapter, not an official Magpie release.
- A free pool can change, become unavailable, require eligibility, or impose quotas. “Token-free” does not promise unlimited or permanently zero-cost access.
- EAC uses its documented GitHub authorization and Star check. Account channels require their provider's login. The skill never asks users to put passwords, OAuth codes, or API keys in chat.
- The plugin's own README and validation notes disclose platform combinations that have not been tested on real hardware. The skill calls those out rather than promising support.

See [SKILL.md](SKILL.md) for the entrypoint and [the platform and usage reference](references/platform-and-usage.md) for OS-specific installation and first-use guidance.

The [execution and recovery guide](references/execution-and-recovery.md) adds concrete shell commands, checksum verification, existing-install reuse, protected configuration backups, bounded retries, and separate checks for installation, runtime, model discovery, agent configuration, and inference. The agent reports which stages it actually verified and which still need a user sign-in.

An optional, read-only environment helper uses Python 3's standard library:

```sh
python3 scripts/preflight.py
```

It detects native architecture (including Rosetta/Windows emulation), WSL/SSH context, available tools, and likely Magpie executables. It does not download software, change files, run Magpie, or read credentials. When Python is unavailable, the skill provides shell checks instead.

Maintainers can run `python3 -m unittest discover -s tests` to verify architecture/host selection. The helper has been run on the author's macOS host; Windows/other-platform installation templates are documentation-derived, not real-hardware installation tests.

## Upstream references

- [Magpie Chinese homepage](https://usemagpie.ai/zh/)
- [Magpie Chinese quick start](https://usemagpie.ai/docs/zh/start)
- [Magpie release assets](https://github.com/yetone/magpie-releases/releases)
- [Our Free Model plugin](https://github.com/mu-zi-lee/magpie-our-free-model)
- [Plugin validation record](https://github.com/mu-zi-lee/magpie-our-free-model/blob/main/VALIDATION.md)

## License

MIT. See [LICENSE](LICENSE).
