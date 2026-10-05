export const hz=(midi:number)=>440*2**((midi-69)/12);
export function tone(ctx:BaseAudioContext,out:AudioNode,time:number,frequency:number,duration:number,gain:number,type:OscillatorType='sine',endFrequency?:number){
  const osc=ctx.createOscillator(),amp=ctx.createGain();osc.type=type;
  osc.frequency.setValueAtTime(frequency,time);
  if(endFrequency)osc.frequency.exponentialRampToValueAtTime(Math.max(20,endFrequency),time+duration);
  amp.gain.setValueAtTime(0,time);amp.gain.linearRampToValueAtTime(gain,time+Math.min(.018,duration*.15));amp.gain.exponentialRampToValueAtTime(.0001,time+duration);
  osc.connect(amp);amp.connect(out);osc.start(time);osc.stop(time+duration+.015);
  osc.onended=()=>{osc.disconnect();amp.disconnect();};
}
let noiseCache:AudioBuffer|undefined;
export function noise(ctx:BaseAudioContext,out:AudioNode,time:number,duration:number,gain:number,frequency:number,type:BiquadFilterType='lowpass'){
  if(!noiseCache||noiseCache.sampleRate!==ctx.sampleRate){noiseCache=ctx.createBuffer(1,ctx.sampleRate,ctx.sampleRate);const values=noiseCache.getChannelData(0);let seed=7382;for(let i=0;i<values.length;i++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;values[i]=(seed/4294967296)*2-1;}}
  const source=ctx.createBufferSource(),filter=ctx.createBiquadFilter(),amp=ctx.createGain();source.buffer=noiseCache;filter.type=type;filter.frequency.value=frequency;filter.Q.value=.6;
  amp.gain.setValueAtTime(0,time);amp.gain.linearRampToValueAtTime(gain,time+.006);amp.gain.exponentialRampToValueAtTime(.0001,time+duration);
  source.connect(filter);filter.connect(amp);amp.connect(out);source.start(time);source.stop(time+duration+.01);source.onended=()=>{source.disconnect();filter.disconnect();amp.disconnect();};
}
