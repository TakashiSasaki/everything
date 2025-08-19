import json
import os
import types

import builtins

import importlib


class _Fn:
    """Function-like stub that accepts argtypes/restype and is callable."""

    def __init__(self, func=None, default=None):
        self.argtypes = None
        self.restype = None
        self._func = func
        self._default = default

    def __call__(self, *args, **kwargs):
        if self._func is not None:
            return self._func(*args, **kwargs)
        return self._default


class _SearchFakeDLL:
    """Minimal Everything DLL fake with result data."""

    def __init__(self, paths):
        self.paths = list(paths)
        self.state = {}
        self.cleaned = False
        self._fns = {}

        # Set up specific functions used by EverythingDLL.search
        self._fns["Everything_SetSearchW"] = _Fn(lambda q: self.state.__setitem__("query", q) or None)
        self._fns["Everything_SetMatchPath"] = _Fn(lambda b: self.state.__setitem__("match_path", bool(b)) or None)
        self._fns["Everything_SetRequestFlags"] = _Fn(lambda f: self.state.__setitem__("flags", int(f)) or None)
        self._fns["Everything_SetOffset"] = _Fn(lambda o: self.state.__setitem__("offset", int(o)) or None)
        self._fns["Everything_SetMax"] = _Fn(lambda m: self.state.__setitem__("max", int(m)) or None)
        self._fns["Everything_QueryW"] = _Fn(lambda *_: True, default=True)
        self._fns["Everything_GetNumResults"] = _Fn(lambda: len(self.paths), default=len(self.paths))

        def _fullpath(i, buf, n):
            buf.value = self.paths[int(i)]
            return len(buf.value)

        self._fns["Everything_GetResultFullPathNameW"] = _Fn(_fullpath)

        def _size(i, p):
            # leave default 0
            return True

        self._fns["Everything_GetResultSize"] = _Fn(_size, default=True)
        self._fns["Everything_CleanUp"] = _Fn(lambda: self._set_cleaned())

    def _set_cleaned(self):
        self.cleaned = True
        return None

    def __getattr__(self, name):
        fn = self._fns.get(name)
        if fn is None:
            fn = _Fn(default=None)
            self._fns[name] = fn
        return fn


def test_guard_non_windows(monkeypatch):
    monkeypatch.setattr(__import__("sys"), "platform", "linux", raising=False)
    dll_class = importlib.import_module("pyeverything.dll_class")
    with __import__("pytest").raises(RuntimeError):
        dll_class.EverythingDLL()


def test_loader_prefers_package_bin(monkeypatch):
    sys = __import__("sys")
    monkeypatch.setattr(sys, "platform", "win32", raising=False)

    dll_class = importlib.import_module("pyeverything.dll_class")
    pkg_bin = os.path.join(os.path.dirname(dll_class.__file__), "bin", "Everything64.dll")

    # Only package bin exists
    def fake_isfile(p):
        return p == pkg_bin

    monkeypatch.setattr(__import__("os.path"), "isfile", fake_isfile, raising=False)

    called = {}

    def fake_WinDLL(path):
        called["path"] = path
        # return a permissive fake that accepts binding
        return _SearchFakeDLL(paths=[])  # no search used in this test

    monkeypatch.setattr(__import__("ctypes"), "WinDLL", fake_WinDLL, raising=False)

    client = dll_class.EverythingDLL()
    assert called.get("path") == pkg_bin
    assert hasattr(client, "dll")


def test_search_minimal_fields(monkeypatch):
    sys = __import__("sys")
    monkeypatch.setattr(sys, "platform", "win32", raising=False)

    dll_class = importlib.import_module("pyeverything.dll_class")
    pkg_bin = os.path.join(os.path.dirname(dll_class.__file__), "bin", "Everything64.dll")
    monkeypatch.setattr(__import__("os.path"), "isfile", lambda p: p == pkg_bin, raising=False)

    paths = [
        r"C:\\Windows\\System32\\drivers\\etc\\hosts",
        r"C:\\Temp\\file.txt",
    ]

    def fake_WinDLL(path):
        return _SearchFakeDLL(paths)

    monkeypatch.setattr(__import__("ctypes"), "WinDLL", fake_WinDLL, raising=False)

    client = dll_class.EverythingDLL()
    res = client.search("dummy", count=10, all_fields=False)
    assert isinstance(res, list)
    assert len(res) == 2
    assert res[0]["path"] == paths[0]
    assert res[0]["name"] == os.path.basename(paths[0])
    assert res[0]["size"] == 0  # our fake leaves size as default 0


def test_cli_json_output(monkeypatch, capsys):
    sys = __import__("sys")
    monkeypatch.setattr(sys, "platform", "win32", raising=False)

    dll_class = importlib.import_module("pyeverything.dll_class")
    pkg_bin = os.path.join(os.path.dirname(dll_class.__file__), "bin", "Everything64.dll")
    monkeypatch.setattr(__import__("os.path"), "isfile", lambda p: p == pkg_bin, raising=False)

    paths = [r"C:\\Foo\\Bar.txt"]

    def fake_WinDLL(path):
        return _SearchFakeDLL(paths)

    monkeypatch.setattr(__import__("ctypes"), "WinDLL", fake_WinDLL, raising=False)

    dll_class.main(["--search", "Bar.txt", "--json", "--count", "5"])
    out = capsys.readouterr().out.strip()
    data = json.loads(out)
    assert isinstance(data, list)
    assert data and data[0]["path"].endswith("Bar.txt")
