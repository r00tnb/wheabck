<template>
  <el-container>
    <el-header class="header-bar">
      <my-header />
    </el-header>
    <el-container style="height: 100%">
      <el-aside width="auto">
        <side-bar-menu :data="menus" />
      </el-aside>
      <el-container>
        <el-header height="auto" class="tabs-bar-class">
          <tabs-bar />
        </el-header>
        <el-main class="main">
          <router-view v-slot="{ Component }">
            <transition name="move" mode="out-in">
              <keep-alive>
                <component :is="Component" :src="$route.meta.src" />
              </keep-alive>
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </el-container>
</template>

<script lang="ts">
import { reactive, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useI18n } from "vue-i18n";
import SideBarMenu from "../components/sidebar-menu.vue";
import TabsBar from "../components/tabs.vue";
import MyHeader from "../components/header.vue";
import { MenuItem } from "../components/components";
import About from "./About.vue";
import WebshellConnections from "./webshell_connections.vue"
import PluginView from '../components/plugin-view.vue'

export default {
  components: {
    SideBarMenu,
    MyHeader,
    TabsBar,
    PluginView
  },
  setup() {
    const router = useRouter()
    const { t } = useI18n();
    const data: MenuItem[] = [
      {
        name: t("side.menu.webshell_connections"),
        index: "webshell-connections",
        icon: "el-icon-edit"
      },
      {
        name: "test123",
        index: "test123",
        icon: "el-icon-edit"
      },
      {
        name: "sdffasdfadsf",
        index: "testtest1",
        icon: "el-icon-edit"
      }
    ];
    const menus = reactive(data);
    onMounted(() => {
      router.addRoute("Home", {
        path: "/webshell-connections",
        name: "WebshellConnections",
        component: WebshellConnections,
        meta:{
          title: t("side.menu.webshell_connections")
        }
      });
      router.addRoute("Home", {
        path: "/test123",
        name: "Test123",
        component: PluginView,
        meta:{
          title: "sdfsf",
          src: "https://localhost:8000/index.html"
        }
      });
      router.addRoute("Home", {
        path: "/testtest1",
        name: "sdfdfsdf",
        component: About,
        meta:{
          title: "水电费第三方"
        }
      });
    });

    return { menus, t };
  }
};
</script>

<style scoped>
.el-container,.el-aside {
  height: 100%;
}
.main {
  background-color: #eaeef0;
}
.header-bar {
  background-color: rgb(95, 108, 145);
  padding: 0;
  color: white;
}
.tabs-bar-class {
  margin: 10px 0 0 0;
  padding: 0;
}
</style>