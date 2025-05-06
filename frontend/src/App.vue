<template>
    <NavigationBar></NavigationBar>
    <div id="app">
        <router-view />
    </div>
</template>

<script setup>
import NavigationBar from "@/components/NavigationBar.vue";
</script>

<style>
/* 全局样式 */
body {
    margin: 0;
    padding: 0;
}
</style>
