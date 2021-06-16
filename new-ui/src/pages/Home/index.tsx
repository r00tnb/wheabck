import React, { useState } from 'react'
import { Layout } from 'antd'
import 'antd/dist/antd.css'
import './index.css'
import Test from '../../components/Test';
import { MyTabs, TabItem } from './MyTabs'
import MyMenu, { MenuItem } from './MyMenu'
import { RouteComponentProps } from "react-router-dom";
import { routeTable } from "../../routes";
import { useEffect } from 'react'
import { randomStr } from '../../utls'
import { t } from '../../i18n';

const { Header, Content, Footer, Sider } = Layout

const defaultMenus: MenuItem[] = [
  {
    key: randomStr(),
    title: "test123",
    to: "/test123"
  },
  {
    key: randomStr(),
    title: t("webshell连接管理"),
    to:"/manage-webshell-connections"
  }
]

const defaultTabs: TabItem[] = [
  {
    key: randomStr(),
    title: "Dashboard",
    route: { path: "/dashboard", component: Test },
    closable: false
  }
]

export default function Home(props: RouteComponentProps) {
  const [collapsed, setcollapsed] = useState<boolean>(false)
  const [tabs, setTabs] = useState<TabItem[]>(defaultTabs)
  const [activeTabKey, setActiveTabKey] = useState(tabs.length ? tabs[0].key : "")
  const [menus] = useState<MenuItem[]>(defaultMenus)
  const { location } = props

  /**
   * 根据path指定的路由添加一个标签页，若指定路由不在路由表则不添加.
   * @param path 标签页对应的路由
   * @param title 标签页标题
   * @param unique 若为真则当已存在该路由的标签时不会添加新的标签页
   */
  const addTab = (path: string, title: string, unique=false) => {
    const routeItem = routeTable.find(path)
    if (routeItem) {
      const tab = tabs.find(item => item.route.path === path && (item.closable === false||unique))//若tabs中存在路由相等且无法关闭的标签则不再生成新的
      let key = randomStr()
      if (!tab) {
        setTabs([...tabs, {
          key: key,
          title: title,
          route: routeItem
        }])
      }else
        key = tab.key
      setActiveTabKey(key)
    }
  }

  const onMenuClick = (item: MenuItem) => {
    if (item.to)
      addTab(item.to, item.title, true)
  }

  useEffect(() => {//挂载后判断当前路由是否在设定的路由表中，是则添加一个标签页并跳到该标签
    addTab(location.pathname, "unknown")
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setcollapsed} >
        <div className="logo" >
          <h2>{t("Wheabck")}</h2>
        </div>
        <MyMenu onclick={onMenuClick} menus={menus} />
      </Sider>
      <Layout>
        <Header style={{ padding: 0 }} />
        <Content style={{ margin: '0 16px' }}>
          <MyTabs tabs={tabs} setTabs={setTabs} activeKey={activeTabKey} setActiveKey={setActiveTabKey} ></MyTabs>
        </Content>
        <Footer style={{ textAlign: 'center' }}>Ant Design ©2018 Created by Ant UED</Footer>
      </Layout>
    </Layout>
  );
}
