import { createStore } from 'vuex'
import {Tab} from '../components/components'

interface AddTabsType {
  tab:Tab,
  index:number //添加到指定索引处
}

export default createStore({
  state: {
    sidebar_collapse:false,
    tabs_list:new Array<Tab>()
  },
  mutations: {
    setSidebarCollapse(state, s:boolean):void{
      state.sidebar_collapse = s
    },
    addTabs(state, paylaod:AddTabsType):void{
      state.tabs_list.splice(paylaod.index, 0, paylaod.tab)
    },
    delTabs(state, index:number){
      state.tabs_list.splice(index, 1)
    },
    cleanTabs(state){
      state.tabs_list.splice(0, state.tabs_list.length)
    },
    delOtherTabs(state, index:number){//删除除了指定索引以为其他的tab
      state.tabs_list.splice(index+1)
      state.tabs_list.splice(0, index)
    }
  },
  actions: {
  },
  modules: {
  }
})
