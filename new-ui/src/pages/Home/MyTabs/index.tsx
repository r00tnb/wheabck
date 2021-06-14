import { Tabs } from "antd"
import React from 'react'
import { Route, useHistory } from "react-router-dom";
import { RouteItem } from "../../../routes";

const {TabPane} = Tabs

export interface TabItem {
    key:string,
    title:string,
    route:RouteItem,
    closable?:boolean
}

interface propsType {
    tabs:TabItem[],
    setTabs: React.Dispatch<React.SetStateAction<TabItem[]>>,
    activeKey:string,
    setActiveKey:React.Dispatch<React.SetStateAction<string>>
}

export function MyTabs(props:propsType){
    const {tabs, setTabs, activeKey, setActiveKey} = props
    const history = useHistory()
    const editTab = (key:any, action:"add"|"remove")=>{
        if(action !== 'remove') return
        let mykey = key
        const newTabs = tabs.filter((tabItem, index)=>{
            if(tabItem.key === key){
                if(index>0 && index+1<tabs.length){
                    mykey = tabs[index+1].key
                }
                return false
            }
            return true
        })
        setTabs(newTabs)
        if(newTabs.length){
            if(mykey === key) mykey = newTabs[newTabs.length-1].key
            clickTab(mykey)
        }
    }
    const clickTab = (key:string)=>{
        const tab = tabs.find(item => key===item.key)
        if(tab){
            history.push(tab.route.path)
            setActiveKey(tab.key)
        }
    }
    return (
        <Tabs activeKey={activeKey} type="editable-card" hideAdd onEdit={editTab} style={{backgroundColor: "white", height:"100%"} } onTabClick={clickTab}>
            {
                tabs.map((tabItem)=>(
                    <TabPane key={tabItem.key} tab={tabItem.title} closable={tabItem.closable} >
                        <Route path={tabItem.route.path} component={tabItem.route.component}></Route>
                    </TabPane>
                ))
            }
        </Tabs>
    )
}