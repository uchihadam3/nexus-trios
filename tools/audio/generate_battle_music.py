#!/usr/bin/env python3
"""Render four original, tempo-synced, dynamically mixed battle music stems."""
from __future__ import annotations

import math
import subprocess
import tempfile
from pathlib import Path

import numpy as np

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'public/assets/audio'
RATE=22050
BPM=108
BEAT=60/BPM
BAR=BEAT*4
BARS=64
DURATION=BAR*BARS
LENGTH=round(DURATION*RATE)

CHORDS=[(50,[62,65,69]),(46,[58,62,65]),(41,[57,60,65]),(48,[55,60,64])]
SCALE=[50,53,55,57,60,62,65,69,72,74,77,81]
STEMS={k:np.zeros((LENGTH,2),dtype=np.float32) for k in ('harmony','rhythm','pulse','lead')}

def add_tone(stem:str, start:float, duration:float, note:float, volume:float, shape:str='sine', pan:float=0, decay:float=7):
    start_i=max(0,round(start*RATE));count=min(round(duration*RATE),LENGTH-start_i)
    if count<=0:return
    t=np.arange(count,dtype=np.float32)/RATE
    freq=440*2**((note-69)/12)
    phase=t*freq*2*np.pi
    if shape=='pad':
        signal=(np.sin(phase)+.32*np.sin(phase*2+.2)+.12*np.sin(phase*3+.5))/1.44
        attack=np.minimum(1,t/.24)
        tail=np.minimum(1,np.maximum(0,(duration-t)/.34))
        env=attack*tail
    elif shape=='pluck':
        signal=np.sin(phase)+.23*np.sin(phase*2)+.09*np.sin(phase*3.01)
        env=(1-np.exp(-t*90))*np.exp(-t*decay)
    elif shape=='lead':
        signal=(np.sin(phase)+.35*np.sin(phase*2.003)+.14*np.sin(phase*3.01))/1.49
        env=np.minimum(1,t/.018)*np.minimum(1,np.maximum(0,(duration-t)/.11))*np.exp(-t*.9)
    elif shape=='kick':
        f=41+76*np.exp(-t*21)
        signal=np.sin(2*np.pi*np.cumsum(f)/RATE)
        env=np.exp(-t*12)
    elif shape=='snare':
        rng=np.random.default_rng(start_i+51)
        noise=rng.uniform(-1,1,count).astype(np.float32)
        low=np.sin(2*np.pi*180*t)
        signal=noise*.72+low*.28
        env=np.exp(-t*19)
    elif shape=='hat':
        rng=np.random.default_rng(start_i+17)
        signal=rng.uniform(-1,1,count).astype(np.float32)
        env=np.exp(-t*53)
    else:
        signal=np.sin(phase)
        env=np.minimum(1,t/.01)*np.exp(-t*8)
    signal=(signal*env*volume).astype(np.float32)
    left=math.sqrt((1-pan)/2);right=math.sqrt((1+pan)/2)
    STEMS[stem][start_i:start_i+count,0]+=signal*left
    STEMS[stem][start_i:start_i+count,1]+=signal*right

