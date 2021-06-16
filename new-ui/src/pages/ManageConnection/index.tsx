import { useState } from "react";
import { Table, TableColumnsType } from "antd"
import { t } from "../../i18n";
import { randomStr } from "../../utls";
import { useEffect } from "react";
import api from '../../api'


export interface ConnectionItem {
    id:string
    createDatetime:number,
    webshellType:string,
    url:string,
    ip:string,
    note:string,
    codeExecutorID:string, //代码执行器的插件ID
    config?:any // 代码执行器收集到的配置信息
}

const columns:TableColumnsType<ConnectionItem> = [
    {title:t("创建时间"), dataIndex:"createDatetime", key:randomStr()},
    {title:t("webshell类型"), dataIndex:"webshellType", key:randomStr()},
    {title:t("webshell地址"), dataIndex:"url", key:randomStr()},
    {title:t("IP"), dataIndex:"ip", key:randomStr()},
    {title:t("备注"), dataIndex:"note", key:randomStr()},
]

const {Column} = Table

/**
 * 展示并管理webshell连接信息
 */
export default function ManageConnection(){
    const [loading, setLoading] = useState(true)
    const [conns, setConns] = useState<ConnectionItem[]>([])
    useEffect(()=>{
        console.log(api.getUrlByMsg("get-webshell-connections"))
        api.send("get-webshell-connections", {}, data=>{
            console.log('Test API',data)
            setLoading(false)
            setConns([...conns, ...(data.data as Array<ConnectionItem>)])
        })
    // eslint-disable-next-line react-hooks/exhaustive-deps
    },[])
    return (
        <div>
            <Table loading={loading} bordered={true} columns={columns} dataSource={conns}>
                <Column title={t("创建时间")} dataIndex="createDatetime" key="createDatetime" />
                <Column title={t("webshell类型")} dataIndex="webshellType" key="webshellType" />
                <Column title={t("webshell地址")} dataIndex="url" key="url" />
                <Column title={t("IP")} dataIndex="ip" key="ip" />
                <Column title={t("备注")} dataIndex="note" key="note" />
                <Column title={t("操作")} key="action" render={
                    
                } />
            </Table>
        </div>
    )
}