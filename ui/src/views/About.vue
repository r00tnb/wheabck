<template>
  <div class="about">
    <h1>This is an about page</h1>
  </div>
</template>
<script lang="ts">
import api, {ResponseData, MessageHandler} from '../api'

export default {
  mounted(){
    api.send('test', {ok:123}, (data)=>{
      console.log(data)
    })
  }
}
</script>
