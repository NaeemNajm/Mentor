import { useEffect, useState } from 'react'
import Scheduler from '../components/Scheduler'
import axios from 'axios'

export default function Home(){
  const [blocks, setBlocks] = useState([])

  useEffect(()=>{
    axios.get((process.env.NEXT_PUBLIC_API_URL||'http://localhost:8000') + '/api/blocks/')
      .then(r=>setBlocks(r.data))
      .catch(()=>setBlocks([]))
  },[])

  return (
    <div style={{padding:20,fontFamily:'Arial'}}>
      <h1>Mentor — Scheduler (MVP)</h1>
      <Scheduler blocks={blocks} />
    </div>
  )
}
