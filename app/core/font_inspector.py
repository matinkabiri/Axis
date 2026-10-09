from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from fontTools.ttLib import TTFont


WEIGHT_NAMES = {
    100: "Thin",
    200: "ExtraLight",
    300: "Light",
    400: "Regular",
    500: "Medium",
    600: "SemiBold",
    700: "Bold",
    800: "ExtraBold",
    900: "Black",
}


@dataclass(frozen=True)
class FontMetadata:
    path: Path
    family_name: str
    subfamily_name: str
    postscript_name: str
    weight: int
    italic: bool
    glyph_count: int
    glyph_names: frozenset[str]


def _name(font: TTFont, name_id: int, fallback: str) -> str:
    names = font["name"].names if "name" in font else []
    for record in names:
        if record.nameID != name_id:
            continue
        try:
            return record.toUnicode()
        except UnicodeDecodeError:
            continue
    return fallback


def inspect_font(path: str | Path) -> FontMetadata:
    source = Path(path)
    with TTFont(source, lazy=True) as font:
        weight = 400
        if "OS/2" in font:
            weight = int(font["OS/2"].usWeightClass or 400)
        italic = False
        if "OS/2" in font:
            italic = bool(font["OS/2"].fsSelection & 0x01)
        if "head" in font:
            italic = italic or bool(font["head"].macStyle & 0x02)
        glyph_names = frozenset(font.getGlyphOrder())
        return FontMetadata(
            path=source,
            family_name=_name(font, 1, source.stem),
            subfamily_name=_name(font, 2, "Regular"),
            postscript_name=_name(font, 6, source.stem),
            weight=weight,
            italic=italic,
            glyph_count=len(glyph_names),
            glyph_names=glyph_names,
        )


def weight_label(value: int) -> str:
    return WEIGHT_NAMES.get(value, str(value))
