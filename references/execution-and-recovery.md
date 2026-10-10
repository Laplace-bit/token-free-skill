# Execution, reruns and recovery

Use these procedures with the current [Magpie manual](https://github.com/yetone/magpie/blob/main/docs/reference.md) and [plugin README](https://github.com/mu-zi-lee/magpie-our-free-model). Examples assume a fresh installation; inspect every destination before writing. Resolve variables to actual paths and quote them. The preflight helper only inventories the host; it does not install or read credentials.

## Host and shell

On macOS/Linux check `uname -s`, `uname -m`, `command -v magpie`, `command -v git`, `command -v curl`, and `command -v tar`. On macOS, `sysctl -n hw.optional.arm64` equal to `1` identifies native ARM hardware even under Rosetta. On Linux inspect `/etc/os-release` and libc when runtime compatibility fails. WSL is a Linux environment: establish whether installation is intended inside WSL or in Windows before writing files. SSH/container paths and localhost URLs refer to the execution host, which may differ from the user's browser machine.

In PowerShell use `$env:LOCALAPPDATA`, `$env:USERPROFILE`, `Get-Command magpie -ErrorAction SilentlyContinue`, and native architecture from `$env:PROCESSOR_ARCHITEW6432` or `$env:PROCESSOR_ARCHITECTURE`. Unknown architectures require investigation; never default them to x64. `%LOCALAPPDATA%` is cmd.exe syntax, not PowerShell interpolation.

## Magpie install and executable discovery

On Unix, inspect `~/.local/bin/magpie`, `/Applications/magpie.app` and `~/Applications/magpie.app` as appropriate, plus any `MAGPIE_BIN_DIR` destination and symlink targets. Inspect the downloaded installer's current destinations before executing it. The official installer can replace existing files: do not run it merely because PATH lookup failed.

For a genuinely fresh install, fetch into a unique temporary directory:

```sh
magpie_stage=$(mktemp -d)
curl --fail --location --connect-timeout 15 --max-time 120 \
  https://usemagpie.ai/install.sh -o "$magpie_stage/install.sh"
```

Stop if download fails. Read the saved script, then execute `sh "$magpie_stage/install.sh"` as a separate operation after inspection. Use its existing checksum mechanism. Afterwards resolve the executable (normally `$HOME/.local/bin/magpie`) and invoke it by absolute path, for example `"$magpie_exe" help` and `"$magpie_exe" ls`. The installer does not automatically put `~/.local/bin` on PATH. Avoid shell-profile edits unless requested; tell the user the actual command path. Remove only the temporary directory this operation created after inspection/execution is complete.

On Windows, the following is a fresh-install template. Check that the detected native architecture matches the intended Windows host, especially in an emulated shell. Fetch metadata once so asset and hash belong to the same release:

```powershell
$ErrorActionPreference = 'Stop'
$magpieNativeArch = $env:PROCESSOR_ARCHITEW6432
if (!$magpieNativeArch) { $magpieNativeArch = $env:PROCESSOR_ARCHITECTURE }
switch ($magpieNativeArch) {
    'ARM64' { $magpieArch = 'arm64' }
    'AMD64' { $magpieArch = 'amd64' }
    default { throw 'Unknown native architecture; inspect before selecting an asset' }
}
$magpieAssetName = "magpie-windows-$magpieArch.exe"
$magpieFeed = Invoke-RestMethod -Uri 'https://usemagpie.ai/api/latest' -TimeoutSec 60
$magpieAsset = $magpieFeed.assets.$magpieAssetName
if (!$magpieAsset -or $magpieAsset.sha256 -notmatch '^[0-9a-fA-F]{64}$') {
    throw 'Official release metadata has no valid asset/hash for this architecture'
}
if ($magpieAsset.url -notlike 'https://github.com/yetone/magpie-releases/releases/download/*') {
    throw 'Unexpected release asset source; inspect current official metadata'
}
$magpieInstallDir = Join-Path $env:LOCALAPPDATA 'Programs\magpie'
$magpieExe = Join-Path $magpieInstallDir $magpieAssetName
if (Test-Path $magpieExe) { throw 'Existing destination: inspect and reuse before installing' }
$magpieStageFile = Join-Path ([IO.Path]::GetTempPath()) ([guid]::NewGuid().ToString() + '.exe')
try {
    Invoke-WebRequest -UseBasicParsing -Uri $magpieAsset.url -OutFile $magpieStageFile -TimeoutSec 300
    if ((Get-FileHash -LiteralPath $magpieStageFile -Algorithm SHA256).Hash -ne $magpieAsset.sha256) {
        throw 'Checksum mismatch; file must not be executed'
    }
    New-Item -ItemType Directory -Path $magpieInstallDir -Force | Out-Null
    Move-Item -LiteralPath $magpieStageFile -Destination $magpieExe -ErrorAction Stop
} finally {
    if (Test-Path $magpieStageFile) { Remove-Item -LiteralPath $magpieStageFile }
}
```

First inspect the directory for any other existing Magpie executable; its different filename must not be mistaken for a missing install. Stop on nonzero exit codes when calling native commands; PowerShell's `$ErrorActionPreference` alone does not enforce that for native executables. Use `& $magpieExe help` and check `$LASTEXITCODE`. Launch the app only after checksum verification; leave OS security prompts to the user. These templates have not been executed on a Windows host as part of this skill's validation.

## Plugin installation and reruns

1. Inspect Magpie's Plugins page (or a plugin-list command verified by the installed version's `help`). Reuse the registered path; if disabled, enable it through the supported UI. Do not guess `plugin ls` or repeatedly call `plugin add`.
2. If no registration exists but the destination directory exists, inspect its `package.json` name (`magpie-our-free-model`), source and current state. For a Git checkout, verify `git remote get-url origin`, `git status --porcelain` and `git rev-parse HEAD`. Preserve local changes. An unrelated or incomplete directory must not be overwritten or deleted.
3. For a missing source directory, create its parent and clone once to the stable destination. For a ZIP fallback, prefer resolving the current commit via `https://api.github.com/repos/mu-zi-lee/magpie-our-free-model/commits/main`, validating its full 40-hex SHA, and downloading `https://github.com/mu-zi-lee/magpie-our-free-model/archive/<resolved-sha>.zip`. This is commit provenance, not a separately published checksum. If the API is unavailable/rate-limited, use the repository's Code → Download ZIP flow and record the actual archive URL, retrieval date and package version without claiming a commit was verified. Extract into staging first and find the package root containing `package.json` and the declared entrypoint. Move that root to an empty stable destination, not a temporary folder or the archive's parent.
4. Read the checked-out README and package metadata before enabling code. Record the commit and package version. Add using the resolved executable path:

```sh
"$magpie_exe" plugin add "$plugin_dir"
```

```powershell
& $magpieExe plugin add $pluginDir
if ($LASTEXITCODE -ne 0) { throw 'Plugin registration failed; inspect the error before retrying' }
```

If this exact path is already registered, skip the add operation. Upgrade only when requested: on a clean checkout use `git pull --ff-only`, then reload/restart the affected host with attention to active sessions. A dirty checkout or non-fast-forward update requires diagnosis, not `reset --hard`, forced checkout or uninstall. ZIP updates must preserve the registered path and separate account/data directories.

## Verification and user handoff

Keep desktop Magpie, `magpie web`, or `magpie serve` running in a persistent foreground session. `magpie plugin login our-free-model` is a short-lived command whose exit stops its service; it is unsuitable as the user's lasting management entry. Do not kill an existing host or create a system service simply to perform setup. Starting `magpie web` may print a secret access link; do not copy it to public reports.

| Stage | Evidence to observe |
| --- | --- |
| Magpie installed | Resolved executable responds to `help`; version read from installed UI/help |
| Plugin registered/enabled | Correct package and stable path shown in Plugins; no duplicate registration |
| Runtime ready | Persistent host remains running; no runtime/download errors; management page opens |
| Models discovered | Refresh completes and shows actual model IDs; provider appearance alone is insufficient |
| Agent configured | Selected agent's model/provider reflects the discovered ID; other agent settings untouched |
| Inference verified | One minimal confirmed-free request succeeds in a new session, if that check is authorized |

Report only observed stages. If a browser/account step is pending, say what is already complete and give the precise next click; resume at that stage once the user completes it. Use the model ID actually discovered rather than inventing an example. Do not dump `magpie providers` output: the upstream manual describes it as including keys. Inspect only necessary fields and redact secrets, account identifiers and capability URLs from any shared diagnostic.

Before changing the selected agent's configuration, determine its actual file paths from the current upstream agent table and installed configuration/overrides. Default examples are `~/.codex/config.toml` for Codex and `~/.claude/settings.json` for Claude Code; a custom home/config override or WSL host can change the relevant location. Back up only affected existing files to a private local directory. On Unix create that directory with owner-only permissions and protect backup files too; on Windows use the user's private profile with appropriate inherited ACLs, not a shared/public folder. Record nonexistent files rather than creating an empty backup. Keep backup contents out of logs and the repository. If verification fails, revert only this run's changed settings; restore a whole backup only when it is still safe against later edits. A Magpie saved profile spans multiple agents, so do not apply one as a narrow rollback without checking its scope.

## Recovery

| Symptom | Action |
| --- | --- |
| `magpie` not found | Locate app/CLI and use its full path; do not reinstall solely to fix PATH |
| Missing Linux GUI runtime | Use installed CLI with `web`/TUI when suitable; offer verified distro runtime packages if desktop is desired |
| Missing/incompatible Node or `tar` | Read runtime error; allow plugin-managed Node download; check `tar`; validate an explicitly configured `managed.nodePath` rather than silently replacing it |
| Download, proxy, permission or checksum error | Identify the failing component/host; fix network or writable data location; preserve checksum checks; never execute a mismatched file |
| Node/channel downloads fail | Fix the identified cause, then restart/reload the same host and plugin to retry; retain source and account data |
| EAC-only failure | Check authorization and EAC diagnostics; available anonymous/account channels can remain usable; do not bypass authorization or rewrite upstream endpoints |
| Management link expired/refused | Keep the host alive and generate a fresh full `/open/...` URL; never reuse consumed links |
| Remote `127.0.0.1` fails | Explain which machine owns localhost; choose remote console or documented SSH forwarding; do not expose model API publicly |
| Cloudflare DNS/startup delay | Allow the documented one-to-two-minute initial propagation; retry a page after waiting, not repeated tunnel creation; use SSH forwarding if the supported tunnel route fails |
| Models absent or rate-limited | Refresh and check enabled channel/model/account and quota; respect Retry-After; report unavailable state instead of paid fallback |

Retry a failed stage at most twice after correcting an identified cause; an unchanged failure requires reporting, not a loop. If a checksum/source mismatch, unsupported architecture, authorization failure or destructive replacement is involved, stop that operation immediately. Repair does not mean uninstall: removal can delete accounts and runtime data. Preserve successful prior stages and give a resumable next step.
