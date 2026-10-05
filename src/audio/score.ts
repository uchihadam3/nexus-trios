import { hz,noise,tone } from './synth';
import { PRESENTATION as P } from '../presentation/config';
export const SCORE={bpm:P.audio.bpm,bars:16,stepsPerBar:16};
export const sixteenth=60/SCORE.bpm/4;
// Original 16-bar arrangement: evolving drums, syncopated bass, warm seventh
// chords and a sparse answering motif. All sound is synthesized locally.
export function scoreStep(ctx:BaseAudioContext,out:AudioNode,step:number,time:number){
  const bar=Math.floor(step/16)%16,beat=step%16,section=Math.floor(bar/4),root=[38,34,41,36][bar%4];
  if([0,6,8].includes(beat)||(bar%4===3&&beat===14)){tone(ctx,out,time,148,.21,.48,'sine',42);noise(ctx,out,time,.035,.08,1300);}
  if(beat===4||beat===12){noise(ctx,out,time,.15,.22,2700);tone(ctx,out,time,175,.085,.10,'triangle',105);}
  if(beat%2===0||(section===2&&beat%4===3))noise(ctx,out,time,beat===14?.10:.037,beat%4===2?.075:.037,4900,'highpass');
  if([0,3,6,8,10,14].includes(beat)){const note=root+(beat===10?12:beat===14?7:0);tone(ctx,out,time,hz(note),sixteenth*(beat===0?2.7:1.65),.16,'triangle');tone(ctx,out,time,hz(note)/2,sixteenth*1.8,.055);}
  if(beat===0){const intervals=bar%4===0?[0,3,7,10]:bar%4===1?[0,4,7,11]:[0,4,7,9];for(const interval of intervals)tone(ctx,out,time,hz(root+24+interval),sixteenth*15,.032,'triangle');}
  if(section!==0&&[2,7,11,15].includes(beat)){const phrase=[12,7,10,15],note=root+24+phrase[[2,7,11,15].indexOf(beat)];tone(ctx,out,time,hz(note),.32,section===2?.037:.025);tone(ctx,out,time+.19,hz(note),.3,.012);}
  if(bar%4===3&&[13,15].includes(beat))noise(ctx,out,time,.055,.07,2200);
}
