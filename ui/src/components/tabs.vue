<template>
  <div
    class="tabs-bar"
    @contextmenu.prevent
    @click.right="clickRightKey"
  >
    <ul>
      <li
        v-for="(tab,index) in tabs_list"
        :key="index"
        :class="{'active':isActive(tab.path), 'delimiter':isNeedDelimiter(tabs_list, index)}"
        @click.right="clickRightKeyOnTab(index, isActive(tab.path))"
      >
        <router-link
          v-if="!isActive(tab.path)"
          :to="tab.path"
          class="not-active-link"
          :title="tab.title"
        >{{tab.title}}</router-link>
        <span v-else class="active-link" :title="tab.title" >{{tab.title}}</span>
        <span @click="closeTab(index)" class="close-area">
          <i class="el-icon-close" />
        </span>
      </li>
    </ul>

    <div v-show="!contextMenu.hidden" class="context-menu-class" :style="{top: contextMenu.y+'px', left: contextMenu.x+'px'}" @mousedown.stop>
        <div
          v-show="contextMenu.closeAll"
          @click.left="closeAll();resetContextmenu()"
        >{{ $t('tabs_bar.context_menu.close_all') }}</div>
        <div
          v-show="contextMenu.closeOthers"
          @click.left="closeOthers(contextMenu.index);resetContextmenu()"
        >{{ $t('tabs_bar.context_menu.close_others') }}</div>
        <div
          v-show="contextMenu.closeCurrent"
          @click.left="closeTab(contextMenu.index);resetContextmenu()"
        >{{ $t('tabs_bar.context_menu.close_current') }}</div>
    </div>
  </div>
</template>

<script lang="ts">
import { useStore } from "vuex";
import { reactive, watch, onMounted, readonly } from "vue";
import { useRouter, RouteLocationNormalizedLoaded } from "vue-router";
import { Tab } from "./components";

export default {
  setup() {
    let store = useStore();
    let router = useRouter();
    const tabs_list = reactive(store.state.tabs_list);
    const closeTab = (index: number) => {
      const activeIndex = store.state.tabs_list.findIndex((item: Tab) => {
        return router.currentRoute.value.fullPath === item.path;
      });
      store.commit("delTabs", index);
      if (activeIndex === index) {
        while (index >= store.state.tabs_list.length) {
          index -= 1;
        }
        if (index >= 0) router.push(store.state.tabs_list[index].path);
        else router.push("/");
      }
    };
    const closeAll = () => {
      store.commit("cleanTabs");
      router.push("/");
    };
    const closeOthers = (index: number) => {
      store.commit("delOtherTabs", index);
    };
    const isActive = (path: string): boolean => {
      return path === router.currentRoute.value.fullPath;
    };
    const addTabFromRoute = (
      route: RouteLocationNormalizedLoaded,
      index: number
    ): void => {
      //将指定路由代表的标签插入到index指定的索引处
      if (
        route.fullPath === "/" ||
        store.state.tabs_list.some((item: Tab) => {
          return route.fullPath === item.path
        })
      )
        return;
      let tab: Tab = {
        name: typeof route.name === "string" ? route.name : "",
        title: typeof route.meta.title === "string" ? route.meta.title : "",
        path: route.fullPath
      };
      store.commit("addTabs", { tab, index });
    };
    const isNeedDelimiter = (tabs: Tab[], index: number) => {
      //当某个标签不活跃并且后一个标签不是活跃的时添加一个分割符样式
      if (!isActive(tabs[index].path) && index < tabs.length - 1) {
        if (!isActive(tabs[index + 1].path)) {
          return true;
        }
      }
      return false;
    };
    const contextMenu = reactive({
      index: -1,
      closeCurrent: false,
      closeOthers: false,
      closeAll: false,
      hidden: true,
      x: 0,
      y: 0
    });
    const resetContextmenu = () => {
      contextMenu.index = -1;
      contextMenu.closeCurrent = false;
      contextMenu.closeOthers = false;
      contextMenu.closeAll = false;
      contextMenu.hidden = true;
      contextMenu.x = 0;
      contextMenu.y = 0;
    };
    const clickRightKey = (e:MouseEvent)=>{
        contextMenu.hidden = false
        contextMenu.closeAll = true
        contextMenu.x = e.clientX
        contextMenu.y = e.clientY
    }
    const clickRightKeyOnTab = (index:number, active:boolean)=>{
        contextMenu.index = index
        contextMenu.closeOthers = active && store.state.tabs_list.length>1
        contextMenu.closeCurrent = true
    }
    watch(router.currentRoute, (newValue, oldValue) =>
      addTabFromRoute(
        newValue,
        1 +
          store.state.tabs_list.findIndex((item: Tab) => {
            return oldValue.fullPath === item.path;
          })
      )
    );
    onMounted(()=>{
        window.addEventListener('mousedown', (e)=>{
            if(e.button === 0){//点击鼠标左键则隐藏右键菜单
                resetContextmenu()
            }
        })
    })
    return {
      tabs_list,
      closeTab,
      isActive,
      isNeedDelimiter,
      contextMenu,
      closeAll,
      closeOthers,
      resetContextmenu,
      clickRightKey,
      clickRightKeyOnTab
    };
  }
};
</script>

<style scoped>
.tabs-bar {
  width: 100%;
  height: 100%;
  background-color: #fefefe;
}
.tabs-bar ul {
  list-style: none;
}
.tabs-bar li {
  display: block;
  float: left;
  padding: 5px;
  height: 100%;
  position: relative;
}
.delimiter::after {
  content: "";
  position: absolute;
  top: auto;
  left: auto;
  bottom: auto;
  right: 0;
  height: 60%;
  width: 1px;
  background-color: black;
}
.active {
  background-color: #eaeef0;
  border-top-left-radius: 4px;
  border-top-right-radius: 4px;
}

.close-area {
  cursor: pointer;
  margin: auto 0 auto 10px;
}
.close-area:hover {
  color: #4091ff;
}
.active-link {
  cursor: default;
}
.not-active-link {
  cursor: pointer;
  max-width: 50em;
  overflow: hidden;
  white-space: nowrap;
  display: inline-flex;
}
.context-menu-class {
    position: absolute;
    background-color: white;
}
.context-menu-class div {
    border-style: outset;
    border-width: 1px;
    padding: 5px;
    text-align: center;
}
.context-menu-class div:hover {
    color: #4091ff;
    cursor: pointer;
}
.context-menu-class div:first-child {
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}
.context-menu-class div:last-child {
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
}
</style>