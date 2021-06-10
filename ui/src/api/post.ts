

export interface FrameMsg{
    name:string,
    data:any
}

export interface FrameMsgHandler {
    (msg:FrameMsg):void
}

/**
 * 用于消息在iframe中的传递
 */
 export class MsgTransfer {
    public wind:Window
    public origin:string

    /**
     * 
     * @param wind window对象
     * @param origin Window对象对应的origin, 若不指定尝试从wind中获取
     */
    public constructor(wind:Window, origin?:string){
        this.wind = wind
        this.origin = origin===undefined?this.wind.origin:origin
    }

    public send(name:string, data:any){
        this.wind.postMessage({name:name, data:data}, this.origin)
    }

    public listen(name:string, handler:FrameMsgHandler){
        this.wind.addEventListener('message', (event:MessageEvent<FrameMsg>)=>{
            handler(event.data)
        })
    }
}