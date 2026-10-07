#!/usr/bin/env python3
"""Build transparent, per-skill art for the 150 expanded characters.

AI source strips in assets/ai-source/skills take precedence. Remaining art
remixes the original detailed icons by move, effect and character palette.
The original 100 character sheets are never touched.
"""
from __future__ import annotations

import colorsys
import hashlib
import json
import math
import random
import re
import subprocess
import unicodedata
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageEnhance, ImageChops

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


MOTIFS = [
    ('sword', r'espada|lamina|lâmina|katana|corte|blade|slash|yamato|masamune|faca|sabre|omnislash|zandatsu|golpe giratorio'),
    ('fist', r'soco|punho|punch|soco|boxe|cqc|chute|combo|marreta|impacto|golpe|fúria|furia'),
    ('gun', r'tiro|arma|pistola|rifle|canhao|canhão|blaster|missil|míssil|bullet|bala|disparo|muni'),
    ('arrow', r'flecha|arco|arrow|dardo|lança|lanca|spear|tridente'),
    ('shield', r'escudo|prote|barreira|defesa|guarda|blindag|armadura|muralha'),
    ('flame', r'fogo|chama|inferno|incendi|brasas|flame|fire|queima|caos'),
    ('lightning', r'raio|relamp|relâmp|trov|electric|eletric|choque|thunder|tempest'),
    ('ice', r'gelo|neve|frio|congel|ice|frost|cristal'),
    ('eye', r'olho|mira|visão|visao|investig|analis|observ|leitura|mental|hipno'),
    ('portal', r'portal|dimens|tempo|magia|selo|runa|dominio|domínio|ritual|invoc|feiti'),
    ('chain', r'corrente|pris|amarra|teia|rede|captur|gancho|ancor|âncor|laço|laco'),
    ('wing', r'asa|voo|voar|pena|anjo|angel|fênix|fenix|levita'),
    ('skull', r'morte|veneno|tox|death|devor|sangue|necros|sentenca|sentença'),
    ('heart', r'cura|curar|vida|regen|restaur|recuper|resgat|cuidado'),
    ('flower', r'flor|raiz|planta|nature|árvore|arvore|espinho|vinha'),
    ('crown', r'rei|rainha|trono|imper|deus|deusa|juizo|juízo|suprem'),
    ('wave', r'onda|mar|água|agua|oceano|tsunami|vibra|sônico|sonico|som'),
    ('book', r'livro|nota|carta|escrit|grimor|plano|estrateg'),
    ('claw', r'garra|mord|dente|predat|fera|lobo|dragão|dragao'),
    ('star', r'luz|estrela|solar|sol|raio de luz|brilho|sagrad'),
]


def motif_for(skill: dict) -> str:
    words = f"{skill['name']} {skill['description']}".lower()
    for motif, pattern in MOTIFS:
        if re.search(pattern, words):
            return motif
    return {'beam': 'star', 'bolt': 'lightning', 'slash': 'sword',
            'web': 'chain', 'shield': 'shield', 'wave': 'wave',
            'psychic': 'portal', 'impact': 'fist'}.get(skill['icon'], 'star')


