#!/usr/bin/env python3
"""Create layered, deterministic original battle cue WAVs for the Web Audio mixer."""
from __future__ import annotations

import json
import math
import wave
from pathlib import Path

import numpy as np
from scipy.signal import butter, sosfilt

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/"public/assets/audio/sfx"
RATE=24000
VARIANTS=4
LENGTHS={"physical-light":.42,"physical-heavy":.78,"energy-charge":.95,"energy-shot":.58,"energy-impact":.78,"electric-charge":.52,"electric-hit":.48,"fire-cast":.72,"fire-impact":.72,"magic-cast":.95,"magic-impact":.75,"slash-fast":.36,"slash-heavy":.61,"shield-on":.68,"shield-hit":.55,"heal":.86,"regen":.72,"interrupt":.38,"shatter":.68,"ko":1.05,"grand-charge":1.25,"grand-impact":1.18,"domain-turn":.82,"victory":1.45,"defeat":1.25}


def env(n:int,attack:float=.02,decay:float=.35,curve:float=2.0)->np.ndarray:
    t=np.arange(n)/RATE
    a=np.clip(t/max(attack,.001),0,1)
    return np.sin(a*np.pi/2)**1.7*np.exp(-np.maximum(0,t-attack)/max(decay,.005))**curve


def filtered_noise(rng:np.random.Generator,n:int,lo:int,hi:int)->np.ndarray:
    x=rng.normal(0,1,n)
    sos=butter(3,[lo,min(hi,RATE*.48)],btype="bandpass",fs=RATE,output="sos")
    return sosfilt(sos,x)


def tone(n:int,f0:float,f1:float,phase:float=0,shape:float=1)->np.ndarray:
    t=np.arange(n)/RATE
    freq=f0+(f1-f0)*(1-np.exp(-t*shape*4))
    return np.sin(phase+2*np.pi*np.cumsum(freq)/RATE)


