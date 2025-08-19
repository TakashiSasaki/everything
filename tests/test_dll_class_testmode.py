import pytest

# Local copies of helpers for test-mode behavior simulation.
def build_test_queries(hostfile: str) -> list[str]:
    return [
        hostfile,
        r'path:"\\\\windows\\\\system32\\\\drivers\\\\etc" hosts',
        "windows system32 drivers etc hosts",
    ]


def find_hosts_match(results: list[dict], hostfile: str):
    host_lower = hostfile.lower()
    for e in results:
        p = str(e.get("path", ""))
        if p.lower() == host_lower:
            return e
    tail = r"\windows\system32\drivers\etc\hosts"
    for e in results:
        p = str(e.get("path", "")).lower().replace("/", "\\")
        if tail in p:
            return e
    return None


def test_build_test_queries_order():
    host = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
    q = build_test_queries(host)
    assert q[0] == host
    q1 = q[1].lower()
    assert q1.startswith("path:") and "hosts" in q1
    assert "windows" in q[2].lower()


def test_find_hosts_match_exact():
    host = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
    results = [
        {"path": host, "name": "hosts", "size": 42},
    ]
    m = find_hosts_match(results, host)
    assert m is results[0]


def test_find_hosts_match_tail_drive_agnostic():
    host = r"D:\\Windows\\System32\\drivers\\etc\\hosts"
    results = [
        {"path": r"D:/Windows/System32/drivers/etc/hosts", "name": "hosts", "size": 1},
    ]
    m = find_hosts_match(results, host)
    assert m is results[0]


def test_find_hosts_match_none():
    host = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
    m = find_hosts_match([], host)
    assert m is None
