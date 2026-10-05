#!/usr/bin/env python3
"""Crop transparent AI sprite sheets into standardized Nexus Trios game assets."""
from __future__ import annotations

import json
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SHEETS = PUBLIC / "assets" / "sheets"
SOURCES = ROOT / "assets" / "ai-source"
CELL = 160
ICON = 128
GUTTER = 8
MARGIN = 8


def load_rgba(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(f"Missing AI source sheet: {path}")
    image = Image.open(path)
    if image.mode != "RGBA":
        raise ValueError(f"Sheet lacks an RGBA alpha channel: {path}")
    return image


def alpha_clean(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    alpha = image.getchannel("A").point(lambda value: 0 if value < 10 else value)
    image.putalpha(alpha)
    return image


def square_cell(sheet: Image.Image, columns: int, rows: int, row: int, column: int) -> tuple[Image.Image, dict[str, int]]:
    width, height = sheet.size
    x0, x1 = round(column * width / columns), round((column + 1) * width / columns)
    y0, y1 = round(row * height / rows), round((row + 1) * height / rows)
    source = sheet.crop((x0, y0, x1, y1))
    side = min(source.size)
    left = (source.width - side) // 2
    top = (source.height - side) // 2
    source = alpha_clean(source.crop((left, top, left + side, top + side)))
    return source, {"x": x0 + left, "y": y0 + top, "width": side, "height": side}


def final_cell(source: Image.Image) -> Image.Image:
    image = source.resize((ICON, ICON), Image.Resampling.LANCZOS)
    cell = Image.new("RGBA", (CELL, CELL), (0, 0, 0, 0))
    cell.alpha_composite(image, ((CELL - ICON) // 2, (CELL - ICON) // 2))
    return cell


def sheet_geometry(columns: int, rows: int) -> tuple[int, int]:
    return (2 * MARGIN + columns * CELL + (columns - 1) * GUTTER,
            2 * MARGIN + rows * CELL + (rows - 1) * GUTTER)


def place(sprite: Image.Image, icon: Image.Image, row: int, column: int) -> tuple[int, int]:
    x = MARGIN + column * (CELL + GUTTER)
    y = MARGIN + row * (CELL + GUTTER)
    sprite.alpha_composite(icon, (x, y))
    return x + (CELL - ICON) // 2, y + (CELL - ICON) // 2


def assert_transparent(path: Path) -> None:
    image = Image.open(path)
    if image.mode != "RGBA" or image.getchannel("A").getextrema()[0] != 0:
        raise ValueError(f"Export is not genuinely transparent: {path}")
    alpha = image.getchannel("A")
    points = [(0, 0), (image.width - 1, 0), (0, image.height - 1), (image.width - 1, image.height - 1)]
    if any(alpha.getpixel(point) != 0 for point in points):
        raise ValueError(f"Nontransparent corner/halo remains: {path}")


def main() -> None:
    manifest_path = PUBLIC / "assets" / "skills" / "manifest.json"
    skills = json.loads(manifest_path.read_text(encoding="utf-8"))["skills"]
    skill_pages = []
    packed_skills = []
    for character in sorted({item["character"] for item in skills}):
        source_path = SOURCES / "skills" / f"{character}.png"
        source = load_rgba(source_path)
        if source.width / source.height < 2.9:
            raise ValueError(f"Skill sheet should be a 3:1 strip: {source_path} {source.size}")
        items = [item for item in skills if item["character"] == character]
        if len(items) != 3:
            raise ValueError(f"Expected 3 skills for {character}, got {len(items)}")
        fw, fh = sheet_geometry(3, 1)
        output = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
        entries = []
        for column, item in enumerate(items):
            source_icon, source_crop = square_cell(source, 3, 1, 0, column)
            icon = final_cell(source_icon)
            x, y = place(output, icon, 0, column)
            individual = Path(item["path"].replace(".svg", ".png").lstrip("/"))
            destination = PUBLIC / individual
            destination.parent.mkdir(parents=True, exist_ok=True)
            icon.crop(((CELL - ICON) // 2, (CELL - ICON) // 2,
                       (CELL + ICON) // 2, (CELL + ICON) // 2)).save(destination)
            assert_transparent(destination)
            record = {**item, "path": "/" + str(individual).replace("\\", "/"),
                      "sheet": f"/assets/sheets/skills/pages/{character}.png", "row": 0, "column": column,
                      "cell": {"x": MARGIN + column * (CELL + GUTTER), "y": MARGIN, "width": CELL, "height": CELL},
                      "sourceCrop": source_crop,
                      "crop": {"x": x, "y": y, "width": ICON, "height": ICON}}
            entries.append(record)
            packed_skills.append(record)
        page_path = SHEETS / "skills" / "pages" / f"{character}.png"
        page_path.parent.mkdir(parents=True, exist_ok=True)
        output.save(page_path)
        assert_transparent(page_path)
        skill_pages.append({"character": character, "sourceSheet": f"/assets/sheets/skills/pages/{character}.png",
                            "sourceResolution": list(source.size), "sheet": f"/assets/sheets/skills/pages/{character}.png",
                            "category": "skills", "format": "PNG RGBA", "resolution": [fw, fh],
                            "columns": 3, "rows": 1, "cell": [CELL, CELL], "gutter": GUTTER,
                            "margin": MARGIN, "icons": entries})
    packed_skills.sort(key=lambda item: (item["character"], item["column"]))
    (SHEETS / "skills" / "manifest.json").write_text(json.dumps({
        "category": "character-skills", "format": "PNG RGBA", "cell": [CELL, CELL],
        "exportedIcon": [ICON, ICON], "gutter": GUTTER, "margin": MARGIN,
        "count": len(packed_skills), "pages": skill_pages, "icons": packed_skills
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps({"count": len(packed_skills), "skills": packed_skills},
                                        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    status_ids = ["exposed", "paralyzed", "protected", "marked", "slow", "haste", "confused", "rooted",
                  "regen", "burning", "electric", "silenced", "strengthened", "weakened"]
    status_names = {"exposed": "Exposto", "paralyzed": "Paralisado", "protected": "Protegido", "marked": "Marcado",
                    "slow": "Lento", "haste": "Acelerado", "confused": "Confuso", "rooted": "Preso",
                    "regen": "Regeneração", "burning": "Queimando", "electric": "Eletrificado", "silenced": "Silenciado",
                    "strengthened": "Fortalecido", "weakened": "Enfraquecido"}
    auxiliary_ids = ["ready", "cooldown", "charging", "preparing", "executing", "buff", "debuff", "tempo-up",
                     "tempo-down", "interrupt", "history", "inspect", "help", "domain", "victory", "defeat"]
    auxiliary_names = {"ready": "Habilidade pronta", "cooldown": "Cooldown", "charging": "Carregando",
                       "preparing": "Preparando", "executing": "Executando", "buff": "Buff", "debuff": "Debuff",
                       "tempo-up": "Ação acelerada", "tempo-down": "Ação atrasada", "interrupt": "Interrupção",
                       "history": "Histórico", "inspect": "Inspeção", "help": "Ajuda", "domain": "Domínio",
                       "victory": "Vitória", "defeat": "Derrota"}
    for category, ids, columns, rows, source_path, out_dir, output_sheet in [
        ("statuses", status_ids, 4, 4, SOURCES / "statuses.png", PUBLIC / "assets" / "statuses", SHEETS / "statuses.png"),
        ("ui", auxiliary_ids, 4, 4, SOURCES / "ui.png", PUBLIC / "assets" / "ui", SHEETS / "ui.png")]:
        source = load_rgba(source_path)
        fw, fh = sheet_geometry(columns, rows)
        output = Image.new("RGBA", (fw, fh), (0, 0, 0, 0))
        records = []
        for index, item_id in enumerate(ids):
            row, column = divmod(index, columns)
            source_icon, source_crop = square_cell(source, columns, rows, row, column)
            icon = final_cell(source_icon)
            x, y = place(output, icon, row, column)
            path = out_dir / f"{item_id}.png"
            path.parent.mkdir(parents=True, exist_ok=True)
            icon.crop(((CELL - ICON) // 2, (CELL - ICON) // 2,
                       (CELL + ICON) // 2, (CELL + ICON) // 2)).save(path)
            assert_transparent(path)
            labels = status_names if category == "statuses" else auxiliary_names
            records.append({"id": item_id, "name": labels[item_id], "path": "/" + str(path.relative_to(PUBLIC)).replace("\\", "/"),
                            "row": row, "column": column,
                            "cell": {"x": MARGIN + column * (CELL + GUTTER), "y": MARGIN + row * (CELL + GUTTER), "width": CELL, "height": CELL},
                            "sourceCrop": source_crop, "crop": {"x": x, "y": y, "width": ICON, "height": ICON}})
        output.save(output_sheet)
        assert_transparent(output_sheet)
        sheet_manifest = {"category": category, "sourceSheet": "/" + str(output_sheet.relative_to(PUBLIC)).replace("\\", "/"),
                          "sourceResolution": list(source.size), "format": "PNG RGBA",
                          "resolution": [fw, fh], "columns": columns, "rows": rows,
                          "cell": [CELL, CELL], "gutter": GUTTER, "margin": MARGIN,
                          "count": len(records), "items": records}
        (SHEETS / category / "manifest.json").parent.mkdir(parents=True, exist_ok=True)
        (SHEETS / category / "manifest.json").write_text(json.dumps(sheet_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # AI PNG exports replace the previous generated SVG icon assets.
    for svg in (PUBLIC / "assets" / "skills").rglob("*.svg"):
        svg.unlink()
    print(f"Packed {len(packed_skills)} transparent skill icons, {len(status_ids)} statuses and {len(auxiliary_ids)} HUD icons.")


if __name__ == "__main__":
    main()