def cue(name:str,variant:int)->np.ndarray:
    dur=LENGTHS[name];n=round(RATE*dur);rng=np.random.default_rng(20261005+sum(map(ord,name))*31+variant*7919)
    t=np.arange(n)/RATE;mix=np.zeros(n,np.float64)
    seed=variant*.41
    if name.startswith("physical") or name in {"energy-impact","fire-impact","magic-impact","shield-hit","grand-impact","ko"}:
        heavy=name in {"physical-heavy","energy-impact","fire-impact","magic-impact","shield-hit","grand-impact","ko"}
        # Low sub impact + woody mid-body + broadband contact/crackle + short resonant tail.
        sub=tone(n,82+variant*5,38+variant*3,seed)*env(n,.008,dur*.48,1.15)
        body=tone(n,205+variant*17,71+variant*7,seed,.7)*env(n,.012,dur*.26,1.35)
        crack=filtered_noise(rng,n,420,7800)*env(n,.002,.075,1.8)
        tail=filtered_noise(rng,n,800,4200)*np.exp(-t*(8 if heavy else 13))
        mix+=sub*(.72 if heavy else .43)+body*(.42 if heavy else .25)+crack*(.16 if heavy else .12)+tail*.07
        if name=="grand-impact": mix+=tone(n,54,29,.3)*env(n,.015,dur*.85,.7)*.45
    elif "electric" in name:
        # Several stochastic crackles with snapping transient and a short rounded body.
        noise=filtered_noise(rng,n,1050,10000)
        gate=np.zeros(n)
        for k in range(10+variant*2):
            at=int(rng.uniform(.015,dur*.72)*RATE);width=int(rng.uniform(.009,.028)*RATE)
            gate[at:min(n,at+width)]+=np.hanning(max(4,min(width,n-at)))[:max(0,min(width,n-at))]
        snap=tone(n,880+variant*45,230,seed,2)*env(n,.002,.13,2)
        low=tone(n,105,62,seed,.4)*env(n,.004,.2,1)
        mix+=noise*gate*.4+snap*.22+low*.27
    elif name.startswith("energy") or name=="grand-charge":
        charge=name.endswith("charge")
        sweep=tone(n,115+variant*9,610+variant*29,seed,.85 if charge else 1.7)
        over=tone(n,230+variant*12,920+variant*39,seed+1.1,1.2)
        air=filtered_noise(rng,n,900,6800)*env(n,.12 if charge else .008,.27,1.2)
        low=tone(n,64,38,seed,.5)*env(n,.025,dur*.55,.9)
        mix+=sweep*env(n,.07,dur*.7,.9)*.27+over*env(n,.09,dur*.36,1.2)*.10+air*.12+low*.24
    elif name.startswith("fire"):
        roar=filtered_noise(rng,n,95,1700)
        hiss=filtered_noise(rng,n,2400,10000)
        pulse=(.65+.35*np.sin(2*np.pi*(7+variant)*t+seed))
        low=tone(n,92,43,seed,.55)*env(n,.02,dur*.6,.9)
        mix+=roar*env(n,.025,dur*.62,.8)*pulse*.3+hiss*env(n,.08,dur*.4,1)*.12+low*.3
    elif name.startswith("magic") or name=="domain-turn":
        reverse=np.clip((t/dur)**1.8,0,1) if name.endswith("cast") else np.exp(-t*5)
        layers=[]
        for k,interval in enumerate((1,1.25,1.5,2)):
            f=155*(1+seed*.16)*interval
            layers.append(tone(n,f,f*(1.4 if name.endswith("cast") else .78),seed+k*.7,.45)*(.13/(k+1)))
        shimmer=filtered_noise(rng,n,3000,10000)*env(n,.08,dur*.5,1)
        impact=tone(n,410,165,seed,.8)*env(n,.012,dur*.35,1.4)
        mix+=sum(layers)*reverse+shimmer*.12+impact*.12
    elif name.startswith("slash"):
        whoosh=filtered_noise(rng,n,850,7000)
        slice_tone=tone(n,1150+variant*120,260,seed,2.8)
        contact=filtered_noise(rng,n,1800,11000)*env(n,.01,.08,2)
        mix+=whoosh*env(n,.015,dur*.2,1.8)*.32+slice_tone*env(n,.012,.09,1.6)*.17+contact*.13
    elif name.startswith("shield"):
        ring=tone(n,390+variant*11,640+variant*17,seed,.65)
        overtone=tone(n,810+variant*23,490,seed+1,.8)
        hit=filtered_noise(rng,n,500,6200)*env(n,.003,.07,2)
        mix+=ring*env(n,.035,dur*.55,.75)*.24+overtone*env(n,.06,dur*.36,1)*.14+hit*.12
    elif name in {"heal","regen"}:
        shimmer=filtered_noise(rng,n,2000,10500)
        bed=sum(tone(n,220*k,220*k+40,seed+k,.5)*(.15/k) for k in (1,2,3,4))
        rise=np.clip(t/dur,0,1)**1.4
        mix+=bed*rise*.28+shimmer*env(n,.1,dur*.5,.7)*.14
    elif name in {"interrupt","shatter"}:
        crack=filtered_noise(rng,n,700,11000)*env(n,.001,.11,2)
        body=tone(n,510,115,seed,2)*env(n,.003,.17,1.5)
        chips=filtered_noise(rng,n,2600,10000)*np.exp(-t*13)
        mix+=crack*.3+body*.2+chips*.17
    elif name in {"victory","defeat"}:
        notes=(60,64,67,72,76) if name=="victory" else (62,59,55,50)
        from scipy.signal import chirp
        for i,midi in enumerate(notes):
            at=round((i*(.16 if name=="victory" else .2))*RATE);ln=n-at
            if ln<=0:continue
            freq=440*2**((midi-69)/12);segment=np.arange(ln)/RATE
            mix[at:]+=np.sin(2*np.pi*freq*segment)*np.exp(-segment*(2.1 if name=="victory" else 2.8))*.11
        mix+=filtered_noise(rng,n,1600,6000)*env(n,.09,.4,1.2)*.04
    else:
        mix+=tone(n,180,370,seed,1)*env(n,.02,dur*.5,1)*.22
    # Very subtle deterministic pitch/texture variation and peak normalization.
    mix+=filtered_noise(rng,n,80,12000)*env(n,.003,.18,1.2)*.018
    peak=max(float(np.max(np.abs(mix))),1e-8)
    return (mix/peak*.78).clip(-1,1)


def main()->None:
    OUT.mkdir(parents=True,exist_ok=True);manifest={"sampleRate":RATE,"channels":1,"encoding":"pcm_s16le","variants":VARIANTS,"sounds":{}}
    for name in LENGTHS:
        clips=[cue(name,variant) for variant in range(VARIANTS)]
        gap=np.zeros(round(RATE*.11),dtype=np.float64)
        offsets=[round(i*(LENGTHS[name]+.11),3) for i in range(VARIANTS)]
        samples=np.concatenate([clip if i==VARIANTS-1 else np.concatenate((clip,gap)) for i,clip in enumerate(clips)])
        path=OUT/f"{name}.wav"
        with wave.open(str(path),"wb") as out:
            out.setnchannels(1);out.setsampwidth(2);out.setframerate(RATE);out.writeframes((samples*32767).astype("<i2").tobytes())
        manifest["sounds"][name]={"file":path.name,"duration":LENGTHS[name],"variantOffsets":offsets}
    (OUT/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    total=sum(p.stat().st_size for p in OUT.glob("*.wav"))
    print(f"generated {len(LENGTHS)} cue families × {VARIANTS} WAV variations ({total/1024:.0f} KiB)")


if __name__=="__main__":main()
