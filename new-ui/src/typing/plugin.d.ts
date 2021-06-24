export interface IConnectionItem {
    id: string,
    createDatetime: number,
    webshellType: string,
    url: string,
    ip: string,
    note: string,
    sessionCount: Int16Array, //该连接生成的存活session数量
    codeExecutorID: string, //代码执行器的插件ID
    config?: any, // 代码执行器收集到的配置信息
    key?: string //为了表格中使用
}

export interface IConnectionRecord {
    url: string,
    webshellType: string,
    note: string,
    codeExecutorID:string,
    config?: any // 代码执行器收集到的配置信息
}

export interface IPluginItem {
    id:string,
    type:string,
    name:string,
    uiPath:string
}

export interface ICodeExecutorItem extends IPluginItem {
    uiPathOfConfig:string // 用于配置收集的UI地址
}