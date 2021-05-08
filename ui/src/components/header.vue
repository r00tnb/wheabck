<template>
    <el-row type="flex" align="middle">
        <el-col :span="3" class="logo">
            <div >Wheabck</div>
        </el-col>
        <el-col :span="1" @click="sidebarCollapse" class="sidebar-collapse">
            <i v-if="!$store.state.sidebar_collapse" class="el-icon-s-fold"></i>
            <i v-else class="el-icon-s-unfold"></i>
        </el-col>
    </el-row>
</template>

<script lang="ts">
import {useStore} from 'vuex'

export default {
    setup(){
        let store = useStore()
        let sidebarCollapse = ()=>{
            store.commit("setSidebarCollapse", !store.state.sidebar_collapse)
        }
        return {sidebarCollapse}
    }
}
</script>

<style scoped>
.el-row {
    height: 100%;
    padding: 0 20px;
}
.logo {
    background-color: cadetblue;
}
.sidebar-collapse {
    cursor: pointer;
    font-size: 30px;
}
</style>