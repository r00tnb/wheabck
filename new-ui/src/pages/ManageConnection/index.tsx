import React, { useState } from "react";
import { Table, Input, Button, Space, Popconfirm, Modal, Form } from "antd"
import { EditOutlined, DeleteOutlined, PlayCircleOutlined, PlusOutlined } from '@ant-design/icons'
import { t } from "../../i18n";
import { randomStr } from "../../utls";
import { useEffect } from "react";
import api from '../../api'
import ConnectionRecordView from './ConnectionRecordView'
import { IConnectionItem, IConnectionRecord } from "../../typing/plugin";

interface TableConnectionItem extends IConnectionItem {
    key?: string //为了表格中使用
}

const { Column } = Table
const {useForm} = Form

/**
 * 展示并管理webshell连接信息
 */
export default function ManageConnection() {
    const [loading, setLoading] = useState(true)
    const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([])
    const [conns, setConns] = useState<TableConnectionItem[]>([])
    const [modalVisible, setModalVisible] = useState(false)

    const [form] = useForm<IConnectionRecord>()

    useEffect(() => {
        console.log(api.getUrlByMsg("get-webshell-connections"))
        api.send("get-webshell-connections", {}, data => {
            const d = (data.data as Array<IConnectionItem>).map(item => {
                return { ...item, key: item.id }
            })
            setLoading(false)
            setConns([...d])
        })
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    function addConnection(connRecord:IConnectionRecord) {
        console.log(connRecord)
    }
    function deleteConnection(record: TableConnectionItem) {
        console.log(record)
    }
    function deleteSelected() { }
    function createSession(record: TableConnectionItem) {

    }
    function createSelected() { }
    function editConnection(record: TableConnectionItem) {

    }

    return (
        <div>
            <Space style={{ margin: "0 10px 10px 10px" }}>
                <Button type="primary" onClick={() => setModalVisible(true)} icon={<PlusOutlined />}>{t("创建")}</Button>
                <Popconfirm disabled={selectedRowKeys.length === 0} title={t("确定删除选中项吗？")} okText={t("确定")} cancelText={t("取消")} onConfirm={deleteSelected}>
                    <Button disabled={selectedRowKeys.length === 0} type="primary" danger icon={<DeleteOutlined />}>{t("批量删除")}</Button>
                </Popconfirm>
                <Popconfirm disabled={selectedRowKeys.length === 0} title={t("确定从选中的连接生成session吗？")} okText={t("确定")} cancelText={t("取消")} onConfirm={createSelected}>
                    <Button disabled={selectedRowKeys.length === 0} type="primary" style={selectedRowKeys.length === 0 ? {} : { backgroundColor: '#40B017', borderColor: '#40B017' }} icon={<PlayCircleOutlined />}>{t("批量生成session")}</Button>
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
                    (count) => {
                        return (
                            <Button type="link" shape="circle" style={count === 0 ? {} : { backgroundColor: '#CCFFCC', color: "black" }}>{count}</Button>
                        )
                    }
                } />
                <Column title={t("备注")} dataIndex="note" key="note" />
                <Column title={t("操作")} key="action" render={
                    (_, record) => {
                        return (
                            <span>
                                <Button type="link" onClick={() => editConnection(record as TableConnectionItem)} icon={<EditOutlined />} title={t("编辑配置")} />
                                <Button type="link" onClick={() => createSession(record as TableConnectionItem)} icon={<PlayCircleOutlined />} title={t("生成session")} />
                                <Popconfirm title={t("确定删除吗？")} okText={t("确定")} cancelText={t("取消")} onConfirm={() => deleteConnection(record as TableConnectionItem)}>
                                    <Button type="link" icon={<DeleteOutlined />} title={t("删除")} />
                                </Popconfirm>
                            </span>
                        )
                    }
                } />
            </Table>
            <ConnectionRecordView recordData={{
                url:"http://xxx.com/1.php",
                note:"dsfa",
                webshellType:"JSP",
                codeExecutorID:"sdfsdf",
                config:{
                    test123:'nbnbnbnbnbnb'
                }
            }} title={t("创建连接")} visible={modalVisible} onClose={()=>setModalVisible(false)} onOk={addConnection} />
        </div>
    )
}