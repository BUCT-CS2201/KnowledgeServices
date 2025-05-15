<script setup>
import {defineProps, defineEmits} from "vue";

const props = defineProps({
    len: Number,
    onAddTag: Function,
    isgrid: Boolean
})

const emit = defineEmits(['update:isgrid'])

//切换表格/栅格视图
const switch2Table = () => {
    emit('update:isgrid', false);
    window.location.hash = 'table'; // 添加 #table
};

const switch2Grid = () => {
    emit('update:isgrid', true);
    window.location.hash = ''; // 移除 Hash（或改为 #grid）
};

</script>

<template>
    <!--grid\table切换、sortby、显示条数-->
    <el-row :gutter="24" style="margin: 10px auto;width: 85%">
        <el-col :span="3" style="margin-top: 5px">显示{{ len }}个文物</el-col>
        <el-col :span="14"></el-col>
        <el-col :span="3" style="margin-top: 10px">
            <el-dropdown placement="bottom" trigger="click">
                        <span style="margin-top: 5px;">
                          排序方式
                          <el-icon class="el-icon--right">
                            <arrow-down/>
                          </el-icon>
                        </span>
                <template #dropdown>
                    <el-dropdown-menu>
                        <el-dropdown-item @click="() => props.onAddTag('时间：新-旧')">时间：新-旧</el-dropdown-item>
                        <el-dropdown-item @click="() => props.onAddTag('时间：旧-新')">时间：旧-新</el-dropdown-item>
                        <el-dropdown-item @click="() => props.onAddTag('名称：A-Z')">名称：A-Z</el-dropdown-item>
                        <el-dropdown-item @click="() => props.onAddTag('名称：Z-A')">名称：Z-A</el-dropdown-item>
                    </el-dropdown-menu>
                </template>
            </el-dropdown>
        </el-col>
        <el-col :span="2" @click="switch2Table()" :class="['table', props.isgrid ? 'inactive' : 'active']">
            表格
            <el-icon>
                <Operation/>
            </el-icon>
        </el-col>
        <el-col :span="2" @click="switch2Grid()" :class="['grid', props.isgrid ? 'active' : 'inactive']">栅格
            <el-icon>
                <Menu/>
            </el-icon>
        </el-col>
    </el-row>
</template>

<style scoped>
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
</style>