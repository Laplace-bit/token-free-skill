# Platform setup and first use

Checked against upstream documentation on 2026-10-10. Re-read the linked current release notes before a future install; asset names, requirements, and support status can change.

For executable discovery, quoted shell commands, safe reruns and acceptance criteria, read [execution-and-recovery.md](execution-and-recovery.md). Runtime versions below describe the reviewed plugin version; use the installed package's current requirements rather than pinning them in a new setup.

## Magpie installation

Magpie is the local gateway and model/agent configuration manager. It is a separate project from the Our Free Model plugin.

First inspect the host OS and CPU architecture and check whether Magpie already works. If present, reuse it; use Magpie's own update flow if the user asked to update. Do not reinstall over an existing app or alter its configuration/data to make a new install easier.

### macOS

- Choose the official Apple Silicon (`arm64`) or Intel (`amd64`) release from [usemagpie.ai](https://usemagpie.ai/zh/) or [Magpie releases](https://github.com/yetone/magpie-releases/releases).
- The official shell installer is suitable for macOS and checks the downloaded release's SHA-256 against the feed from usemagpie.ai. Fetch it from `https://usemagpie.ai/install.sh`, inspect the saved script, then run it only if the user requested installation. It installs `magpie.app` into `/Applications` (or `~/Applications` if that is not writable) and the CLI into `~/.local/bin`.
- Installation may leave the command outside PATH; use the resolved full path until the user chooses to adjust PATH. Inspect existing app destinations before running an installer that may replace them.
- The site has shown conflicting minimum macOS versions (12+ in one place and 11+ elsewhere). Check the current release/site requirement; when unresolved, do not promise support below macOS 12.

### Windows

- Do not run the Unix `curl | sh` installer in PowerShell. The official release offers `magpie-windows-amd64.exe` and `magpie-windows-arm64.exe`; download the matching asset from the official site/release. `https://usemagpie.ai/api/latest` provides each asset URL and SHA-256. Verify the downloaded file against that official SHA-256 before launching it.
- Keep the executable in a stable user-owned directory so Magpie's configuration and plugin registration remain available. The Windows executable accepts the same CLI commands as `magpie`; invoke it by its full path when a `magpie` command is not on PATH.
- Current Windows builds may be unsigned and trigger SmartScreen. Do not disable or bypass SmartScreen. If the OS blocks launch, explain the official source and hand the decision back to the user.
- The site's current platform notes list Windows 10+ and x64/ARM support. Recheck these against the selected release.

### Linux

- The official installer supports x86-64 and ARM64, installs the command in `~/.local/bin`, and adds a desktop entry when it can install the desktop build.
- The desktop app requires GTK 3 and WebKitGTK 4.1 at runtime. The installer chooses the terminal-only build if the WebKitGTK 4.1 runtime is absent; do not install development headers just to run a released app. If the user wants the desktop app, identify the distribution-specific runtime packages first. Ask before using `sudo` or another privileged package-manager operation.
- Fetch and inspect `https://usemagpie.ai/install.sh` before running the official installer. The script verifies the release SHA-256. When only the CLI is available, use the current Magpie-supported web/TUI workflow described by upstream docs.

### Official installer notes

The official shell installer also accepts `--proxy <url>` and `--mirror <prefix>`. A mirror is optional; if used, keep the SHA-256 supplied by usemagpie.ai as the authority. Do not substitute third-party installers or hard-code a release version from this document.

## Add the Our Free Model plugin

The plugin repository is a third-party Magpie adapter. Its README's normal path is:

```sh
git clone https://github.com/mu-zi-lee/magpie-our-free-model.git
magpie plugin add /absolute/path/to/magpie-our-free-model
```

Use a persistent user directory (for example, `~/.local/share/magpie-plugins/magpie-our-free-model` on macOS/Linux or `%LOCALAPPDATA%\magpie-plugins\magpie-our-free-model` on Windows). Magpie registers the local path, so do not clone into a temporary directory or move it after adding it. On Windows invoke the official executable with `plugin add <path>` if `magpie` is not on PATH. If Git is unavailable, download the ZIP from this exact GitHub repository, extract it to a persistent location, and add that directory in Magpie's Plugins page. Follow the repository's latest README if its supported installation route changes.

Normal setup does not need `npm install`, compilation, a separate Our Free Model launch, or a global Node.js install. On first plugin enable, it can download Node.js 24.21.0 when a compatible Node.js (22.19+ or 24+) is absent. Its runtime stays in the plugin data directory and is SHA-256 checked; the project says this does not need root or system PATH changes. macOS/Linux need `tar` for these downloads. The plugin can also fetch `cloudflared` when a remote management tunnel is requested; prefer the local console on a desktop machine.

These are runtime details recorded for plugin 0.8.0. Check the installed `package.json` and README for changed Node requirements and managed download versions before troubleshooting.

The project lists automatic Node downloads for Linux/macOS/Windows x64 and ARM64 (Alpine currently x64 only), but its README and validation notes say that some OS/runtime paths have not been exercised on the corresponding hardware. Its Cloudflare binary list includes Windows x64, not Windows ARM64. Do not promise that an unverified combination will work. If activation fails, report the precise OS/architecture and error; do not silently install global runtimes or switch to a different provider.

## First use

1. In Magpie's Plugins page, confirm **Our Free Model** is installed and enabled.
2. Open **Providers → Our Free Model → Login/connection**. For a local desktop, use the local model/account management entry and open the complete `http://127.0.0.1:<port>/open/...` link it generates. For a headless server, choose the temporary remote console or use SSH forwarding as documented by the plugin. If the first click only returns to Magpie, repeat the same connection choice to obtain/open the link.
3. The plugin management link is one-use and expires after 10 minutes. A Cloudflare management tunnel lasts at most 30 minutes; regenerate it in Magpie when needed. The Cloudflare option does not require a Cloudflare account, but it is still a secret management link. It exposes the plugin management console, not the model API. Keep it private and keep Magpie running while using the plugin.
4. Choose an actual provider path in the console. Anonymous Zen/Kilo models may be available without account setup. EAC requires its GitHub login and Star check. Account channels need the corresponding provider login. The UI's “connected” state means the plugin is active; it does not prove that a given model or quota is available.
5. Return to Magpie, refresh the provider's models, then use **Agents** to select a model under `our-free-model`. Start a new agent session. Magpie's gateway runs locally at `127.0.0.1:3425`; keep the Magpie app or supported host process running. If changing a Codex model list, restart Codex and any open Codex session.

Keep desktop Magpie, `magpie web`, or `magpie serve` running throughout management and use. A short-lived `magpie plugin login our-free-model` command closes the plugin service when it exits. Do not confuse completing registration with completing runtime/model verification.

Do not collect credentials in chat. Let the user complete browser authorization and vendor sign-in directly. Tell the user that Magpie can also use their existing paid subscriptions, API providers, or local Ollama/LM Studio; API billing follows the provider's terms. A free model pool is not guaranteed to be unlimited, always online, eligible for every account, or permanently free.

## Sources

- [Magpie Chinese homepage](https://usemagpie.ai/zh/)
- [Magpie Chinese quick start](https://usemagpie.ai/docs/zh/start)
- [Magpie releases and platform assets](https://github.com/yetone/magpie-releases/releases)
- [Magpie-Our-Free-Model README](https://github.com/mu-zi-lee/magpie-our-free-model)
- [Plugin validation record](https://github.com/mu-zi-lee/magpie-our-free-model/blob/main/VALIDATION.md)
