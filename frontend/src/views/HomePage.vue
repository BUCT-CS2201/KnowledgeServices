<template>
    <div class="home-page">
        <el-container direction="vertical" class="p-6">

            <!--搜索栏-->
            <SearchBar @search="handleSearch" :onAddTag="addTag" :fetch="fetchArtifacts"></SearchBar>

            <!--高级搜索、popular、reset-->
            <div class="popularbox" style="margin: 10px auto;">
                <el-row :gutter="24">
                    <el-col :span="2" @click="switchShowPopular()">热门
                        <el-icon v-if="!isShowPop" style="margin-left: 5px;">
                            <ArrowDown/>
                        </el-icon>
                        <el-icon v-else style="margin-left: 5px;">
                            <ArrowUp/>
                        </el-icon>
                    </el-col>
                    <el-col :span="19"></el-col>
                    <!--高级搜索-->
                    <el-col :span="3" style="margin:auto 0;">
                        <el-link @click="dialogVisible = true">高级搜索
                            <el-icon class="el-icon--right">
                                <Setting/>
                            </el-icon>
                        </el-link>
                    </el-col>
                </el-row>
                <!--热门 静态按钮-->
                <div v-if="isShowPop" style="margin-top: 10px">
                    <el-button round @click="addTag('仰韶文化')" color="black" size="small">仰韶文化</el-button>
                    <el-button round @click="addTag('作者不详')" color="black" size="small">作者不详</el-button>
                    <el-button round @click="addTag('纸本水墨')" color="black" size="small">纸本水墨</el-button>
                    <el-button round @click="addTag('山水')" color="black" size="small">山水</el-button>
                    <el-button round @click="addTag('含视频')" color="black" size="small">含视频</el-button>
                </div>
            </div>

            <!--搜索标签-->
            <div class="tags" style="margin: 10px auto;">
                <el-tag v-for="(tag,index) in selectedTags" :key="index" round closable size="large"
                        @close="removeTag(tag)" style="margin: 5px" color="pink" type="danger">{{ tag }}
                </el-tag>
                <el-link v-if="selectedTags.length > 0" style="margin-left: 5px" @click="reset()">重置</el-link>
            </div>

            <SearchModal v-if="dialogVisible" @addTags="handleAddTags" @close="dialogVisible = false">
            </SearchModal>

            <!--grid/table切换栏-->
            <GridTable :len="artifacts.length" ref="GridTableRef" :onAddTag="addTag"></GridTable>

            <!--栅格展示视图-->
            <ArtifactGrid v-if="isgrid" :artifacts="artifacts"></ArtifactGrid>
            <!--表格展示视图-->
            <ArtifactTable v-else ref="tableComponent" :artifacts="artifacts"></ArtifactTable>

            <!--搜索结果为空-->
            <div v-if="artifacts.length === 0 && searched" class="text-gray-500" style="margin: 0 auto">
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
import {ref, onMounted, computed} from 'vue'
import axios from 'axios'
import SearchBar from '@/components/SearchBar.vue'
import ArtifactGrid from "@/components/ArtifactGrid.vue";
import ArtifactTable from "@/components/ArtifactTable.vue";
import GridTable from "@/components/GridTable.vue";
import {ElMessage} from "element-plus";
import qs from 'qs';
import SearchModal from "@/components/SearchModal.vue";

const searchQuery = ref('')
const artifacts = ref([])
const searched = ref(false)
const GridTableRef = ref(true)
const isShowPop = ref(false)
const selectedTags = ref([])
const dialogVisible = ref(false)

//控制栅格/表格展示
const isgrid = computed(() => {
    return GridTableRef.value.isgrid ?? true;
});

//获取搜索内容
const handleSearch = (query) => {
    searchQuery.value = query
    fetchArtifacts(query)
}

//挂载
onMounted(() => {
    fetchArtifacts();
    // 检查 URL Hash，如果包含 #table 则强制表格视图
    if (window.location.hash === '#table') {
        isgrid.value = false;
    }
});

