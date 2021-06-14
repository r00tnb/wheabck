import { Menu } from 'antd'
import { ReactNode } from 'react'
import { MenuOutlined } from '@ant-design/icons'
import { NavLink } from 'react-router-dom'

export interface MenuItem {
    key: string,
    title: string,
    to?: string,
    icon?: ReactNode,
    disabled?: boolean,
    children?: MenuItem[]
}

interface propsType {
    menus: MenuItem[],
    onclick?:(menu:MenuItem)=>void
}

export default function MyMenu(props: propsType) {
    const { menus, onclick } = props
    const clickMenu = (item:MenuItem)=>{
        return ()=>{
            if(onclick)
                onclick(item)
        }
    }
    const createMenu = (menus:MenuItem[]): ReactNode => {
        return (
            menus.map(item => {
                if (item.children !== undefined) {
                    return (
                        <Menu.SubMenu disabled={item.disabled} key={item.key} title={item.title} icon={item.icon ? item.icon : <MenuOutlined />}>
                            {createMenu(item.children)}
                        </Menu.SubMenu>
                    )
                } else {
                    return (
                        <Menu.Item disabled={item.disabled} key={item.key} title={item.title} icon={item.icon ? item.icon : <MenuOutlined />}>
                            {
                                item.to ? <NavLink to={item.to} onClick={clickMenu(item)}>
                                    {item.title}
                                </NavLink> : item.title}
                        </Menu.Item>
                    )
                }
            })
        )
    }
    return (
        <Menu theme="dark" mode="inline">
            {createMenu(menus)}
        </Menu>
    )
}