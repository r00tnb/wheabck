/**
 * 所有注册过的路由才能展示在内容区的tabs组件中
 */
import { ComponentType } from 'react'
import Test from '../components/Test'
import ManageConnection from '../pages/ManageConnection'
import TestPage from '../pages/test'


export interface RouteItem {
    path: string,
    component: ComponentType
}

const defaultRoutes: RouteItem[] = [
    {
        path: "/manage-webshell-connections",
        component: ManageConnection
    },
    {
        path: "/test123",
        component: Test
    },
    {
        path: "/dashboard", component: Test
    },
    {
        path:"/testpage",
        component:TestPage
    }
]

export class RouteTable {
    routes = defaultRoutes

    /**
     * 在路由表中查找指定路由
     * @param path 路由路径
     * @returns 成功返回查找到的路由条目，否则返回undefined
     */
    public find(path: string): RouteItem | undefined {
        return this.routes.find(item => item.path === path)
    }

    /**
     * 更新路由表，有如下4种情况：
     *      1.当路由在路由表时，若不传入组件对象则删除匹配的路由
     *      2.当路由在路由表时，若传入了组件对象则更新匹配的路由
     *      3.当路由不在路由表且传入了组件对象时，添加一个新的路由
     *      4.其他情况不做任何操作
     * @param path 路由路径
     * @param component 路由对应的组件对象
     */
    public updateRoute(path: string, component?: ComponentType) {
        const index = this.routes.findIndex(item => item.path === path)
        if (index !== -1) {
            if (component) {
                //update route
                this.routes[index] = {
                    path: path,
                    component: component
                }
            } else {
                //remove route
                this.routes.splice(index, 1)
            }
        } else if (component) {
            //add route
            this.routes.push({
                path: path,
                component: component
            })
        }
    }
}

const routeTable = new RouteTable()
export { routeTable }
