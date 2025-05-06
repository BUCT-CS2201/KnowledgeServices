<script setup>
import {ref} from "vue";

const searchQuery = ref('')
</script>

<template>
    <!--搜索栏-->
    <div style="margin-top: 50px">
        <el-row :gutter="10">
            <el-col :span="2"></el-col>
            <!--搜索框-->
            <el-col :span="15" align="center">
                <input style="height: 60px;width: 100%;font-size: xxx-large;margin-top: 10px;border: none;"
                       v-model="searchQuery"
                       placeholder="文物搜索..." @keyup.enter="fetchArtifacts" clearable>
            </el-col>
            <!--限制条件-->
            <el-col :span="2" align="center">
                <el-dropdown trigger="click"
                             style="display: flex; align-items: center; justify-content: center; height: 100%;">
                    <span class="el-dropdown-link">
                      限制
                      <el-icon class="el-icon--right">
                        <arrow-down/>
                      </el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item>艺术家</el-dropdown-item>
                            <el-dropdown-item>标题</el-dropdown-item>
                            <el-dropdown-item>描述</el-dropdown-item>
                            <el-dropdown-item>类型</el-dropdown-item>
                            <el-dropdown-item>含视频</el-dropdown-item>
                            <el-dropdown-item>朝代</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </el-col>
            <!--搜索按钮-->
            <el-col :span="3" align="center">
                <el-button @click="$emit('search', searchQuery)"
                           style="border-radius: var(--el-border-radius-small);background-color: black;width: 70%;
                               height: 70px;">
                    <el-icon style="color: white;font-size: 32px;">
                        <Search/>
                    </el-icon>
                </el-button>
            </el-col>
            <el-col :span="2"></el-col>
        </el-row>
        <!--分割线-->
        <el-divider style="border-color: black;width: 85%;margin: 5px auto;border-width: 2px;"></el-divider>
    </div>
</template>

<style scoped>

</style>