// src/router/index.js
import {createRouter, createWebHistory} from 'vue-router'
import KgGraph from '@/views/KgGraph.vue'
import LoginPage from '@/views/LoginPage.vue'
import TimeLine from "@/views/TimeLine.vue";
import QA from "@/views/QA.vue"
import HomePage from "@/views/HomePage.vue";
import SelfProfile from "@/views/SelfProfile.vue";
import RegisterPage from "@/views/RegisterPage.vue";
import DetailImformation from '@/views/DetailImformation.vue';
import {ElMessage} from "element-plus";

const routes = [
    {path: '/', redirect: '/home'},
    {path: '/login', component: LoginPage},
    {path: '/graph', component: KgGraph},
    {path: '/timeline', component: TimeLine},
    {path: '/qa', component: QA},
    {path: '/home', component: HomePage},
    {path: '/profile', component: SelfProfile},
    {path: '/register', component: RegisterPage},
    {path: '/detail/:id', component: DetailImformation, meta: {requiresAuth: true}},
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

//全局前置路由守卫
router.beforeEach((to, from, next) => {
    const isLoggedIn = sessionStorage.getItem('isLoggedIn') === 'true'
    if (to.meta.requiresAuth && !isLoggedIn) {
        ElMessage({
            message: '请先登录后再操作',
            type: 'warning',
            showClose: true, plain: false, grouping: true,
        })
        next({
            path: '/login',
            query: {redirect: to.fullPath}
        })
    } else {
        next()
    }
})

export default router
