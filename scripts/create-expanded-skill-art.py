#!/usr/bin/env python3
"""Build original, transparent skill art for the 150 expanded characters.

Each character requires its own AI source strip, except Mario's three original
object illustrations. Missing sources fail the build rather than reusing art.
The original 100 character sheets are never touched.
"""
from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public/assets"
SOURCES = ROOT / "assets/ai-source/skills"
SIZE, CELL, MARGIN, GUTTER = 128, 160, 8, 8


def roster() -> list[dict]:
    code = ("import {characters} from './src/data/characters.ts';"
            "console.log(JSON.stringify(characters.map(c=>({id:c.id,name:c.name,color:c.color,"
            "universe:c.universe,skills:c.skills.map(s=>({id:s.id,name:s.name,"
            "description:s.description,icon:s.icon,effects:s.effects}))}))))")
    result = subprocess.run(['node', '--import', 'tsx', '--input-type=module', '-e', code],
                            cwd=ROOT, check=True, capture_output=True, text=True)
    return json.loads(result.stdout)


def jumping_flower_star(index: int) -> Image.Image:
    """Object-only art for three moves whose dedicated generation was unavailable."""
    canvas=Image.new('RGBA',(512,512));layer=Image.new('RGBA',(512,512))
    d=ImageDraw.Draw(layer)
    if index==0:
        d.polygon([(196,75),(298,75),(306,284),(386,319),(427,383),(406,423),
                   (113,423),(80,389),(96,348),(188,307)],fill=(196,35,39,245),outline=(255,211,119,255),width=13)
        d.polygon([(192,110),(302,110),(304,177),(190,177)],fill=(255,245,225,255))
        d.rounded_rectangle((116,362,405,406),14,fill=(84,44,50,255))
        for x in (145,201,257,313,369):d.line((x,379,x+24,395),fill=(255,221,128,250),width=8)
        d.arc((121,100,429,433),178,271,fill=(75,192,255,255),width=15)
    elif index==1:
        d.line((253,304,255,447),fill=(55,183,88,255),width=30)
        d.polygon([(243,368),(120,306),(169,414),(252,407)],fill=(46,189,76,245))
        d.polygon([(265,390),(389,311),(361,428),(263,421)],fill=(60,218,94,245))
        for i in range(7):
            a=math.tau*i/7;x=255+106*math.cos(a);y=209+106*math.sin(a)
            d.ellipse((x-80,y-80,x+80,y+80),fill=(241,75,47,245),outline=(255,198,76,250),width=9)
        d.ellipse((203,157,307,261),fill=(255,212,43,255),outline=(255,251,171,255),width=13)
        d.ellipse((239,191,272,224),fill=(197,77,27,255))
    else:
        points=[]
        for i in range(10):
            a=-math.pi/2+i*math.pi/5;r=193 if i%2==0 else 91
            points.append((256+r*math.cos(a),256+r*math.sin(a)))
        d.polygon(points,fill=(255,197,44,255),outline=(255,250,169,255),width=15)
        d.ellipse((219,190,278,248),fill=(255,247,196,195))
        for i in range(10):
            a=math.tau*i/10;x,y=256+226*math.cos(a),256+226*math.sin(a)
            d.ellipse((x-5,y-5,x+5,y+5),fill=(255,241,134,220))
    shadow=Image.new('RGBA',(512,512),(255,137,43,0))
    shadow.putalpha(layer.getchannel('A').filter(ImageFilter.GaussianBlur(28)).point(lambda n:int(n*.52)))
    canvas.alpha_composite(shadow);canvas.alpha_composite(layer)
    return canvas.resize((SIZE,SIZE),Image.Resampling.LANCZOS)


