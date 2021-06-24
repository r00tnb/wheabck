import { useEffect, useState } from "react"
import { MsgTransfer } from "../api"

export default function TestPage(){
    const [info, setInfo] = useState('test123')
    useEffect(()=>{
        const trans = new MsgTransfer(window.top, window.top.origin)
        trans.listen("get-config", (data)=>{
            console.log('TestPage recv info', data)
            setInfo(data.name)
            return {nb:'gyhnb'}
        })
        trans.listen("set-config", (data)=>{
            console.log('TestPage recv info', data)
            setInfo(data.name)
        })
    }, [])

    return (
        <div>
            {info}
        </div>
    )
}