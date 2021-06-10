<template>
  <div v-if="useIframe">
    <iframe ref="frame" :src="src"></iframe>
  </div>
  <div v-else>
    <keep-alive>
      <component :is="comp"></component>
    </keep-alive>
  </div>
</template>

<script lang="ts">
import api, { MsgTransfer } from "../api";
import { ref, onMounted } from "vue";

export default {
  props: {
    useIframe: {
      type: Boolean,
      default: false
    },
    src: String, //如果使用iframe，则表示url地址,否则无意义
    comp: Object //如果不使用iframe，则表示一个组件对象
  },
  setup(props:any) {
    const frame = ref(new Object());
    onMounted(() => {
      if (props.useIframe) {
        const f = frame.value as HTMLIFrameElement;
        if (f.contentWindow === null) return;
        const transfer = new MsgTransfer(f.contentWindow, props.src);
        setTimeout(() => {
          transfer.send("info", {
            sessionID: "sdfsdf",
            pluginID: "adfasfad123123"
          });
        }, 1000);
      }
    });
    return { frame };
  }
};
</script>