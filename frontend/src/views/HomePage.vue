<template>
    <div class="home-page">
        <el-container direction="vertical" class="p-6">

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
                        <el-button @click="fetchArtifacts"
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

            <!--高级搜索、popular、reset-->
            <div></div>

            <!--grid\table切换、sortby、显示条数-->
            <div></div>

            <div class="artifact-grid">
                <div
                    v-for="artifact in artifacts"
                    :key="artifact.id"
                    class="artifact-card"
                >
                    <el-card style="border: none;border-radius: var(--el-border-radius-small);" shadow="hover">
                        <img
                            :src="artifact.image"
                            class="artifact-image"
                            alt="artifact image"
                        />
                        <div class="font-semibold text-base mt-2">{{ artifact.type }}</div>
                        <div class="text-sm text-gray-500">{{ artifact.dynasty }}</div>
                        <div class="text-sm text-gray-500">{{ artifact.matrials }}</div>
                        <div class="text-sm text-gray-500">{{ artifact.date }}</div>
                    </el-card>
                </div>
            </div>

            <div v-if="artifacts.length === 0 && searched" class="text-gray-500 mt-4">
                No results found.
            </div>
        </el-container>
    </div>
</template>

<script setup>
import {ref} from 'vue'
import axios from 'axios'

const searchQuery = ref('')
const artifacts = ref([])
const searched = ref(false)

const fetchArtifacts = async () => {
    searched.value = true
    try {
        const response = await axios.get('http://localhost:5000/search', {
            params: {q: searchQuery.value}
        })
        artifacts.value = response.data.results
    } catch (error) {
        console.error('Error fetching artifacts:', error)
    }
}
</script>

<style scoped>
.home-page {
    max-width: 1200px;
    margin: 0 auto;
}

.artifact-grid {
    column-count: 4;
    column-gap: 20px;
    padding: 10px;
}

@media (max-width: 1200px) {
    .artifact-grid {
        column-count: 2;
    }
}

.artifact-card {
    break-inside: avoid;
    margin-bottom: 20px;
}

.artifact-image {
    width: 100%;
    height: auto;
    object-fit: contain;
    display: block;
}

</style>
