<template>
    <div class="home-page">
        <el-container direction="vertical" class="p-6">

            <!--搜索栏-->
            <SearchBar @search="handleSearch"></SearchBar>

            <!--高级搜索、popular、reset-->
            <el-row :gutter="24" style="margin: 10px auto;border: 2px solid black;height: 50px;width: 85%">
                <el-col :span="2">热门</el-col>
                <el-col :span="20"></el-col>
                <el-col :span="2">带视频</el-col>
            </el-row>

            <!--grid\table切换、sortby、显示条数-->
            <el-row :gutter="24" style="margin: 10px auto;width: 85%">
                <el-col :span="3" style="margin-top: 5px">显示{{ artifacts.length }}个文物</el-col>
                <el-col :span="2" @click="clear()" style="margin-top: 5px">清空</el-col>
                <el-col :span="12"></el-col>
                <el-col :span="3" style="margin-top: 10px">
                    <el-dropdown placement="bottom">
                        <span>
                          排序方式
                          <el-icon class="el-icon--right">
                            <arrow-down/>
                          </el-icon>
                        </span>
                        <template #dropdown>
                            <el-dropdown-menu>
                                <el-dropdown-item>时间：新-旧</el-dropdown-item>
                                <el-dropdown-item>时间：旧-新</el-dropdown-item>
                                <el-dropdown-item>名称：A-Z</el-dropdown-item>
                                <el-dropdown-item>名称：Z-A</el-dropdown-item>
                            </el-dropdown-menu>
                        </template>
                    </el-dropdown>
                </el-col>
                <el-col :span="2" @click="switch2Table()" :class="['table', isgrid === false ? 'active' : 'inactive']">
                    表格
                    <el-icon>
                        <Operation/>
                    </el-icon>
                </el-col>
                <el-col :span="2" @click="switch2Grid()" :class="['grid', isgrid === true ? 'active' : 'inactive']">栅格
                    <el-icon>
                        <Menu/>
                    </el-icon>
                </el-col>
            </el-row>

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

/*grid/table切换样式*/
.table,
.grid {
    box-sizing: border-box;
    transition: margin-top 0.5s ease, border 0.5s ease;
}

.active {
    border: 2px solid black;
    padding: 10px;
    margin-top: 0;
}

.inactive {
    margin-top: 10px; /* ✅ 让未选中项略微下沉 */
    border: none;
}


/*回到顶部样式*/
:deep(.el-table__header) {
    --el-table-header-bg-color: rgba(245, 245, 245);
    --el-table-header-text-color: black;
    font-size: larger;
}
</style>
