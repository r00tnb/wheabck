<template>
    <div v-if="useIframe">
        <iframe :src="src"></iframe>
    </div>
    <div v-else>
        <keep-alive>
            <component :is="comp"></component>
        </keep-alive>
    </div>
</template>

<script lang="ts">
import {onMounted} from 'vue'
export default {
    props: {
        useIframe:{
            type: Boolean,
            default: false
        },
        src:String, //如果使用iframe，则表示url地址,否则无意义
        comp:Object //如果不使用iframe，则表示一个组件对象
    }
}

</script>