import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "preflight", Path(__file__).parents[1] / "scripts/preflight.py")
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)


class HostSelectionTests(unittest.TestCase):
    def test_windows_emulated_process_uses_native_arm(self):
        report = preflight.describe_host("Windows", "AMD64", {
            "PROCESSOR_ARCHITEW6432": "ARM64",
            "PROCESSOR_ARCHITECTURE": "AMD64"}, "")
        self.assertEqual(report["release_arch"], "arm64")

    def test_rosetta_uses_native_arm(self):
        report = preflight.describe_host("Darwin", "x86_64", {}, "", mac_arm=True)
        self.assertEqual(report["release_arch"], "arm64")

    def test_unknown_arch_does_not_default_to_x64(self):
        self.assertIsNone(preflight.normalize_arch("riscv64"))

    def test_wsl_and_remote_are_distinguished(self):
        report = preflight.describe_host("Linux", "aarch64", {
            "SSH_CONNECTION": "present"}, "microsoft-standard-WSL2")
        self.assertTrue(report["wsl"])
        self.assertTrue(report["ssh"])
        self.assertFalse(report["linux_desktop_environment"])


if __name__ == "__main__":
    unittest.main()
