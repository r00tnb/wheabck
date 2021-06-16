import React, { useState } from "react";
import { Table, TableColumnsType, Button, Space, Popconfirm } from "antd"
import { EditOutlined, DeleteOutlined, PlayCircleOutlined, PlusOutlined } from '@ant-design/icons'
import { t } from "../../i18n";
import { randomStr } from "../../utls";
import { useEffect } from "react";
import api from '../../api'


export interface ConnectionItem {
    id: string,
    createDatetime: number,
    webshellType: string,
    url: string,
    ip: string,
    note: string,
    sessionCount:Int16Array, //该连接生成的存活session数量
    codeExecutorID: string, //代码执行器的插件ID
    config?: any, // 代码执行器收集到的配置信息
    key?: string //为了表格中使用
}


const { Column } = Table

/**
 * 展示并管理webshell连接信息
 */
export default function ManageConnection() {
    const [loading, setLoading] = useState(true)
    const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
    const [conns, setConns] = useState<ConnectionItem[]>([])
    useEffect(() => {
        console.log(api.getUrlByMsg("get-webshell-connections"))
        api.send("get-webshell-connections", {}, data => {
            const d = (data.data as Array<ConnectionItem>).map(item => {
                return { ...item, key: item.id }
            })
            setLoading(false)
            setConns([...d])
        })
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    function addConnection() { }
    function deleteConnection(record: ConnectionItem) {
        console.log(record)
    }
    function deleteSelected() { }
    function createSession(record: ConnectionItem) {

    }
    function createSelected() { }
    function editConnection(record: ConnectionItem) {

    }

    return (
        <div>
            <Space style={{ margin: "0 10px 10px 10px" }}>
                <Button type="primary" onClick={addConnection} icon={<PlusOutlined />}>{t("创建")}</Button>
                <Popconfirm disabled={selectedRowKeys.length===0} title={t("确定删除选中项吗？")} okText={t("确定")} cancelText={t("取消")} onConfirm={deleteSelected}>
                    <Button disabled={selectedRowKeys.length===0} type="primary" icon={<DeleteOutlined />}>{t("批量删除")}</Button>
                </Popconfirm>
                <Popconfirm disabled={selectedRowKeys.length===0} title={t("确定从选中的连接生成session吗？")} okText={t("确定")} cancelText={t("取消")} onConfirm={createSelected}>
                    <Button disabled={selectedRowKeys.length===0} type="primary" icon={<PlayCircleOutlined />}>{t("批量生成session")}</Button>
                </Popconfirm>
            </Space>
            <Table rowSelection={{
                selectedRowKeys,
                onChange(rowKeys) {
                    console.log(rowKeys)
                    setSelectedRowKeys(rowKeys)
                }
            }} loading={loading} bordered={true} dataSource={conns}>
                <Column title={t("创建时间")} dataIndex="createDatetime" key="createDatetime" />
                <Column title={t("webshell类型")} dataIndex="webshellType" key="webshellType" />
                <Column title={t("webshell地址")} dataIndex="url" key="url" />
                <Column title={t("IP")} dataIndex="ip" key="ip" />
                <Column title={t("存活Session数量")} dataIndex="sessionCount" key="sessionCount" render={
                    (count)=>{
                        return (
                            <Button type="link" shape="circle" style={count===0?{}:{backgroundColor:'#CCFFCC', color:"black"}}>{count}</Button>
                        )
                    }
                } />
                <Column title={t("备注")} dataIndex="note" key="note" />
                <Column title={t("操作")} key="action" render={
                    (_, record) => {
                        return (
                            <span>
                                <Button type="link" onClick={() => editConnection(record as ConnectionItem)} icon={<EditOutlined />} title={t("编辑配置")} />
                                <Button type="link" onClick={() => createSession(record as ConnectionItem)} icon={<PlayCircleOutlined />} title={t("生成session")} />
                                <Popconfirm title={t("确定删除吗？")} okText={t("确定")} cancelText={t("取消")} onConfirm={() => deleteConnection(record as ConnectionItem)}>
                                    <Button type="link" icon={<DeleteOutlined />} title={t("删除")} />
                                </Popconfirm>
                            </span>
                        )
                    }
                } />
            </Table>
        </div>
    )
}