<template>
    <div class="home-page">
        <el-container direction="vertical" class="p-6">

            <!--搜索栏-->
            <SearchBar @search="handleSearch"></SearchBar>

            <!--高级搜索、popular、reset-->
            <div></div>

            <!--grid\table切换、sortby、显示条数-->
            <el-menu class="switch_tab" mode="horizontal" :ellipsis="false"
                     active-text-color="#000" @select="handleMenuSelect" :default-active="activeMenu">
                <el-menu-item index="1" @click.stop style="pointer-events: none; color: inherit; cursor: default;">显示
                    {{ artifacts.length }}
                    个文物
                </el-menu-item>
                <el-menu-item index="2" @click="clear()">清空</el-menu-item>
                <el-sub-menu index="3">
                    <template #title>排序方式:</template>
                    <el-menu-item index="3-1">时间：新-旧</el-menu-item>
                    <el-menu-item index="3-2">时间：旧-新</el-menu-item>
                    <el-menu-item index="3-3">名称：A-Z</el-menu-item>
                    <el-menu-item index="3-4">名称：Z-A</el-menu-item>
                </el-sub-menu>
                <el-menu-item index="4" @click="switch2Table()" :class="{ 'selected': activeMenu === '4' }">表格
                    <el-icon>
                        <Operation/>
                    </el-icon>
                </el-menu-item>
                <el-menu-item index="5" @click="switch2Grid()" :class="{ 'selected': activeMenu === '5' }">栅格
                    <el-icon>
                        <Menu/>
                    </el-icon>
                </el-menu-item>
            </el-menu>


            <div class="artifact-grid" v-if="isgrid">
                <div
                    v-for="artifact in artifacts"
                    :key="artifact.id"
                    class="artifact-card"
                    @click="goToDetail(artifact.id)"
                    style="cursor: pointer;"
                >
                    <el-card style="border: none;border-radius: var(--el-border-radius-small);" shadow="hover">
                        <el-image :src="artifact.image"
                                  v-if="artifact.image"
                                  class="artifact-image"
                                  alt="artifact image"></el-image>
                        <el-empty v-else description="无图片" :image-size=100></el-empty>
                        <el-space direction="vertical" alignment="flex-start">
                            <el-text size="large" tag="b" style="color: black">{{ artifact.type }}</el-text>
                            <el-text tag="b">{{ artifact.matrials }} &nbsp;&nbsp; {{ artifact.dynasty }}</el-text>
                            <el-text>{{ artifact.date }}</el-text>
                        </el-space>

                    </el-card>
                </div>
            </div>

            <div v-else>yes</div>

            <div v-if="artifacts.length === 0 && searched" class="text-gray-500 mt-4">
                搜索结果为空
            </div>
        </el-container>
    </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {useRouter} from "vue-router";
import axios from 'axios'
import SearchBar from '@/components/SearchBar.vue'

const searchQuery = ref('')
const artifacts = ref([])
const searched = ref(false)
const router = useRouter()
const isgrid = ref(true)
const activeMenu = ref('5')

const goToDetail = (id) => {
    router.push(`/detail/${id}`)
}

const handleSearch = (query) => {
    searchQuery.value = query
    fetchArtifacts(query)
}


onMounted(() => {
    fetchArtifacts();
})

const fetchArtifacts = async () => {
    searched.value = true
    try {
        const response = await axios.get('http://localhost:5000/search', {
            params: {q: searchQuery.value || ''}
        })
        artifacts.value = response.data.results
    } catch (error) {
        console.error('Error fetching artifacts:', error)
    }
}
const switch2Table = () => {
    activeMenu.value = '4'
    isgrid.value = false;
}

const switch2Grid = () => {
    activeMenu.value = '5'
    isgrid.value = true;
}

const handleMenuSelect = (index) => {
    activeMenu.value = index
}

const clear = () => {
    console.log('clear');
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
    margin-bottom: 10px;
}

.artifact-image {
    width: 100%;
    height: auto;
    object-fit: contain;
    display: block;
}

.el-menu--horizontal > .el-menu-item:nth-child(2) {
    margin-right: auto;
}

.switch_tab {
    --el-menu-hover-text-color: grey;
    --el-menu-hover-bg-color: white;
    border: none !important;
}

.switch_tab .el-menu-item.is-active {
    border-bottom: none;
}

.switch_tab .el-menu-item {
    transition: none;
}

.switch_tab .el-menu-item.selected {
    border: 2px solid black;
}

</style>
