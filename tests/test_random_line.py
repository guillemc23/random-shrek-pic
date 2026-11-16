import importlib.util
from pathlib import Path


def _load_module():
    spec = importlib.util.spec_from_file_location("main_mod", Path("main.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_single_line_no_newline(tmp_path):
    mod = _load_module()
    p = tmp_path / "single.txt"
    p.write_text("http://example.com/pic\n", encoding="utf-8")
    assert mod.random_line(p) == "http://example.com/pic"


def test_multiple_lines_stripped(tmp_path):
    mod = _load_module()
    p = tmp_path / "multi.txt"
    lines = ["a\n", "b\n", "c\n"]
    p.write_text("".join(lines), encoding="utf-8")
    result = mod.random_line(p)
    assert result in [l.strip() for l in lines]
    # ensure no newline/carriage return characters remain
    assert "\n" not in result
    assert "\r" not in result


def test_crlf_line(tmp_path):
    mod = _load_module()
    p = tmp_path / "crlf.txt"
    # write CRLF explicitly as bytes
    p.write_bytes(b"http://example.com/pic\r\n")
    assert mod.random_line(p) == "http://example.com/pic"


def test_empty_file_returns_none(tmp_path):
    mod = _load_module()
    p = tmp_path / "empty.txt"
    p.write_text("", encoding="utf-8")
    import pytest

    with pytest.raises(ValueError):
        mod.random_line(p)
