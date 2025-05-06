<script setup>
import {ref, watch, inject} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {UserFilled, HomeFilled, DocumentAdd} from '@element-plus/icons-vue'

// 登录状态
const isLoggedIn = inject('isLoggedIn')

const router = useRouter()
const route = useRoute()

// 当前激活项，使用当前路由 path
const activeIndex = ref(route.path)

watch(
    () => route.path,
    (newPath) => {
        activeIndex.value = newPath
    }
)

// 路由跳转逻辑
const handleSelect = (index) => {
    router.push(index)
}
</script>

<template>
    <el-menu
        mode="horizontal"
        :ellipsis="false"
        :default-active="activeIndex"
        @select="handleSelect"
        active-text-color="#000"
        router
    >
        <el-menu-item class="home" index="/home">海外文物知识服务子系统
        </el-menu-item>
        <el-menu-item index="/graph" style="margin-left: auto">知识图谱</el-menu-item>
        <el-menu-item index="/timeline">历史时间线</el-menu-item>
        <el-menu-item index="/qa" style="margin-right: auto">知识问答</el-menu-item>
        <template v-if="!isLoggedIn">
            <el-menu-item index="/login" style="margin-left: auto">
                <el-icon>
                    <UserFilled/>
                </el-icon>
                登录
            </el-menu-item>
            <el-menu-item index="/register">
                <el-icon>
                    <DocumentAdd/>
                </el-icon>
                注册
            </el-menu-item>
        </template>
        <template v-else>
            <el-menu-item index="/profile" style="margin-left: auto">
                <el-icon>
                    <HomeFilled/>
                </el-icon>
                个人信息
            </el-menu-item>
        </template>
    </el-menu>
</template>

<style scoped>
.el-menu--horizontal {
    --el-menu-horizontal-height: 70px;
    --el-menu-hover-text-color: grey;
    --el-menu-hover-bg-color: white;
}

.home {
    margin: auto 20px;
    font-size: larger;
    border-bottom: none !important;
}
</style>