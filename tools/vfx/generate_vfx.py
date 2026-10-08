#!/usr/bin/env python3
"""Generate deterministic, layered combat VFX atlases and a neutral arena texture."""
from __future__ import annotations

import json
from io import BytesIO
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy.ndimage import gaussian_filter, map_coordinates

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "public/assets/vfx"
COLS, ROWS = 3, 4
FRAMES = 12
FPS = 20
SCALE = 2
FAMILIES = {
    "physical_light": ((255, 225, 177), 96, "physical"),
    "physical_heavy": ((255, 204, 150), 128, "grand"),
    "slash": ((218, 239, 255), 128, "slash"),
    "projectile": ((255, 225, 177), 96, "energy"),
    "energy_orb": ((139, 224, 255), 128, "energy"),
    "electric": ((255, 239, 142), 128, "electric"),
    "fire": ((255, 119, 56), 128, "fire"),
    "magic_psychic": ((193, 151, 255), 128, "magic"),
    "dark": ((174, 99, 239), 128, "dark"),
    "control": ((159, 225, 243), 128, "prison"),
    "shield": ((142, 222, 255), 128, "shield"),
    "heal_buff": ((139, 255, 193), 128, "heal"),
}


def _line_layer(n: int, family: str, frame: int, color: tuple[int, int, int]) -> Image.Image:
    """High resolution hand-built silhouettes: branches, crescents, cage, shards."""
    t = frame / (FRAMES - 1)
    s = SCALE
    im = Image.new("RGBA", (n*s, n*s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c = n*s/2
    unit = n*s
    rgba = (*color, 220)
    if family == "electric":
        # Branching, irregular arcs replace a single geometric bolt.
        rng = np.random.default_rng(321+frame)
        reach = (.22 + .68*min(1, t*1.5))*unit
        def bolt(x1: float, y1: float, x2: float, y2: float, depth: int=0, width: int=3):
            steps = max(3, int(math.hypot(x2-x1,y2-y1)/(unit*.085)))
            pts=[(x1,y1)]
            for k in range(1,steps):
                q=k/steps;pts.append((x1+(x2-x1)*q+rng.uniform(-.055,.055)*unit, y1+(y2-y1)*q+rng.uniform(-.055,.055)*unit))
            pts.append((x2,y2));d.line(pts,fill=rgba,width=width*s,joint="curve")
            if depth < 2:
                for k in range(2,steps,3):
                    x,y=pts[k]; bolt(x,y,x+rng.uniform(-.25,.25)*unit,y+rng.uniform(-.22,.22)*unit,depth+1,max(1,width-1))
        for angle in (0, math.pi*.66, math.pi*1.37):
            bolt(c+math.cos(angle)*.08*unit,c+math.sin(angle)*.08*unit,c+math.cos(angle)*reach,c+math.sin(angle)*reach)
    elif family == "slash":
        # Twin broad blade crescents with fading tapered ends.
        reach=(.25+.72*min(1,t*1.5))*unit
        for offset,alpha in ((0,235),(.12*unit,115)):
            box=(c-reach*.85+offset,c-reach*.68,c+reach*.85+offset,c+reach*.68)
            d.arc(box,200-70*t,345-70*t,fill=(*color,alpha),width=max(2,round(unit*.055)))
        for k in range(7):
            x=(.22+k*.09)*unit;y=(.30+((k*11)%7)*.075)*unit
            d.polygon([(x,y),(x+unit*.025,y-unit*.045),(x+unit*.04,y+unit*.025)],fill=(*color,170))
    elif family == "prison":
        close=min(1,t*1.4);half=(.48-.19*close)*unit
        for x in (c-half,c,c+half):
            d.line((x,c-unit*.45,x,c+unit*.45),fill=rgba,width=max(2,unit//48))
        for y in (c-unit*.28,c+unit*.28):
            d.arc((c-half,y-unit*.28,c+half,y+unit*.28),180,360,fill=rgba,width=max(2,unit//55))
        d.arc((c-unit*.43,c-unit*.43,c+unit*.43,c+unit*.43),200,340,fill=(*color,160),width=max(2,unit//64))
    elif family in {"impact", "physical", "grand", "interrupt", "ko"}:
        rng=np.random.default_rng(900+frame)
        count=22 if family in {"grand","ko"} else 13
        r=(.18+.62*min(1,t*1.35))*unit
        for k in range(count):
            a=math.tau*k/count+rng.uniform(-.07,.07)
            length=rng.uniform(.045,.14)*unit*(1-.25*t)
            x=c+math.cos(a)*r;y=c+math.sin(a)*r*.78
            tip=(x+math.cos(a)*length,y+math.sin(a)*length)
            side=length*.23
            d.polygon([(x-math.sin(a)*side,y+math.cos(a)*side),tip,(x+math.sin(a)*side,y-math.cos(a)*side)],fill=(*color,int(190*(1-.3*t))))
        if family in {"interrupt","ko"}:
            for k in range(5):
                x=(.26+k*.11)*unit;y=(.34+((k*7)%5)*.08)*unit
                d.line((x,y,x+unit*.07,y-unit*.1),fill=(*color,210),width=max(2,unit//50))
    elif family in {"shield", "buff", "debuff", "heal", "regen"}:
        rng=np.random.default_rng(170+frame)
        count=15 if family in {"heal","regen"} else 11
        for k in range(count):
            a=math.tau*k/count+t*2.4
            rad=(.26+.28*math.sin(t*math.pi))*unit
            x=c+math.cos(a)*rad;y=c+math.sin(a)*rad*.85
            r=(.018+rng.random()*.022)*unit
            if family in {"heal","regen"}: y-=unit*.18*t
            d.ellipse((x-r,y-r,x+r,y+r),fill=(*color,190))
        if family == "shield":
            for k in range(6):
                a=math.tau*k/6
                x=c+math.cos(a)*unit*.4;y=c+math.sin(a)*unit*.36
                d.line((x,y,x+unit*.055,y+unit*.05),fill=(*color,210),width=max(2,unit//50))
    elif family == "magic":
        # Arcane seal, broken into rotating segments and a center sigil.
        r=unit*(.30+.12*math.sin(t*math.tau))
        d.arc((c-r,c-r,c+r,c+r),int(15+360*t),int(250+360*t),fill=rgba,width=max(2,unit//55))
        d.arc((c-r*.76,c-r*.76,c+r*.76,c+r*.76),int(175-360*t),int(330-360*t),fill=(*color,170),width=max(2,unit//72))
        for k in range(9):
            a=math.tau*k/9+t*1.6;x=c+math.cos(a)*r;y=c+math.sin(a)*r
            d.polygon([(x,y-unit*.036),(x+unit*.024,y),(x,y+unit*.036),(x-unit*.024,y)],fill=(*color,200))
    elif family == "dark":
        rng=np.random.default_rng(740+frame)
        for k in range(5):
            a=math.tau*k/5+t*.9;pts=[]
            for j in range(8):
                q=j/7;rr=(.14+q*.56)*unit
                pts.append((c+math.cos(a+q*.45)*rr,c+math.sin(a+q*.45)*rr*.8))
            d.line(pts,fill=(*color,int(210*(1-.35*t))),width=max(3,unit//25),joint="curve")
    elif family == "fire":
        rng=np.random.default_rng(510+frame)
        for k in range(9):
            x=c+rng.uniform(-.28,.28)*unit;y=c+rng.uniform(-.2,.2)*unit
            h=unit*rng.uniform(.18,.44)*(1-.32*t);w=unit*rng.uniform(.04,.1)
            d.polygon([(x-w,y),(x-w*.55,y-h*.48),(x+rng.uniform(-w,w),y-h),(x+w*.8,y-h*.43),(x+w,y)],fill=(*color,int(200*(1-.45*t))))
    elif family == "energy":
        rng=np.random.default_rng(250+frame)
        # Short radial streamers surround the spinning orb; beam streak remains secondary.
        for k in range(10):
            a=math.tau*k/10+t*2.5;ri=unit*.16;ro=unit*(.34+.08*math.sin(t*math.tau+k))
            pts=[(c+math.cos(a)*ri,c+math.sin(a)*ri),(c+math.cos(a+.07)*unit*.25,c+math.sin(a+.07)*unit*.25),(c+math.cos(a+.1)*ro,c+math.sin(a+.1)*ro)]
            d.line(pts,fill=(*color,175),width=max(2,unit//65),joint="curve")
    elif family == "psychic":
        rng=np.random.default_rng(88+frame)
        for k in range(8):
            a=math.tau*k/8+t*.7;r=unit*(.3+.14*math.sin(t*math.pi+k))
            x=c+math.cos(a)*r;y=c+math.sin(a)*r*.8
            d.polygon([(x,y-unit*.065),(x+unit*.025,y+unit*.01),(x-unit*.02,y+unit*.075)],fill=(*color,150))
    return im


def frame(family: str, index: int, size: int, color: tuple[int, int, int]) -> Image.Image:
    n=size*SCALE
    yy,xx=np.mgrid[-1:1:complex(n),-1:1:complex(n)]
    rad=np.sqrt(xx*xx+yy*yy);angle=np.arctan2(yy,xx)
    t=index/(FRAMES-1)
    rng=np.random.default_rng(20261005+index*97+sum(map(ord,family)))
    noise=gaussian_filter(rng.random((n,n)).astype(np.float32),sigma=7*SCALE)
    noise=(noise-noise.min())/(noise.max()-noise.min()+1e-6)
    pulse=math.sin(math.pi*t)
    field=np.zeros((n,n),np.float32)
    if family in {"physical","impact","interrupt","ko","grand"}:
        expand=.12+.86*t
        ring=np.exp(-((rad-expand)/(.035+.025*t))**2)*(.9-.34*t)
        core=np.exp(-(rad/max(.12,.5*(1-t)+.08))**2)*(.98-.55*t)
        shards=np.maximum(0,np.cos(angle*(20 if family=="grand" else 13)+noise*8+t*8))**18*np.exp(-((rad-(.28+.45*t))/.25)**2)
        field=ring+core*.55+shards*(.8 if family in {"physical","grand"} else .5)
    elif family=="energy":
        r=.2+.11*math.sin(t*math.tau)
        orb=np.exp(-((rad-r)/(.08+.035*noise))**2)
        spiral=np.maximum(0,np.sin(angle*4+rad*24-t*math.tau*1.6+noise))**7*np.exp(-((rad-.4)/.28)**2)
        field=orb+spiral*.65+np.exp(-((rad-.055)/.055)**2)*.85
    elif family=="electric":
        # Lightning silhouettes are supplemented by the branching layer above.
        arcs=np.maximum(0,np.cos(angle*7+noise*3+t*9))**16*np.exp(-((rad-(.25+.57*t))/.2)**2)
        field=arcs+np.exp(-((rad-.16)/.09)**2)*pulse
    elif family=="fire":
        tongues=np.maximum(0,np.sin(angle*7+rad*13-noise*6-t*9))**5
        field=tongues*np.exp(-((rad-(.35+.12*math.sin(t*math.pi)))/.34)**2)*(1-.32*t)
        field+=np.exp(-((rad-.18)/.15)**2)*(.72-.4*t)
    elif family=="slash":
        curve=yy-(.45*xx+.36*math.sin(t*math.tau))
        field=np.exp(-(curve/(.075+.018*noise))**2)*np.clip(1-np.abs(xx)*.7,0,1)
        field*=np.clip(1-abs(t-.55)*1.65,0,1)
    elif family=="magic":
        glyph=np.maximum(0,np.sin(angle*9+rad*32-t*math.tau*1.4+noise))**9
        field=glyph*np.exp(-((rad-(.38+.08*math.sin(t*math.tau)))/.16)**2)+np.exp(-((rad-.13)/.045)**2)*pulse
    elif family=="dark":
        tendrils=np.maximum(0,np.sin(angle*5+rad*19-noise*8+t*3))**4
        field=tendrils*np.exp(-((rad-.45)/.35)**2)+np.exp(-(rad/.19)**2)*(.9-.4*t)
    elif family=="psychic":
        distort=np.sin(rad*31-noise*9+t*9+np.sin(angle*4)*1.8)
        field=np.exp(-(distort/.19)**2)*np.clip(1-rad,0,1)*(.5+.5*pulse)
    elif family=="shield":
        sides=6;sector=2*math.pi/sides
        polygon=rad*np.cos((angle+math.pi/sides+sector/2)%sector-sector/2)
        surface=np.exp(-((polygon-(.63-.06*pulse))/.035)**2)
        ripple=np.exp(-((rad-(.25+.42*t))/.025)**2)*pulse
        field=surface+ripple*.8
    elif family=="prison":
        close=np.clip(t*1.25,0,1);bars=np.maximum(0,np.cos(angle*4))**36
        cage=bars*np.exp(-((rad-(.76-.21*close))/.07)**2)
        field=cage+np.exp(-((rad-(.6-.2*close))/.025)**2)*pulse
    elif family in {"heal","regen","buff"}:
        rise=np.maximum(0,np.sin(angle*7+rad*14+t*7+noise))**8
        field=rise*np.exp(-((rad-(.48-.2*t))/.25)**2)*(.8-.3*t)
        field+=np.exp(-((rad-(.18+.56*t))/.028)**2)*.65
    elif family=="debuff":
        field=np.maximum(0,np.sin(angle*8+rad*22+noise*5))**7*np.exp(-((rad-.46)/.38)**2)
    else:
        field=np.maximum(0,np.sin(angle*6+rad*23-t*6))**8*np.exp(-((rad-.4)/.3)**2)
    field=np.clip(field,0,1)
    # Family-specific heat, smoke, and aura layers.
    glow=gaussian_filter(field,sigma=5*SCALE)
    smoke=gaussian_filter(noise*(1-field),sigma=12*SCALE)*(.28 if family in {"fire","dark","ko"} else 0)
    smoke*=np.exp(-((rad-.46)/.48)**2)
    alpha=np.clip(field*.88+glow*.68+smoke*.24,0,.97)
    alpha[rad>.985]=0
    if family in {"physical","interrupt","ko","grand"}: alpha*=max(.25,1-.55*t)
    if family in {"heal","regen","buff","shield"}: alpha*=.55+.32*pulse
    rgb=np.empty((n,n,3),dtype=np.uint8)
    col=np.asarray(color,np.float32)
    inner=np.clip(field[...,None]*.34+glow[...,None]*.68,0,.96)
    rgb[:]=(col*(1-inner)+255*inner).clip(0,255).astype(np.uint8)
    if family in {"fire","dark","ko"}:
        rgb=(rgb.astype(np.float32)*(1-smoke[...,None]*.6)).clip(0,255).astype(np.uint8)
    rgba=Image.fromarray(np.dstack((rgb,(alpha*255).astype(np.uint8))),"RGBA")
    rgba.alpha_composite(_line_layer(size,family,index,color))
    # Supersampled masters are reduced with Lanczos for crisp mobile scaling.
    return rgba.resize((size,size),Image.Resampling.LANCZOS)


def arena() -> Image.Image:
    w,h=768,1056;y,x=np.mgrid[0:h,0:w]
    nx,ny=(x-w/2)/(w/2),(y-h/2)/(h/2);radial=np.sqrt(nx*nx+ny*ny)
    base=np.zeros((h,w,3),np.float32);base[:]=(7,13,21)
    center=np.exp(-((nx/.8)**2+(ny/.52)**2)*2.3)
    base+=center[...,None]*np.array([24,48,60]);base*=np.clip(1-radial*.23,.48,1)[...,None]
    img=Image.fromarray(np.uint8(np.clip(base,0,255)),"RGB").convert("RGBA")
    overlay=Image.new("RGBA",(w,h),(0,0,0,0));d=ImageDraw.Draw(overlay);cx,cy=w//2,h//2
    d.polygon([(cx-224,cy-93),(cx-181,cy-124),(cx+181,cy-124),(cx+224,cy-93),(cx+224,cy+93),(cx+181,cy+124),(cx-181,cy+124),(cx-224,cy+93)],fill=(37,71,79,13),outline=(168,218,222,22),width=2)
    for rx,ry,a in ((248,121,29),(211,101,20),(160,75,12)):
        d.ellipse((cx-rx,cy-ry,cx+rx,cy+ry),outline=(167,211,218,a),width=2)
    d.line((35,cy,w-35,cy),fill=(169,212,216,21),width=2)
    img.alpha_composite(overlay);return img


def beam_sheet() -> Image.Image:
    """A short transparent, looping beam texture; rotation/scale are done by CSS."""
    w,h=256,32
    sheet=Image.new("RGBA",(w,h*4),(0,0,0,0))
    for i in range(4):
        y,x=np.mgrid[0:h,0:w];rng=np.random.default_rng(100+i)
        ripple=np.sin(x*.14+i*1.5+np.sin(x*.037)*2)*.5+.5
        streak=gaussian_filter(rng.random((h,w)).astype(np.float32),sigma=(1.4,7))
        streak=(streak-streak.min())/(streak.max()-streak.min()+1e-6)
        edge=np.exp(-((y-(h-1)/2)/9)**4)
        core=np.exp(-((y-(h-1)/2)/2.8)**2)
        alpha=np.uint8(np.clip((edge*(.45+.22*ripple+.14*streak)+core*.3)*255,0,242))
        rgb=np.stack((np.uint8(119+125*core),np.uint8(184+70*core),np.uint8(224+31*core)),axis=-1)
        sheet.paste(Image.fromarray(np.dstack((rgb,alpha)),"RGBA"),(0,h*i))
    return sheet


def main() -> None:
    """Hoje só a textura neutra da arena sai daqui.

    Os efeitos de combate passaram para tools/vfx/generate_families.py
    (adendo, parte 3): 46 folhas neutras tingidas pelo jogo, no lugar dos
    treze atlas coloridos que este arquivo gerava. As funções antigas ficam
    como referência do primeiro conjunto.
    """
    OUT.mkdir(parents=True,exist_ok=True)
    arena().save(OUT/"arena.webp","WEBP",quality=86,method=5)
    manifest={"arena":{"file":"arena.webp","size":[768,1056],"containsText":False,"containsFigures":False}}
    for stale in OUT.glob("*.webp"):
        if stale.name!="arena.webp": stale.unlink()
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(f"generated arena in {OUT}")


if __name__=="__main__": main()
