<template>
  <div class="plugin-view">
    <keep-alive>
    <iframe ref="frame" :src="src"></iframe>
    </keep-alive>
  </div>
</template>

<script lang="ts">
import api, { MsgTransfer } from "../api";
import { ref, onMounted } from "vue";

export default {
  props: {
    src: String //iframe的url地址
  },
  setup(props: any) {
    const frame = ref(new Object());
    onMounted(() => {
      if (props.src !== undefined) {
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

<style scoped>
.plugin-view, .plugin-view>iframe {
  height: 100%;
  width: 100%;
}
</style>