def palette(base: str, motif: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    r, g, b = (int(base[i:i+2], 16) for i in (1, 3, 5))
    h, _, _ = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    favored = {'flame': .055, 'lightning': .55, 'ice': .54, 'heart': .37,
               'flower': .33, 'skull': .78, 'shield': .47, 'star': .13,
               'sword': .59, 'gun': .58, 'wave': .52}
    h = (h * .48 + favored.get(motif, h) * .52) % 1
    def rgb(hue: float, saturation: float, value: float):
        return tuple(round(v * 255) for v in colorsys.hsv_to_rgb(hue % 1, saturation, value))
    return rgb(h, .72, .93), rgb(h+.085, .43, 1)


def words(value: str) -> set[str]:
    plain=unicodedata.normalize('NFD',value.lower())
    plain=''.join(ch for ch in plain if unicodedata.category(ch)!='Mn')
    return {x for x in re.findall(r'[a-z]{4,}',plain) if x not in
            {'para','sobre','quando','depois','antes','todos','todas','mais','tira','alvo','campo','trio','proprio','propria'}}


def art_path(owner: dict, skill: dict) -> str:
    plain=unicodedata.normalize('NFD',skill['id'].lower())
    plain=''.join(ch for ch in plain if unicodedata.category(ch)!='Mn')
    slug=re.sub(r'-+', '-', re.sub(r'[^a-z0-9-]+','-',plain)).strip('-')
    return f"/assets/skills/{owner['id']}/{slug}.png"


@lru_cache(maxsize=300)
def original_icon(path: str) -> Image.Image:
    return Image.open(PUBLIC/path.removeprefix('/assets/')).convert('RGBA')


def remix(character: dict, skill: dict, index: int, originals: list[tuple[dict,dict]], used: dict[str,int]) -> Image.Image:
    """Paint a new composition with an existing detailed combat texture as its core."""
    motif=motif_for(skill);c,accent=palette(character['color'],motif)
    seed=int.from_bytes(hashlib.sha256(f"{character['id']}:{skill['id']}".encode()).digest()[:8],'big')
    rng=random.Random(seed);terms=words(skill['name']);all_terms=words(skill['name']+' '+skill['description'])
    kinds={e['kind'] for e in skill['effects']}
    statuses={e.get('status') for e in skill['effects'] if e['kind']=='status'}
    def score(item: tuple[dict,dict]) -> float:
        owner,other=item;path=art_path(owner,other)
        other_terms=words(other['name']+' '+other['description'])
        other_statuses={e.get('status') for e in other['effects'] if e['kind']=='status'}
        return (20*(motif_for(other)==motif)+12*(other['icon']==skill['icon'])+
                14*len(terms&words(other['name']))+3*len(all_terms&other_terms)+
                6*len(statuses&other_statuses)+2*len(kinds&{e['kind'] for e in other['effects']})-
                16*used.get(path,0)+rng.random()*1.2)
    owner,match=max(originals,key=score)
    path=art_path(owner,match);used[path]=used.get(path,0)+1
    source=original_icon(path).copy()
    tinted=Image.blend(source.convert('RGB'),Image.new('RGB',source.size,c),.12)
    tinted=ImageEnhance.Contrast(tinted).enhance(1.12)
    alpha=source.getchannel('A')
    falloff=Image.new('L',source.size);fd=ImageDraw.Draw(falloff)
    for y in range(SIZE):
        for x in range(SIZE):
            radius=math.hypot(x-63.5,y-63.5)
            value=255 if radius<51 else round(255*max(0,min(1,(71-radius)/20)))
            fd.point((x,y),fill=value)
    tinted.putalpha(ImageChops.multiply(alpha,falloff))
    scaled=tinted.resize((112,112),Image.Resampling.LANCZOS)
    scaled=scaled.rotate(rng.randrange(-17,18),Image.Resampling.BICUBIC,expand=False)
    art=Image.new('RGBA',(SIZE,SIZE));art.alpha_composite(scaled,(8,8))
    glow=Image.new('RGBA',(SIZE,SIZE),(*c,0))
    glow.putalpha(art.getchannel('A').filter(ImageFilter.GaussianBlur(5)).point(lambda n:int(n*.18) if n>25 else 0))
    canvas=Image.new('RGBA',(SIZE,SIZE));canvas.alpha_composite(glow)
    d=ImageDraw.Draw(canvas)
    for j in range(2):
        radius=rng.randrange(45,62);a=rng.randrange(0,360)
        d.arc((64-radius,64-radius,64+radius,64+radius),a,a+rng.randrange(28,74),fill=(*accent,145),width=2)
    for _ in range(9):
        a=rng.random()*math.tau;r=rng.randrange(43,62)
        x,y=64+r*math.cos(a),64+r*math.sin(a)
        size=rng.choice((1,1,2));d.ellipse((x-size,y-size,x+size,y+size),fill=(*accent,rng.randrange(130,210)))
    canvas.alpha_composite(art)
    return canvas


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
    originals=[(c,s) for c in characters[:100] for s in c['skills']]
    used:dict[str,int]={}
    skill_records={(item['character'],item['id']):item for item in icons['skills']}
    pages={page['character']:page for page in sheets['pages']}
    ai=0
    for c in characters[100:]:
        source=SOURCES/f"{c['id']}.png"
        source_size=Image.open(source).size if source.exists() else None
        if source_size: ai+=1
        sheet=Image.new('RGBA',(512,176))
        records=[]
        for col,skill in enumerate(c['skills']):
            art=from_source(source,col) if source.exists() else jumping_flower_star(col) if c['id']=='mario' else remix(c,skill,col,originals,used)
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
                    'artMethod':'AI sheet' if source.exists() else 'object illustration' if c['id']=='mario' else 'remixed combat art'}
            records.append(record);skill_records[(c['id'],skill['id'])]=record
        sheet_target=PUBLIC/'sheets/skills/pages'/f"{c['id']}.png"
        sheet.save(sheet_target,optimize=True)
        pages[c['id']]={'character':c['id'],'sourceSheet':f"/assets/sheets/skills/pages/{c['id']}.png",
                        'sheet':f"/assets/sheets/skills/pages/{c['id']}.png",
                        'sourceResolution':list(source_size) if source_size else [512,176],
                        'category':'skills','format':'PNG RGBA','resolution':[512,176],
                        'columns':3,'rows':1,'cell':[CELL,CELL],'gutter':GUTTER,'margin':MARGIN,
                        'icons':records,'artMethod':'AI sheet' if source.exists() else 'object illustration' if c['id']=='mario' else 'remixed combat art'}
    icons['skills']=[skill_records[(c['id'],s['id'])] for c in characters for s in c['skills']]
    icons['count']=len(icons['skills'])
    sheets['pages']=[pages[c['id']] for c in characters]
    sheets['icons']=[item for page in sheets['pages'] for item in page['icons']]
    sheets['count']=len(sheets['icons'])
    icon_path.write_text(json.dumps(icons,ensure_ascii=False,indent=2)+'\n')
    sheet_path.write_text(json.dumps(sheets,ensure_ascii=False,indent=2)+'\n')
    objects=int(not (SOURCES/'mario.png').exists())
    print(f'Built 150 character sheets / 450 distinct icons ({ai} new AI sheets, {objects} object sheet, {150-ai-objects} remixed sheets).')


if __name__=='__main__': main()