//获取文物信息
const fetchArtifacts = async () => {
    searched.value = true
    //普通搜索
    const sortOptions = ['时间：新-旧', '时间：旧-新', '名称：A-Z', '名称：Z-A']
    const conditionOptions = ['仅限作者', '仅限标题', '仅限描述', '仅限类型', '仅限朝代', '仅限材料', '仅限尺寸']

    let queryParams = {
        q: '',
        sort: '',
        condition: '',
        author: '',
        name: '',
        museum: '',
        after: '',
        before: '',
        type: '',
        dynasty: '',
        matrials: '',
        popular: [],
    }

    //处理普通搜索标签
    for (const tag of selectedTags.value) {
        if (sortOptions.includes(tag)) {
            queryParams.sort = tag
        } else if (conditionOptions.includes(tag)) {
            queryParams.condition = tag.replace('仅限', '')
        } else if (tag.startsWith('搜索：')) {
            queryParams.q = tag.replace('搜索：', '')
            //处理高级搜索标签
        } else if (tag.startsWith('作者：')) {
            queryParams.author = tag.replace('作者：', '')
        } else if (tag.startsWith('名称：')) {
            queryParams.name = tag.replace('名称：', '')
        } else if (tag.startsWith('博物馆：')) {
            queryParams.museum = tag.replace('博物馆：', '')
        } else if (tag.startsWith('类型：')) {
            queryParams.type = tag.replace('类型：', '')
        } else if (tag.startsWith('材料：')) {
            queryParams.matrials = tag.replace('材料：', '')
        } else if (tag.startsWith('朝代：')) {
            queryParams.dynasty = tag.replace('朝代：', '')
        } else if (tag.startsWith('之后：')) {
            let time = tag.replace('之后：', '')
            if (time.startsWith('CE')) time = time.replace('CE', '')
            else time = '-' + time.replace('BCE', '')
            queryParams.after = time
        } else if (tag.startsWith('以前：')) {
            let time = tag.replace('以前：', '')
            if (time.startsWith('CE')) time = time.replace('CE', '')
            else time = '-' + time.replace('BCE', '')
            queryParams.before = time
        } else {
            queryParams.popular.push(tag)
        }
    }

    try {
        const response = await axios.get('http://localhost:5000/search', {
            params: queryParams,
            paramsSerializer: params => qs.stringify(params, {arrayFormat: 'repeat'})
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

//热门标签展示
const switchShowPopular = () => {
    isShowPop.value = !isShowPop.value;
}

// 添加标签（去重）
function addTag(tag, suppressFetch = false) {
    //排序互斥\限制条件互斥
    const sortOptions = ['时间：新-旧', '时间：旧-新', '名称：A-Z', '名称：Z-A']
    const conditionOptions = ['仅限作者', '仅限标题', '仅限描述', '仅限类型', '仅限朝代', '仅限材料', '仅限尺寸']
    const uniquePrefixes = ['作者：', '名称：', '博物馆：', '类型：', '材料：', '朝代：', '之后：', '以前：']

    const isSortTag = sortOptions.includes(tag)
    const isConditionTag = conditionOptions.includes(tag)
    const isSearchTag = tag.startsWith('搜索：')

    if (isSortTag) {
        // 删除已有的排序标签
        selectedTags.value = selectedTags.value.filter(t => !sortOptions.includes(t))
    } else if (isConditionTag) {
        // 删除已有的条件标签
        selectedTags.value = selectedTags.value.filter(t => !conditionOptions.includes(t))
    } else if (isSearchTag) {
        selectedTags.value = selectedTags.value.filter(t => !t.startsWith('搜索：'))
    } else {
        for (const prefix of uniquePrefixes) {
            if (tag.startsWith(prefix)) {
                selectedTags.value = selectedTags.value.filter(t => !t.startsWith(prefix))
                break
            }
        }
    }
    //去重
    if (!selectedTags.value.includes(tag)) {
        selectedTags.value.push(tag)
    }
    if (!suppressFetch) {
        fetchArtifacts();
    }
}

// 移除标签
function removeTag(tag) {
    selectedTags.value = selectedTags.value.filter(t => t !== tag);
    fetchArtifacts();
}

function reset() {
    selectedTags.value = [];
    fetchArtifacts();
}

function handleAddTags(tags) {
    tags.forEach(tag => addTag(tag, true))
    fetchArtifacts()
}

</script>

<style scoped>
.home-page {
    max-width: 1200px;
    margin: 0 auto;
}

/*回到顶部样式*/
:deep(.el-table__header) {
    --el-table-header-bg-color: rgba(245, 245, 245);
    --el-table-header-text-color: black;
    font-size: larger;
}

.popularbox {
    border: 2px solid black;
    width: 80%;
    padding: 10px 25px;
}

.tags {
    width: 80%;
    padding: 10px 25px;
}

.el-tag {
    color: black;
    border-color: black;
}

</style>
