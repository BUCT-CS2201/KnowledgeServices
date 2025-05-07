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

            <!--栅格展示视图-->
            <ArtifactGrid v-if="isgrid" :artifacts="artifacts"></ArtifactGrid>
            <!--表格展示视图-->
            <ArtifactTable v-else ref="tableComponent" :artifacts="artifacts"></ArtifactTable>

            <!--搜索结果为空-->
            <div v-if="artifacts.length === 0 && searched" class="text-gray-500 mt-4">
                搜索结果为空
            </div>
        </el-container>
    </div>

    <!--回到顶部-->
    <el-backtop :right="100" :bottom="100" style="width: 100px" @click="scrollToTop()">
        <div style="
        width: 100px;
        background-color: black;
        line-height: 50px;
        color: white;
        font-size: medium;
        text-align: center">
            <el-icon>
                <Top/>
            </el-icon>
            回到顶部
        </div>
    </el-backtop>

</template>

<script setup>
import {ref, onMounted} from 'vue'
import axios from 'axios'
import SearchBar from '@/components/SearchBar.vue'
import ArtifactGrid from "@/components/ArtifactGrid.vue";
import ArtifactTable from "@/components/ArtifactTable.vue";
import {ElMessage} from "element-plus";

const searchQuery = ref('')
const artifacts = ref([])
const searched = ref(false)
const isgrid = ref(true)
const activeMenu = ref('5')


//获取搜索内容
const handleSearch = (query) => {
    searchQuery.value = query
    fetchArtifacts(query)
}

onMounted(() => {
    fetchArtifacts();
    // 检查 URL Hash，如果包含 #table 则强制表格视图
    if (window.location.hash === '#table') {
        isgrid.value = false;
        activeMenu.value = '4';
    }
});

//获取文物信息
const fetchArtifacts = async () => {
    searched.value = true
    try {
        const response = await axios.get('http://localhost:5000/search', {
            params: {q: searchQuery.value || ''}
        })
        artifacts.value = response.data.results
    } catch (error) {
        ElMessage({
            message: '无法获取文物信息', type: 'error',
            showClose: true, plain: true, grouping: true,
        })
        console.error('Error fetching artifacts:', error)
    }
}

//切换表格/栅格视图
const switch2Table = () => {
    activeMenu.value = '4';
    isgrid.value = false;
    localStorage.setItem('viewMode', 'table');
    window.location.hash = 'table'; // 添加 #table
};

const switch2Grid = () => {
    activeMenu.value = '5';
    isgrid.value = true;
    localStorage.setItem('viewMode', 'grid');
    window.location.hash = ''; // 移除 Hash（或改为 #grid）
};

const handleMenuSelect = (index) => {
    // 只让 Grid/Table 项触发选中样式
    if (index === '4' || index === '5') {
        activeMenu.value = index
    }
}

//清空搜索条件
const clear = () => {
    console.log('clear');
}

// 回到顶部逻辑
const tableComponent = ref(null)

const scrollToTop = () => {
    window.scrollTo({top: 0, behavior: 'smooth'})
    const wrapper = tableComponent.value?.tableWrapper
    if (wrapper) {
        const scrollWrap = wrapper.querySelector('.el-scrollbar__wrap')
        if (scrollWrap) {
            scrollWrap.scrollTo({top: 0, behavior: 'smooth'})
        }
    }
}

</script>

<style scoped>
.home-page {
    max-width: 1200px;
    margin: 0 auto;
}

/*栅格表格切换栏样式*/
.el-menu--horizontal > .el-menu-item:nth-child(2) {
    margin-right: auto;
}

/*取消原menu样式*/
.switch_tab {
    --el-menu-hover-text-color: grey;
    --el-menu-hover-bg-color: white;
    border: none !important;
}

.switch_tab .el-sub-menu__title.is-active {
    border-bottom: none;
}

.switch_tab .el-sub-menu__title {
    transition: none;
}

.switch_tab .el-menu-item.is-active {
    border-bottom: none;
}

.switch_tab .el-menu-item{
    transition: none;
}


/*grid/table被选中*/
.switch_tab .el-menu-item.selected {
    border: 2px solid black;
}

/*回到顶部样式*/
:deep(.el-table__header) {
    --el-table-header-bg-color: rgba(245, 245, 245);
    --el-table-header-text-color: black;
    font-size: larger;
}
</style>
