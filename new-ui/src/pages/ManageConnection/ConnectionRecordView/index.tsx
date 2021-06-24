import { Input, Button, Space, Popconfirm, Modal, Form, Row, Col, Cascader, Divider, Drawer } from "antd"
import React, { useEffect, useRef, useState } from 'react'
import { t } from '../../../i18n'
import { IConnectionRecord, ICodeExecutorItem } from "../../../typing/plugin"
import api, { FrameMsg, MsgTransfer } from '../../../api'
import { CascaderOptionType } from "antd/lib/cascader"
import { findArrayElementCommonValues } from "../../../utls"

interface ICascaderOptionTypeEx extends CascaderOptionType {
    codeExecutor?: ICodeExecutorItem
}

interface IBaseConfig {
    url: string,
    webshellType: string[],
    note: string,
}

interface propsType {
    visible: boolean,
    title: string,
    onClose: () => void,
    onOk: (record: IConnectionRecord) => void,
    recordData?:IConnectionRecord
}


const { useForm, Item } = Form

export default function ConnectionRecordView(props: propsType) {
    const { visible, title, onOk, onClose, recordData } = props
    const [form] = useForm<IBaseConfig>()
    const [okBtnLoading, setOkBtnLoading] = useState(false)
    const [typeOptions, setTypeOptions] = useState<CascaderOptionType[]>([])
    const [configCollectSrc, setConfigCollectSrc] = useState('')
    const iframe = useRef<HTMLIFrameElement>(null)

    useEffect(() => {
        if (visible) {
            api.send("get-code-executor-list", {}, (data) => {
                const codeExecutorList = (data.data as ICodeExecutorItem[])
                let options: CascaderOptionType[] = []
                const types: string[] = findArrayElementCommonValues(codeExecutorList, 'type')
                types.forEach(t => {
                    let children: ICascaderOptionTypeEx[] = []
                    codeExecutorList.forEach(item => {
                        if (item.type === t) {
                            children.push({
                                label: item.name,
                                value: item.id,
                                isLeaf: true,
                                codeExecutor: item
                            })
                        }
                    })
                    options.push({
                        label: t,
                        value: t,
                        isLeaf: false,
                        children: children
                    })
                })
                setTypeOptions(options)
            })
        }
    }, [visible])

    useEffect(()=>{
        if(recordData){
            const baseConfig:IBaseConfig = {
                url:recordData.url,
                note:recordData.note,
                webshellType:[recordData.webshellType, recordData.codeExecutorID]
            }
            form.setFieldsValue(baseConfig)

            //setConfigCollectSrc(recordData.)
            setCodeExecutorConfig(recordData.config)
        }
    }, [recordData])

    /**
     * 设置代码执行器的配置信息
     * @param config 代码执行器的配置信息
     */
    function setCodeExecutorConfig(config:any){
        const wind = iframe.current?.contentWindow
        if (!wind) return
        const trans = new MsgTransfer(wind, wind.origin)
        trans.send("set-config", config)
    }

    /**
     * 获取收集到的配置数据
     */
    async function getCodeExecutorConfig() {
        const wind = iframe.current?.contentWindow
        if (!wind) return {}
        const trans = new MsgTransfer(wind, wind.origin)
        const recvData = await trans.send("get-config", {}, (data) => {
            return data.data
        }) as FrameMsg
        return recvData.data
    }

    async function onSubmit() {
        const baseConfig = form.getFieldsValue()
        const record:IConnectionRecord = {
            url:baseConfig.url,
            note:baseConfig.note,
            webshellType:baseConfig.webshellType[0],
            codeExecutorID:baseConfig.webshellType[1]
        }
        setOkBtnLoading(true)
        record.config = await getCodeExecutorConfig()
        onOk(record)
        setOkBtnLoading(false)
    }

    function typeChange(_: any, selectedOptions?: CascaderOptionType[]) {
        if (!selectedOptions || selectedOptions.length === 0) return
        const codeExecutor = (selectedOptions[1] as ICascaderOptionTypeEx).codeExecutor
        if (codeExecutor) {
            setConfigCollectSrc(codeExecutor.uiPathOfConfig)
        }
    }

    return (
        <Drawer closable={false} width="800px" visible={visible} title={
            <div>
                <span style={{ marginRight: '20px' }}>{title}</span>
                <Space>
                    <Button loading={okBtnLoading} onClick={onSubmit} type="primary">{t("提交")}</Button>
                    <Button onClick={() => {
                        setOkBtnLoading(false)
                        onClose()
                    }}>{t("取消")}</Button>
                </Space>
            </div>
        } onClose={() => {
            if (!okBtnLoading) onClose()
        }} >
            <Divider>{t("基本配置")}</Divider>
            <Form layout="vertical" name="baseConfig" form={form} >
                <Row gutter={10}>
                    <Col span={12}>
                        <Item label={t("webshell地址")} name="url" >
                            <Input />
                        </Item>
                        <Item label={t("类型&代码执行器")} name="webshellType" >
                            <Cascader options={typeOptions} onChange={typeChange} />
                        </Item>
                    </Col>
                    <Col span={12}>
                        <Item label={t("备注")} name="note" >
                            <Input.TextArea autoSize={{ minRows: 5 }} />
                        </Item>
                    </Col>
                </Row>
            </Form>
            <Divider>{t("代码执行器配置")}</Divider>
            {
                configCollectSrc ? <iframe ref={iframe} style={{ height: '100%', width: '100%' }} title={configCollectSrc} src={configCollectSrc} /> : <span>NO!</span>
            }
        </Drawer>
    )
}