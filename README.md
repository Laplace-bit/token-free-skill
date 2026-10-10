# token-free-skill

A Codex skill for setting up [Magpie](https://usemagpie.ai/zh/) and the third-party [Our Free Model Magpie plugin](https://github.com/mu-zi-lee/magpie-our-free-model) across macOS, Windows, and Linux, then guiding the user through first use.

The skill checks the host platform and existing installation, uses official download sources, adds the plugin from a stable local directory, verifies that it is enabled, and hands account sign-in back to the user. It explains the difference between free model pools, existing subscriptions, API billing, and local models.

## Install the skill

Copy or clone this repository into your Codex skills directory as `token-free-skill`, then invoke it with `$token-free-skill` when you want help installing or troubleshooting this setup. For example, on macOS or Linux:

```sh
git clone https://github.com/Laplace-bit/token-free-skill.git ~/.codex/skills/token-free-skill
```

On Windows, clone or copy the repository to `%USERPROFILE%\.codex\skills\token-free-skill`.

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
