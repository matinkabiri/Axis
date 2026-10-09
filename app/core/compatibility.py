from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fontTools.ttLib import TTFont

from app.core.font_inspector import FontMetadata, inspect_font


@dataclass(frozen=True)
class CompatibilityReport:
    compatible: bool
    shortest_path: Path | None
    shared_glyphs: frozenset[str]
    problems: tuple[str, ...]


def check_compatibility(paths: list[str | Path]) -> CompatibilityReport:
    if not paths:
        return CompatibilityReport(False, None, frozenset(), ("No fonts were selected.",))
    metadata = [inspect_font(path) for path in paths]
    shortest = min(metadata, key=lambda item: item.glyph_count)
    shared = frozenset.intersection(*(item.glyph_names for item in metadata))
    problems: list[str] = []
    if len({item.glyph_names for item in metadata}) > 1:
        problems.append("The source fonts do not contain matching glyph sets.")
    if len(shared) < 2:
        problems.append("The fonts do not share enough glyphs to build a variable font.")
    if len({item.family_name for item in metadata}) > 1:
        problems.append("The source fonts belong to different families.")
    if not _same_outline_order(paths):
        problems.append("The source fonts have different glyph orderings.")
    problems.extend(_outline_problems(paths))
    return CompatibilityReport(not problems, shortest.path, shared, tuple(problems))


def _same_outline_order(paths: list[str | Path]) -> bool:
    if not paths:
        return True
    orders: list[tuple[str, ...]] = []
    for path in paths:
        with TTFont(path, lazy=True) as font:
            orders.append(tuple(font.getGlyphOrder()))
    return len(set(orders)) == 1


def _outline_problems(paths: list[str | Path]) -> list[str]:
    """Catch common TrueType interpolation failures before varLib runs."""
    fonts = [TTFont(path, lazy=True) for path in paths]
    try:
        if not all("glyf" in font for font in fonts):
            return []
        glyphs = set(fonts[0].getGlyphOrder())
        for font in fonts[1:]:
            glyphs.intersection_update(font.getGlyphOrder())
        incompatible = []
        for glyph_name in sorted(glyphs):
            signatures = []
            for font in fonts:
                glyph = font["glyf"][glyph_name]
                if glyph.isComposite():
                    signature = ("composite", tuple(component.glyphName for component in glyph.components))
                else:
                    coordinates, end_points, flags = glyph.getCoordinates(font["glyf"])
                    signature = ("outline", len(coordinates), tuple(end_points), tuple(flags))
                signatures.append(signature)
            if len(set(signatures)) > 1:
                incompatible.append(glyph_name)
        if incompatible:
            preview = ", ".join(incompatible[:5])
            suffix = "..." if len(incompatible) > 5 else ""
            return [f"{len(incompatible)} glyph outlines are not compatible ({preview}{suffix})."]
        return []
    finally:
        for font in fonts:
            font.close()


def trim_to_shared_glyphs(source: str | Path, destination: str | Path, shared_glyphs: frozenset[str]) -> None:
    """Write a copy containing the shared glyph set.

    This is intentionally separate from compatibility checking: trimming glyphs can
    solve a glyph-set mismatch, but it cannot repair incompatible outlines.
    """
    from fontTools.subset import Options, Subsetter

    with TTFont(source) as font:
        options = Options()
        options.recalc_average_width = False
        subsetter = Subsetter(options=options)
        subsetter.populate(glyphs=sorted(shared_glyphs))
        subsetter.subset(font)
        font.save(destination)
