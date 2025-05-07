<script setup>
import {defineProps} from 'vue'
import {useRouter} from "vue-router";

const router = useRouter()

defineProps({
    artifacts: Array
})

const goToDetail = (id) => {
    router.push(`/detail/${id}`)
}
</script>

<template>
    <div class="artifact-grid">
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
</template>

<style scoped>
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

</style>