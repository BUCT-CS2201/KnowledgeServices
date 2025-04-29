// src/main.js
import {createApp, ref} from 'vue'
import App from './App.vue'
import router from './router'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const app = createApp(App)
// 创建登录状态变量并注入全局
const isLoggedIn = ref(sessionStorage.getItem('isLoggedIn') === 'true');
app.provide('isLoggedIn', isLoggedIn);
app.use(ElementPlus)
app.use(router)
app.mount('#app')

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
