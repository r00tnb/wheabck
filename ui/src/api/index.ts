import axios from 'axios'
import * as socketio from 'socket.io-client'

axios.defaults.headers.post['Content-Type'] = "application/json"
axios.defaults.timeout = 10000

export interface ResponseData {
    code:number,
    msg:string,
    data:any
}

export interface ApiItem {
    name:string, //消息名
    url:string, // api路径
    isSocket?:boolean // 表示当前api是否是websocket类型
}

export interface Handler {//消息处理函数
    (data:ResponseData):ResponseData|void
}

export interface Message {//消息类型
    name:string,
    data?:any,
    need_rely?:boolean
}

export class Api {
    public api_list: ApiItem[]
    public socketio: socketio.Socket
    public constructor(){
        this.api_list = new Array<ApiItem>()
        this.socketio = socketio.io("/socket.io")
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

    /**
     * 获取消息名的真实事件名称，用于和服务端交互
     * @param msg_name 消息名(websocket类型)
     * @returns 真实事件名称
     */
    public get_real_msg_name(msg_name:string):string{
        return `global_${msg_name}`
    }

    /**
     * 监听指定名称的消息(websocket类型的消息)
     * @param name 消息名称
     * @param handler 消息处理函数
     */
    public on(name:string, handler:Handler){
        this.socketio.on(this.get_real_msg_name(name), (data)=>{
            handler(data)
        })
    }

    /**
     * 向服务器发送消息
     * @param name 消息名称
     * @param data 传递的数据
     * @param http_handler 对于http消息将在返回数据后调用，否则不可用
     */
    public async emit(name:string, data:any, http_handler?:Handler){
        let item = this.api_list.find((v)=>{
            if(v.isSocket) name = this.get_real_msg_name(name)
            return v.name === name
        })
        if(item){
            if(item.isSocket){
                this.socketio.emit(item.name, data)
            }else{
                let res = await axios.post(item.url, data)
                if(http_handler){
                    http_handler(res.data)
                }
            }
        }
    }
}

/**
 * 描述插件api的类，每次session生成并加载完毕插件时，为每个带有前端界面的插件生成一个api实例
 */
export class PluginApi extends Api{
    public session_id:string
    public plugin_id:string
    public constructor(session_id:string, plugin_id:string){
        super()
        this.session_id = session_id
        this.plugin_id = plugin_id
    }

    public get_real_msg_name(msg_name:string):string{
        return `plugin_${this.session_id}_${this.plugin_id}_${msg_name}`
    }
}

const api: Api = new Api()

/**
 * 初始化API
 */
// 全局api
let global_api_path = "/global-api"
let global_api:ApiItem[] = [
    {
        name:'get-connections',
        url: `${global_api_path}/get-connections`
    }
]

export default api