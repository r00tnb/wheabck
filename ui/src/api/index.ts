import axios from 'axios'
import * as socketio from 'socket.io-client'

const base_url = window.location.origin //指定后台网址，默认同域网址

axios.defaults.headers.post['Content-Type'] = "application/json"
axios.defaults.timeout = 10000

export interface ResponseData {
    code: number,
    msg: string,
    data: any
}

export interface MessageHandler {//消息处理函数
    (data: ResponseData): void
}

/**
 * api对象，用于某个session进行api调用
 */
export class ApiItem {
    public sessionID: string // 指定api所属的session id
    public socketio: socketio.Socket

    public constructor(sessionID: string) {
        this.sessionID = sessionID
        this.socketio = socketio.io(this.getApiUrl(true))
    }

    /**
     * 获取api的接口地址
     * @param isSocket 是否是websocket的接口地址
     * @returns api接口地址
     */
    private getApiUrl(isSocket: boolean): string {
        return `${base_url}/${this.sessionID}/${isSocket ? 'ss' : 'http'}`
    }


    /**
     * 获取对应的真实api地址，若是websocket类型的消息则返回监听的事件名，否则返回完整url路径
     * @param pluginID 插件ID
     * @param name 消息名称
     * @param isSocket 是否是websocket类型的消息
     * @returns 对应的真实地址
     */
    public getRealAddr(pluginID: string, name: string, isSocket = false): string {
        if (isSocket)
            return `${pluginID}_${name}`
        return `${this.getApiUrl(false)}/${pluginID}/${name}`
    }

    /**
     * 监听指定插件的某一个消息
     * @param pluginID 插件ID
     * @param name 消息名称
     * @param handler 消息处理函数
     */
    public on(pluginID: string, name: string, handler: MessageHandler) {
        this.socketio.on(this.getRealAddr(pluginID, name, true), (data) => {
            handler(data)
        })
    }

    /**
     * 向后台发送消息
     * @param pluginID 插件ID
     * @param name 消息名
     * @param data 传递的数据
     * @param http_handler http消息处理函数，若不传入则表示消息是一个websocket消息
     */
    public async emit(pluginID: string, name: string, data: any, http_handler?: MessageHandler) {
        if (http_handler === undefined) {
            this.socketio.emit(this.getRealAddr(pluginID, name, true), data)
        } else {
            const res = await axios.post(this.getRealAddr(pluginID, name), data)
            http_handler(res.data)
        }
    }
}

/**
 * 用于整个框架的全局api
 */
export class GlobalApi extends ApiItem {
    public apiList: ApiItem[] // 存储除全局api外的api
    private pluginID = "global"
    public constructor() {
        super("global")
        this.apiList = new Array<ApiItem>()
    }

    /**
     * 保存一个api对象并返回对应的sessionID
     * @param api 需要保存的api对象
     * @returns 返回保存的api对应的sessionID
     */
    public push(api: ApiItem): string {
        this.apiList.push(api)
        return api.sessionID
    }

    /**
     * 删除指定sessionID对应的API
     * @param sessionID 指定sessionID
     */
    public remove(sessionID: string) {
        const i = this.apiList.findIndex(api => api.sessionID === sessionID)
        if (i !== -1)
            this.apiList.splice(i, 1)
    }

    /**
     * 获取指定sessionID的api，若找不到返回undefined
     * @param sessionID 要查找的sessionID
     * @returns 查找到的api
     */
    public getApi(sessionID: string): ApiItem | undefined {
        return this.apiList.find((api) => {
            return api.sessionID === sessionID
        })
    }

    /**
     * 监听指定插件的某一个消息
     * @param name 消息名称
     * @param handler 消息处理函数
     */
    public listen(name: string, handler: MessageHandler) {
        this.on(this.pluginID, name, handler)
    }

    /**
     * 向后台发送消息
     * @param name 消息名
     * @param data 传递的数据
     * @param http_handler http消息处理函数，若不传入则表示消息是一个websocket消息
     */
    public async send(name: string, data: any, http_handler?: MessageHandler) {
        this.emit(this.pluginID, name, data, http_handler)
    }

    /**
     * 通过消息名称获取对应的http类型的api地址
     * @param name 消息名称
     * @returns 真实api地址
     */
    public getUrlByMsg(name:string):string{
        return this.getRealAddr(this.pluginID, name, false)
    }

}

// 用于全局的消息api
export default new GlobalApi()

export * from './post'