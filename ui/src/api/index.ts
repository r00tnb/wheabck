import axios from 'axios'
import * as socketio from 'socket.io'

axios.defaults.headers.post['Content-Type'] = "application/json"
axios.defaults.timeout = 10000

export interface ResponseData {
    code:number,
    msg:string,
    result:any
}

export abstract class ApiItem {
    public name:string
    public url:string
    public static domain:string
    public constructor(name:string, url:string){
        this.name = name
        this.url = url
    }

    public abstract request(): ResponseData
}

export interface Handler {//消息处理函数
    (data:JSON):JSON|undefined
}

export interface Message {//消息类型
    name:string,
    data?:any,
    need_rely?:boolean
}

export class Api {
    public api_list: ApiItem[]
    public constructor(){
        this.api_list = new Array<ApiItem>()
    }
    public push(item:ApiItem){
        this.api_list.push(item)
    }
    public pop(name:string):ApiItem|undefined{
        const index = this.api_list.findIndex((item)=>{
            return item.name === name
        })
        if(index === -1) return undefined
        return this.api_list.splice(index, 1)[0]
    }
    public request(name:string):ResponseData|undefined{ //同步
        const item = this.api_list.find((item)=>{
            return item.name===name
        })
        if(item === undefined) return undefined
        return item.request()
    }

    /**
     * 监听指定名称的消息
     * @param name 消息名称
     * @param handler 消息处理函数
     */
    public on(name:string, handler:Handler){

    }
}

const api: Api = new Api()

export default api