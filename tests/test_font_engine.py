from pathlib import Path

import pytest

from app.core.compatibility import check_compatibility
from app.core.variable_font_builder import build_weight_variable_font


def test_empty_collection_is_not_compatible() -> None:
    report = check_compatibility([])
    assert not report.compatible
    assert report.problems


def test_builder_requires_two_masters(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="At least two"):
        build_weight_variable_font(["one.ttf"], [400], "Test", tmp_path / "Test.ttf")
