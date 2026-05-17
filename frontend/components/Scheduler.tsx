import React from 'react'

export default function Scheduler({blocks}:{blocks:any[]}){
  const slots = Array.from({length: 96}).map((_,i)=>{
    const hh = Math.floor(i/4)
    const mm = (i%4)*15
    return {idx:i, time: `${String(hh).padStart(2,'0')}:${String(mm).padStart(2,'0')}`}
  })

  const bySlot: Record<number, any> = {}
  blocks.forEach((b:any)=>{
    // naive mapping: compute start slot from hour/min
    const d = new Date(b.start_iso)
    const idx = d.getHours()*4 + Math.floor(d.getMinutes()/15)
    bySlot[idx] = b
  })

  return (
    <div style={{display:'grid',gridTemplateColumns:'repeat(4,1fr)',gap:10}}>
      {slots.map(s=> (
        <div key={s.idx} style={{border:'1px solid #ddd',padding:10, minHeight:60, background: bySlot[s.idx]? '#e6ffed' : '#fff'}}>
          <div style={{fontSize:12,color:'#666'}}>{s.time}</div>
          <div style={{marginTop:6}}>{bySlot[s.idx]? bySlot[s.idx].title : ''}</div>
        </div>
      ))}
    </div>
  )
}
