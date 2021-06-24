

export interface FrameMsg{
    name:string,
    data:any
}

export interface FrameMsgHandler {
    (msg:FrameMsg):any|void // 若返回了非undefined的数据，则返回数据会被发回源窗口对象
}


const receivePrefix = "recv_" // 用于标记接受某个消息的返回数据

/**
 * 用于消息在iframe中的传递
 */
 export class MsgTransfer {
    public target:Window
    public origin:string

    /**
     * 
     * @param target 目标window对象
     * @param origin 目标Window对象对应的origin, 若不指定尝试从wind中获取
     */
    public constructor(target:Window, origin?:string){
        this.target = target
        this.origin = origin===undefined?this.target.origin:origin
    }

    /**
     * 根据传入消息名返回其对应的接收消息名
     * @param name 消息名
     * @returns 消息对应的接收消息名
     */
    private getRecvMsgName(name:string):string{
        return `${receivePrefix}${name}`
    }

    /**
     * 发送消息
     * @param name 发送的消息名
     * @param data 携带的数据
     * @param recvHandler 对接受传回消息的处理函数
     */
    public async send(name:string, data:any, recvHandler?:FrameMsgHandler){
        this.target.postMessage({name:name, data:data}, this.origin)
        if(recvHandler)
            return new Promise((resolve, reject)=>{
                window.addEventListener('message', (event:MessageEvent<FrameMsg>)=>{
                    const result:FrameMsg = {name:this.getRecvMsgName(name), data:undefined}
                    if(result.name === event.data.name){
                        result.data = recvHandler(event.data)
                        resolve(result)
                    }else{
                        console.log(`No recv correct message in send: ${result.name}`,event.data)
                    }
                })
            })
    }

    /**
     * 监听消息
     * @param name 要监听的消息名
     * @param handler 消息处理函数
     */
    public async listen(name:string, handler:FrameMsgHandler){
        return new Promise((resolve, reject)=>{
            window.addEventListener('message', (event:MessageEvent<FrameMsg>)=>{
                const result:FrameMsg = {name:name, data:undefined}
                if(result.name === event.data.name){
                    result.data = handler(event.data)
                    if(result.data !== undefined)
                        this.target.postMessage({name:this.getRecvMsgName(name), data:result.data}, this.origin)
                    resolve(result)
                }else{
                    console.log(`No recv correct message in listen: ${result.name}`,event.data)
                }
            })
        })
    }
}