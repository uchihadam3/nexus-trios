import { useState } from 'react';
import type { Character } from '../engine/types';
export function Portrait({character:c,className=''}:{character:Character;className?:string}){
  const [failed,setFailed]=useState(false);
  return <div className={`portrait ${className}`} style={{'--character':c.color} as React.CSSProperties}>
    {!failed&&<img src={c.portrait} data-portrait={c.id} alt="" onError={()=>setFailed(true)}/>}
    {failed&&<svg className="portrait-art" viewBox="0 0 240 300" aria-hidden="true">
      <defs><linearGradient id={`g-${c.id}-${className.replaceAll(' ','')}`} x2="1" y2="1"><stop stopColor={c.color} stopOpacity=".6"/><stop offset="1" stopColor={c.color} stopOpacity=".05"/></linearGradient></defs>
      <circle cx="120" cy="115" r="90" fill="none" stroke={c.color} opacity=".2"/><circle cx="120" cy="115" r="73" fill="none" stroke={c.color} opacity=".12"/>
      <path d="M20 300L39 223L87 195L94 175L146 175L153 195L202 223L225 300" fill={c.color} opacity=".16"/>
      <path d="M80 104L90 74L119 63L150 76L161 105L152 153L134 177L105 177L87 153Z" fill={c.color} opacity=".24"/>
      <path d="M80 103L70 80L83 82L79 53L96 68L105 35L119 61L143 41L143 68L163 61L157 87L167 98L151 102L144 89L98 91L90 105Z" fill={c.color} opacity=".32"/>
      <path d="M88 192L120 228L150 192L161 222L144 294H95L78 223Z" fill={c.color} opacity=".2"/>
      <path d="M101 117L113 120M130 120L142 117" fill="none" stroke={c.color} strokeWidth="3" opacity=".9"/>
      <text x="120" y="272" textAnchor="middle" fill={c.color} opacity=".8" fontFamily="system-ui" fontWeight="800" fontSize="36">{c.symbol}</text>
      <path d="M20 26H47M20 26V53M220 26H193M220 26V53M20 274H47M220 274H193" fill="none" stroke={c.color} opacity=".4"/>
    </svg>}
  </div>;
}
