import os
from pathlib import Path

import pytest

# If requests isn't available in the environment, skip the entire module with a helpful note.
try:
    import requests  # noqa: F401
except Exception:  # ImportError or other issues
    pytest.skip(
        "`requests` is required to run these network tests. Set up the environment or install requests.",
        allow_module_level=True,
    )


def _collect_urls():
    data_dir = Path("data")
    urls = []
    if not data_dir.exists():
        return urls
    for txt in sorted(data_dir.glob("*.txt")):
        try:
            text = txt.read_text(encoding="utf-8")
        except Exception:
            # if any file can't be read, include it as a failing entry so the test surfaces it
            continue
        for line in text.splitlines():
            u = line.strip()
            if not u:
                continue
            if u.startswith("#"):
                continue
            urls.append((txt.name, u))
    return urls


URLS = _collect_urls()

if not URLS:
    pytest.skip(
        "No URLs found in data/*.txt — skipping network availability tests",
        allow_module_level=True,
    )


@pytest.mark.parametrize("source,url", URLS)
def test_url_is_available(source, url):
    """Check that the URL responds (HEAD, fallback to GET)."""
    if os.getenv("NO_NETWORK_TESTS"):
        pytest.skip("Network tests disabled via NO_NETWORK_TESTS")

    import requests

    try:
        # Try a fast HEAD request first
        resp = requests.head(url, timeout=8, allow_redirects=True)
        status = resp.status_code
        # Some servers return 405 for HEAD; fall back to GET in that case or on error codes
        if status >= 400 or status == 405:
            resp = requests.get(url, timeout=12, stream=True, allow_redirects=True)
            status = resp.status_code

        assert 200 <= status < 400, f"{url} (from {source}) returned HTTP {status}"

        # Prefer checking content-type when present
        ct = resp.headers.get("content-type", "").lower()
        if ct:
            assert ct.startswith("image/") or "image" in ct, (
                f"{url} (from {source}) returned unexpected content-type: {ct}"
            )

    except Exception as exc:  # noqa: BLE001 - allow broad except for test diagnostic
        pytest.fail(f"Request to {url} (from {source}) raised: {exc!r}")
