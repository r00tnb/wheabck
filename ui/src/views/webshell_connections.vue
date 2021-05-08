<template>
  <el-table :data="connections" border style="width: 100%">
    <el-table-column prop="datetime" :label="$t('connections.create_datetime')" width="180"> </el-table-column>
    <el-table-column prop="type" :label="$t('connections.type')" width="180"> </el-table-column>
    <el-table-column prop="address" :label="$t('connections.webshell_address')"> </el-table-column>
    <el-table-column prop="ip" :label="$t('connections.ip')"> </el-table-column>
    <el-table-column prop="position" :label="$t('connections.position')"> </el-table-column>
    <el-table-column prop="comments" :label="$t('connections.comments')"> </el-table-column>
  </el-table>
</template>

<script>
import { defineComponent } from "vue";

export default defineComponent({
    data(){
        return {
            connections:[
                {
                    datetime: "2020-12-21 08:32:21",
                    type: "PHP",
                    address: "http://sdfsf.com/1.php",
                    ip: "127.0.0.1",
                    position: "test",
                    comments: "牛逼"
                },
                {
                    datetime: "2021-02-21 08:32:21",
                    type: "ASP_NET_CS",
                    address: "http://sdfsf.com/1df.aspx",
                    ip: "127.0.0.1",
                    position: "test",
                    comments: "牛逼"
                }
            ]
        }
    }
});
</script>