def render():
    # Long chord beds change voicing at 16-bar boundaries, while a light sequencer
    # and syncopated motif keep all 142 seconds evolving over four broad sections.
    rng=np.random.default_rng(74931)
    for bar in range(BARS):
        sec=bar//16
        chord_i=(bar//4)%4
        bass,notes=CHORDS[chord_i]
        section_gain=(.80,1.0,1.12,.9)[sec]
        down=bar*BAR
        if bar%4==0:
            for i,n in enumerate(notes):
                add_tone('harmony',down,note_duration(BAR*3.85),n,0.074*section_gain,'pad',pan=(-.46+i*.46))
        # A softened high chord tone shifts by section to open/close the arc.
        if sec in (1,2) and bar%4==0:
            add_tone('harmony',down+BAR*.5,BAR*1.55,notes[1]+12,.032,'pad',.32)
        # Bass with rests and octave pickups instead of a static drone.
        for beat in range(4):
            at=down+beat*BEAT
            note=bass+(12 if (bar%4==3 and beat==3 and sec>=2) else 0)
            add_tone('pulse',at,.43,note,.18,'pluck',-.12,3.5)
            if beat in (1,3) and (bar%8!=7):
                passing=notes[(beat//2+bar)%len(notes)]+12
                add_tone('pulse',at+BEAT*.5,.19,passing,.052,'pluck',.1,7)
        # A compact 4-bar melodic idea is re-voiced every section, with rests left
        # for the music to breathe around the synthesized drums.
        motif=[0,4,7,4,2,5,7,9,7,5,4,2,0,2,4,7]
        for eighth in range(8):
            beat=eighth//2
            slot=bar%4*4+eighth%4
            if ((slot+sec*3)%11 in (1,2,7)) or (sec==3 and slot%4==0):
                idx=(motif[slot%len(motif)]+(sec*2 if sec==2 else 0))%len(SCALE)
                add_tone('lead',down+eighth*BEAT*.5,.24,SCALE[idx]+12,.072*section_gain,'lead',(-.24 if eighth%2 else .22),5.4)
        # Four-on-floor kick, backbeat snare, and a controlled closed-hat pattern.
        for beat in range(4):
            if beat in (0,2) or sec==2 and bar%2==1 and beat==3:
                add_tone('rhythm',down+beat*BEAT,.34,36,.23*section_gain,'kick',0)
            if beat in (1,3):
                add_tone('rhythm',down+beat*BEAT,.22,38,.105*section_gain,'snare',.08)
            hat_power=.046 if beat%2==0 else .028
            add_tone('rhythm',down+beat*BEAT,.047,92,hat_power,'hat',.2 if beat%2 else -.2)
            add_tone('rhythm',down+beat*BEAT+BEAT*.5,.035,92,hat_power*.64,'hat',-.18 if beat%2 else .18)
        # Small reverse-like transition swell every eight bars (quiet filtered noise).
        if bar%8==7:
            start=down+BAR*3.35
            dur=BAR*.65
            count=round(dur*RATE)
            t=np.arange(count)/RATE
            noise=rng.normal(0,1,count).astype(np.float32)
            env=np.linspace(0,.055*section_gain,count,dtype=np.float32)
            tone=noise*env*np.sin(np.linspace(0,np.pi,count,dtype=np.float32))
            start_i=round(start*RATE)
            if start_i+count<=LENGTH:
                pan=np.linspace(-.7,.7,count,dtype=np.float32)
                STEMS['rhythm'][start_i:start_i+count,0]+=tone*np.sqrt((1-pan)/2)
                STEMS['rhythm'][start_i:start_i+count,1]+=tone*np.sqrt((1+pan)/2)
    # Keep a gentle tail into the loop; identical opening/closing chord + beat makes
    # the final bar transition back to the first bar naturally.
    for samples in STEMS.values():
        peak=np.max(np.abs(samples))
        if peak>.72:samples*=.72/peak

def note_duration(seconds:float):return seconds

def write_stems():
    OUT.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='nexus-music-') as tmp:
        for name,stereo in STEMS.items():
            wav=Path(tmp)/f'{name}.wav'
            pcm=np.clip(stereo,-.98,.98)
            data=(pcm*32767).astype('<i2')
            import wave
            with wave.open(str(wav),'wb') as handle:
                handle.setnchannels(2);handle.setsampwidth(2);handle.setframerate(RATE);handle.writeframes(data.tobytes())
            dest=OUT/f'{name}.ogg'
            subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(wav),'-c:a','libvorbis','-q:a','3',str(dest)],check=True)
            print(f'{name}: {dest.stat().st_size/1024:.0f} KiB')

if __name__=='__main__':
    render();write_stems()
    print(f'Duração do tema: {DURATION:.1f}s ({DURATION/60:.2f} min) a {BPM} BPM')
