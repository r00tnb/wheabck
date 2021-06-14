import { useState } from "react";
import { Table, TableColumnsType } from "antd"
import { t } from "../../i18n";
import { randomStr } from "../../utls";
import { useEffect } from "react";
import api from '../../api'

export interface ConnectionItem {
    createDatetime:number,
    webshellType:string,
    url:string,
    ip:string,
    note:string,
    key:string
}

const columns:TableColumnsType<ConnectionItem> = [
    {title:t("创建时间"), dataIndex:"createDatetime", key:randomStr()},
    {title:t("webshell类型"), dataIndex:"webshellType", key:randomStr()},
    {title:t("webshell地址"), dataIndex:"url", key:randomStr()},
    {title:t("IP"), dataIndex:"ip", key:randomStr()},
    {title:t("备注"), dataIndex:"note", key:randomStr()},
]

/**
 * 展示并管理webshell连接信息
 */
export default function ManageConnection(){
    const [loading, setLoading] = useState(true)
    const [conns, setConns] = useState<ConnectionItem[]>([
        {
            createDatetime:Date.now(),
            webshellType:"PHP",
            url:"http://sdfsdf.com/1.php",
            ip:"127.0.0.1",
            note:"test123",
            key:randomStr()
        }
    ])
    useEffect(()=>{
        console.log(api.getUrlByMsg("get-webshell-connections"))
        api.send("get-webshell-connections", {}, data=>{
            console.log('Test API',data)
            setLoading(false)
            setConns([...conns, ...(data.data as Array<ConnectionItem>)])
        })
    },[])
    return (
        <div>
            <Table loading={loading} bordered={true} columns={columns} dataSource={conns} />
        </div>
    )
}