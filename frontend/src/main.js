// src/main.js
import { createApp, ref } from 'vue'
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

// 在Vue实例创建前覆盖ResizeObserver
const originalResizeObserver = window.ResizeObserver;
window.ResizeObserver = class {
    constructor(callback) {
        this.observer = new originalResizeObserver((...args) => {
            requestAnimationFrame(() => callback(...args));
        });
    }
    observe() { this.observer.observe(...arguments); }
    unobserve() { this.observer.unobserve(...arguments); }
    disconnect() { this.observer.disconnect(); }
};

// 添加全局错误过滤
window.addEventListener('error', e => {
    if (/ResizeObserver/.test(e.message)) e.stopImmediatePropagation();
});

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}
