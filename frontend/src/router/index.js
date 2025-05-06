// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import KgGraph from '@/views/KgGraph.vue'
import LoginPage from '@/views/LoginPage.vue'
import TimeLine from "@/views/TimeLine.vue";
import QA from "@/views/QA.vue"
import HomePage from "@/views/HomePage.vue";
import SelfProfile from "@/views/SelfProfile.vue";
import RegisterPage from "@/views/RegisterPage.vue";
import DetailImformation from '@/views/DetailImformation.vue';

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: LoginPage },
    { path: '/graph', component: KgGraph },
    { path: '/timeline', component: TimeLine },
    { path: '/qa', component: QA },
    { path: '/home', component: HomePage },
    { path: '/profile', component: SelfProfile },
    { path: '/register', component: RegisterPage },
    { path: '/detail', component: DetailImformation },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router
