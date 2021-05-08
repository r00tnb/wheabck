import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import ElementPlus from 'element-plus'
import { createI18n } from 'vue-i18n'
import zh from './i18n/zh'
import en from './i18n/en'
import 'element-plus/lib/theme-chalk/index.css'

const i18n = createI18n({
    locale: 'zh',
    messages: { zh, en }
})

const app = createApp(App).use(store).use(router).use(i18n).use(ElementPlus)


// 注册全局对象wheabck
import {Wheabck} from './core'
// import api from './api'
declare global {
    interface Window {
        wheabck: Wheabck;
    }
}
window.wheabck = new Wheabck(app.mount('#app'))