import mympltools as mt


def test_get_style() -> None:
    assert mt.style._get_style("21.10") == mt.style.mystyle_21_10
