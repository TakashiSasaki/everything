import os
import sys
import ctypes
import pytest


PKG_DLL = os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "pyeverything", "bin", "Everything64.dll"
))


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only integration test")
def test_dll_file_exists_in_package_bin():
    assert os.path.isfile(PKG_DLL), (
        "Everything64.dll not found in package bin. Expected at: " + PKG_DLL
    )


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only integration test")
def test_dll_loads_and_bindings_ok():
    if not os.path.isfile(PKG_DLL):
        pytest.skip("Everything64.dll missing; skipping load test")

    from pyeverything.dll import load_everything_dll, init_functions, verify_dll_bindings

    dll = load_everything_dll()
    assert isinstance(dll, ctypes.WinDLL)

    init_functions(dll)
    ok, missing = verify_dll_bindings(dll)
    if not ok:
        pytest.fail("Missing DLL exports: " + ", ".join(missing))


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only integration test")
def test_ipc_available_or_skip():
    if not os.path.isfile(PKG_DLL):
        pytest.skip("Everything64.dll missing; skipping IPC test")

    from pyeverything.dll import load_everything_dll, init_functions
    dll = load_everything_dll()
    init_functions(dll)

    # Probe IPC via a lightweight call
    _ = dll.Everything_IsDBLoaded()
    last_error = dll.Everything_GetLastError()

    EVERYTHING_ERROR_IPC = 2
    if last_error == EVERYTHING_ERROR_IPC:
        pytest.skip("Everything IPC not available; ensure Everything is running")

    # If IPC is available, call should succeed with 0 or non-zero
    assert last_error == 0


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only integration test")
def test_version_info_when_ipc_available():
    if not os.path.isfile(PKG_DLL):
        pytest.skip("Everything64.dll missing; skipping version test")

    from pyeverything.dll import load_everything_dll, init_functions
    dll = load_everything_dll()
    init_functions(dll)

    major = dll.Everything_GetMajorVersion()
    minor = dll.Everything_GetMinorVersion()
    revision = dll.Everything_GetRevision()
    build = dll.Everything_GetBuildNumber()
    last_error = dll.Everything_GetLastError()

    EVERYTHING_ERROR_IPC = 2
    if (major == 0 or build == 0) and last_error == EVERYTHING_ERROR_IPC:
        pytest.skip("Everything IPC not available; cannot read version info")

    assert major > 0
    assert minor >= 0
    assert revision >= 0
    assert build > 0

