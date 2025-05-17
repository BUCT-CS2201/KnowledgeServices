<script setup>
import { defineProps, ref, defineEmits, defineExpose } from "vue";
import axios from 'axios';

const searchQuery = ref('');
const loading = ref(false);

const fetchSuggestions = async (queryString, cb) => {
    try {
        loading.value = true;
        const { data } = await axios.get('http://localhost:5000/search-suggestions');

        const suggestions = Object.entries(data).flatMap(([type, values]) =>
            values.map(value => ({
                value: `${value}`,
                type: type,
                raw: value
            }))
        );

        cb(suggestions.filter(item =>
            item.raw.toLowerCase().includes(queryString.toLowerCase())
        ));
    } catch (error) {
        console.error('获取建议失败:', error);
        cb([]);
    } finally {
        loading.value = false;
    }
};

const props = defineProps({
    len: Number,
    onAddTag: Function,
    fetch: Function
})

defineEmits(['update:searchQuery'])

const submitSearchQuery = () => {
    if (searchQuery.value.trim() !== '') {
        // 搜索内容作为标签，标签内容可以自定义前缀，如 "搜索：xxx"
        props.onAddTag('搜索：' + searchQuery.value.trim(), 'search')
    }
    props.fetch(true);
}

const handleLimitClick = (field) => {
    if (searchQuery.value.trim() !== '') {
        props.onAddTag('搜索：' + searchQuery.value.trim(), 'search')
    }
    props.onAddTag('仅限' + field)
    props.fetch(true)
}

const resetSearchQuery = () => {
    searchQuery.value = ''
}

defineExpose({ resetSearchQuery })
</script>

<template>
    <!--搜索栏-->
    <div style="margin-top: 50px">
        <el-row :gutter="10">
            <el-col :span="2"></el-col>
            <!--搜索框-->
            <el-col :span="15" align="center">
                <!-- <input style="height: 60px;width: 100%;font-size: xxx-large;margin-top: 10px;border: none;"
                    v-model="searchQuery" placeholder="文物搜索..." @keyup.enter="submitSearchQuery" clearable> -->
                <el-autocomplete v-model="searchQuery" :fetch-suggestions="fetchSuggestions" placeholder="文物搜索..."
                    @select="submitSearchQuery" @keyup.enter="submitSearchQuery" clearable
                    style="height: 60px;width: 100%;font-size: xxx-large;margin-top: 10px;border: none;"
                    popper-class="search-autocomplete" :loading="loading">
                    <template #default="{ item }">
                        <div class="suggestion-item">
                            <span class="type-badge">{{ item.type }}</span>
                            {{ item.value }}
                        </div>
                    </template>
                </el-autocomplete>
            </el-col>
            <!--限制条件-->
            <el-col :span="2" align="center">
                <el-dropdown trigger="click"
                    style="display: flex; align-items: center; justify-content: center; height: 100%;">
                    <span class="el-dropdown-link">
                        限制
                        <el-icon class="el-icon--right">
                            <arrow-down />
                        </el-icon>
                    </span>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item @click="handleLimitClick('作者')">作者</el-dropdown-item>
                            <el-dropdown-item @click="handleLimitClick('标题')">标题</el-dropdown-item>
                            <el-dropdown-item @click="handleLimitClick('描述')">描述</el-dropdown-item>
                            <el-dropdown-item @click="handleLimitClick('类型')">类型</el-dropdown-item>
                            <el-dropdown-item @click="handleLimitClick('朝代')">朝代</el-dropdown-item>
                            <el-dropdown-item @click="handleLimitClick('材料')">材料</el-dropdown-item>
                            <el-dropdown-item @click="handleLimitClick('尺寸')">尺寸</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </el-col>
            <!--搜索按钮-->
            <el-col :span="3" align="center">
                <el-button @click="() => { submitSearchQuery(); $emit('search', searchQuery) }" style="border-radius: var(--el-border-radius-small);background-color: black;width: 70%;
                               height: 70px;">
                    <el-icon style="color: white;font-size: 32px;">
                        <Search />
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
:deep(.el-input__wrapper) {
    height: 60px;
    padding: 0 15px;
    box-shadow: none !important;
    border: none !important;
    outline: none !important;
}

:deep(.el-input__inner) {
    font-size: xxx-large;
    font-family: "Georgia", "Times New Roman", Times, serif;
    border: none;
    height: 100% !important;
    line-height: 60px !important;
    /* 与容器高度一致 */
    padding: 0 !important;
}
</style>