import os
import sys
import ctypes
import pytest


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only integration test")
def test_load_everything_dll_and_get_version():
    # Require packaged 64-bit DLL per repo policy
    pkg_bin = os.path.join(os.path.dirname(__file__), "..", "pyeverything", "bin", "Everything64.dll")
    pkg_bin = os.path.abspath(pkg_bin)
    if not os.path.isfile(pkg_bin):
        pytest.skip("Everything64.dll not found in package bin; skipping")

    from pyeverything.dll import load_everything_dll, init_functions

    dll = load_everything_dll()
    assert isinstance(dll, ctypes.WinDLL)

    # Initialize ctypes signatures
    init_functions(dll)

    # Attempt to get version information
    major = dll.Everything_GetMajorVersion()
    minor = dll.Everything_GetMinorVersion()
    revision = dll.Everything_GetRevision()
    build = dll.Everything_GetBuildNumber()

    # If IPC is not available (Everything not running), tolerate by skipping
    last_error = dll.Everything_GetLastError()
    EVERYTHING_ERROR_IPC = 2
    if any(v == 0 for v in (major, minor, revision, build)) and last_error == EVERYTHING_ERROR_IPC:
        pytest.skip("Everything IPC not available; ensure Everything is running")

    # Otherwise, all version components should be non-zero
    assert major > 0
    assert minor >= 0  # minor can be 0 for early versions
    assert revision >= 0
    assert build > 0

    # Target machine should be one of the known values when IPC is available
    target = dll.Everything_GetTargetMachine()
    if target == 0 and dll.Everything_GetLastError() == EVERYTHING_ERROR_IPC:
        pytest.skip("Everything IPC not available for target machine")
    assert target in (1, 2, 3, 4)

