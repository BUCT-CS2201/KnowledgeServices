<script setup>
import {inject} from "vue";
import {useRouter} from "vue-router";

const isLoggedIn = inject('isLoggedIn')
const router = useRouter()

//登出
const logout = () => {
    sessionStorage.clear();
    isLoggedIn.value = false;
    router.push('/login');
}

</script>

<template>
    <h1>个人信息</h1>
    <el-button @click="logout">登出</el-button>
</template>

<style scoped>

</style>