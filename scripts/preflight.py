#!/usr/bin/env python3
"""Read-only host inventory; no network, installs, or credential/config reads."""
import json
import os
import platform
import shutil
import subprocess
from pathlib import Path


def normalize_arch(value):
    return {
        "amd64": "amd64", "x86_64": "amd64", "x64": "amd64",
        "arm64": "arm64", "aarch64": "arm64",
    }.get(value.lower())


def describe_host(system, machine, environ, release, mac_arm=False):
    native = machine
    if system == "Windows":
        native = (environ.get("PROCESSOR_ARCHITEW6432")
                  or environ.get("PROCESSOR_ARCHITECTURE") or machine)
    elif system == "Darwin" and mac_arm:
        native = "arm64"
    return {
        "os": system,
        "process_arch": machine,
        "native_arch": native,
        "release_arch": normalize_arch(native),
        "wsl": system == "Linux" and (
            "microsoft" in release.lower() or bool(environ.get("WSL_DISTRO_NAME"))),
        "ssh": bool(environ.get("SSH_CONNECTION") or environ.get("SSH_TTY")),
        "linux_desktop_environment": system == "Linux" and bool(
            environ.get("DISPLAY") or environ.get("WAYLAND_DISPLAY")),
    }


def inventory():
    system = platform.system()
    mac_arm = False
    if system == "Darwin":
        try:
            result = subprocess.run(
                ["sysctl", "-n", "hw.optional.arm64"], capture_output=True,
                text=True, timeout=5, check=False)
            mac_arm = result.returncode == 0 and result.stdout.strip() == "1"
        except (OSError, subprocess.TimeoutExpired):
            pass
    report = describe_host(system, platform.machine(), os.environ,
                           platform.release(), mac_arm)
    user_dir = Path.home()
    candidates = [user_dir / ".local/bin/magpie"]
    if os.environ.get("MAGPIE_BIN_DIR"):
        candidates.append(Path(os.environ["MAGPIE_BIN_DIR"]) / "magpie")
    if system == "Darwin":
        candidates += [Path("/Applications/magpie.app/Contents/MacOS/magpie"),
                       user_dir / "Applications/magpie.app/Contents/MacOS/magpie"]
    elif system == "Windows" and os.environ.get("LOCALAPPDATA"):
        base = Path(os.environ["LOCALAPPDATA"]) / "Programs/magpie"
        candidates += [base / name for name in (
            "magpie.exe", "magpie-windows-amd64.exe", "magpie-windows-arm64.exe")]
    resolved = shutil.which("magpie")
    if resolved:
        candidates.insert(0, Path(resolved))
    report["magpie_candidates"] = sorted({str(p) for p in candidates if p.is_file()})
    report["broken_magpie_symlinks"] = sorted({
        str(p) for p in candidates if p.is_symlink() and not p.exists()})
    report["tools"] = {name: shutil.which(name) for name in ("git", "curl", "tar")}
    report["notes"] = [
        "Candidates are not proof of a healthy installation; verify with Magpie help/UI.",
        "Confirm the intended host when WSL/SSH is detected; this process may be remote.",
        "Verify OS version, libc and current upstream asset support separately.",
    ]
    return report


if __name__ == "__main__":
    print(json.dumps(inventory(), indent=2, ensure_ascii=False))
