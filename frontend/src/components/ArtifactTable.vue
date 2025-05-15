<script setup>
import {defineProps, defineExpose, ref} from 'vue'
import {useRouter} from "vue-router";

const router = useRouter()
const tableWrapper = ref(null)

const goToDetail = (id) => {
    router.push(`/detail/${id}`)
}

defineProps({
    artifacts: Array
})

defineExpose({tableWrapper})
</script>

<template>
    <div class="artifact-table" ref="tableWrapper">
        <el-table :data="artifacts" stripe style="width: 100%" height="600">
            <el-table-column label="图片" width="200">
                <template #default="{ row }">
                    <div style="cursor: pointer" @click="goToDetail(row.id)">
                        <el-image
                            :src="row.image"
                            style="width: 100%; height: auto; object-fit: cover;"
                            v-if="row.image"
                        ></el-image>
                        <span v-else>暂无图片</span>
                    </div>
                </template>
            </el-table-column>
            <el-table-column label="名称" width="180">
                <template #default="{ row }">
                            <span style="cursor: pointer" @click="goToDetail(row.id)">
                                {{ row.name }}
                            </span>
                </template>
            </el-table-column>
            <el-table-column label="类型/材质" width="150">
                <template #default="{ row }">
                    <div>{{ row.type }} / {{ row.matrials }}</div>
                </template>
            </el-table-column>
            <el-table-column prop="description" label="描述" width="180">
            </el-table-column>
            <el-table-column label="朝代/作者" width="150">
                <template #default="{ row }">
                    <div>{{ row.dynasty }} / {{ row.author }}</div>
                </template>
            </el-table-column>
            <el-table-column prop="size" label="大小" width="150">
            </el-table-column>
            <el-table-column prop="museum" label="博物馆"></el-table-column>
        </el-table>
    </div>
</template>

<style scoped>
.artifact-table {
    margin: 20px auto;
}
</style>