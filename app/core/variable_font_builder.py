from __future__ import annotations

from pathlib import Path

from fontTools.designspaceLib import AxisDescriptor, DesignSpaceDocument, SourceDescriptor
from fontTools.varLib import build


def build_weight_variable_font(
    source_paths: list[str | Path],
    weights: list[int],
    family_name: str,
    output_path: str | Path,
) -> None:
    if len(source_paths) != len(weights) or len(source_paths) < 2:
        raise ValueError("At least two source fonts and one weight per source are required.")
    if len(set(weights)) != len(weights):
        raise ValueError("Each source font must have a unique Weight value.")

    axis = AxisDescriptor()
    axis.name = "Weight"
    axis.tag = "wght"
    axis.minimum = min(weights)
    axis.default = 400 if 400 in weights else weights[len(weights) // 2]
    axis.maximum = max(weights)

    document = DesignSpaceDocument()
    document.addAxis(axis)
    for index, (path, weight) in enumerate(zip(source_paths, weights)):
        source = SourceDescriptor()
        source.name = f"master-{index + 1}"
        source.path = str(Path(path).resolve())
        source.familyName = family_name
        source.styleName = "Regular"
        source.location = {"Weight": weight}
        document.addSource(source)

    document_path = Path(output_path).with_suffix(".designspace")
    document_path.parent.mkdir(parents=True, exist_ok=True)
    document.write(document_path)
    font, _, _ = build(document_path)
    font.save(output_path)
