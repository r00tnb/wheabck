<template>
    <template v-if="!root">
        <template v-for="(menu, index) in data" :key="index">
            <template v-if="menu.sub">
                <el-menu-item-group v-if="menu.group" :title="menu.name">
                    <sidebar :root="false" :data="menu.sub" />
                </el-menu-item-group>
                <el-submenu v-else>
                    <i :class="menu.icon" />
                    <template #title>{{menu.name}}</template>
                    <sidebar :root="false" :data="menu.sub" />
                </el-submenu>
            </template>
            <el-menu-item v-else :index="menu.index">
                <i :class="menu.icon" />
                <template #title>{{menu.name}}</template>
            </el-menu-item>
        </template>
    </template>
    <template v-else>
        <el-menu class="sidebar-menu" :collapse="$store.state.sidebar_collapse" router collapse-transition>
            <sidebar :root="false" :data="data" />
        </el-menu>
    </template>
</template>

<script lang="ts">

export default {
    name: 'sidebar',
    props:{
        root:{
            type: Boolean,
            default: true,
            require: false
        },
        data:{
            type: Array,
            require:true
        }
    }
}
</script>
<style scoped>
.sidebar-menu {
    text-align: left;
    overflow-y:auto;
    height: 100%;
}
.sidebar-menu:not(i) {
    color: black;
    font-weight: bolder;
}
</style>