def from_source(path: Path, column: int) -> Image.Image:
    source=Image.open(path).convert('RGBA')
    x0=round(column*source.width/3);x1=round((column+1)*source.width/3)
    segment=source.crop((x0,0,x1,source.height))
    alpha=segment.getchannel('A').point(lambda value: 0 if value<12 else value)
    segment.putalpha(alpha)
    bbox=segment.getbbox()
    if not bbox: raise ValueError(f'Empty AI icon {path}, column {column}')
    segment=segment.crop(bbox)
    segment.thumbnail((SIZE-4,SIZE-4),Image.Resampling.LANCZOS)
    icon=Image.new('RGBA',(SIZE,SIZE))
    icon.alpha_composite(segment,((SIZE-segment.width)//2,(SIZE-segment.height)//2))
    return icon


def main() -> None:
    characters=roster()
    assert len(characters)==250
    icon_path=PUBLIC/'skills/manifest.json';sheet_path=PUBLIC/'sheets/skills/manifest.json'
    icons=json.loads(icon_path.read_text());sheets=json.loads(sheet_path.read_text())
    original={p['character'] for p in sheets['pages'] if not p.get('placeholder') and p['character'] in {c['id'] for c in characters[:100]}}
    assert len(original)==100, 'The original 100 AI sheets must remain intact.'
    skill_records={(item['character'],item['id']):item for item in icons['skills']}
    pages={page['character']:page for page in sheets['pages']}
    ai=0
    for c in characters[100:]:
        source=SOURCES/f"{c['id']}.png"
        if not source.exists() and c['id']!='mario':
            raise FileNotFoundError(f'Missing original AI art for {c["name"]}: {source}')
        source_size=Image.open(source).size if source.exists() else None
        if source_size: ai+=1
        sheet=Image.new('RGBA',(512,176))
        records=[]
        for col,skill in enumerate(c['skills']):
            art=from_source(source,col) if source.exists() else jumping_flower_star(col)
            assert art.getchannel('A').getpixel((0,0))==0
            target=PUBLIC/'skills'/c['id']/f"{skill['id']}.png"
            target.parent.mkdir(parents=True,exist_ok=True);art.save(target,optimize=True)
            x=MARGIN+col*(CELL+GUTTER)+(CELL-SIZE)//2
            sheet.alpha_composite(art,(x,MARGIN+(CELL-SIZE)//2))
            path=f"/assets/skills/{c['id']}/{skill['id']}.png"
            record={'id':skill['id'],'character':c['id'],'name':skill['name'],'path':path,
                    'sheet':f"/assets/sheets/skills/pages/{c['id']}.png",'row':0,'column':col,
                    'crop':{'x':x,'y':MARGIN+(CELL-SIZE)//2,'width':SIZE,'height':SIZE},
                    'cell':{'x':MARGIN+col*(CELL+GUTTER),'y':MARGIN,'width':CELL,'height':CELL},
                    'sourceCrop':{'x':round(col*source_size[0]/3),'y':0,'width':round(source_size[0]/3),'height':source_size[1]} if source_size else {'x':0,'y':0,'width':CELL,'height':CELL},
                    'artMethod':'AI sheet' if source.exists() else 'object illustration'}
            records.append(record);skill_records[(c['id'],skill['id'])]=record
        sheet_target=PUBLIC/'sheets/skills/pages'/f"{c['id']}.png"
        sheet.save(sheet_target,optimize=True)
        pages[c['id']]={'character':c['id'],'sourceSheet':f"/assets/sheets/skills/pages/{c['id']}.png",
                        'sheet':f"/assets/sheets/skills/pages/{c['id']}.png",
                        'sourceResolution':list(source_size) if source_size else [512,176],
                        'category':'skills','format':'PNG RGBA','resolution':[512,176],
                        'columns':3,'rows':1,'cell':[CELL,CELL],'gutter':GUTTER,'margin':MARGIN,
                        'icons':records,'artMethod':'AI sheet' if source.exists() else 'object illustration'}
    icons['skills']=[skill_records[(c['id'],s['id'])] for c in characters for s in c['skills']]
    icons['count']=len(icons['skills'])
    sheets['pages']=[pages[c['id']] for c in characters]
    sheets['icons']=[item for page in sheets['pages'] for item in page['icons']]
    sheets['count']=len(sheets['icons'])
    icon_path.write_text(json.dumps(icons,ensure_ascii=False,indent=2)+'\n')
    sheet_path.write_text(json.dumps(sheets,ensure_ascii=False,indent=2)+'\n')
    objects=int(not (SOURCES/'mario.png').exists())
    assert ai==149 and objects==1
    print(f'Built 150 character sheets / 450 original icons ({ai} AI sheets, {objects} illustrated object sheet).')


if __name__=='__main__': main()
