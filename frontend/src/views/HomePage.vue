<template>
    <div class="home-page">
        <el-container direction="vertical" class="p-6">

            <!--搜索栏-->
            <SearchBar @search="handleSearch"></SearchBar>

            <!--高级搜索、popular、reset-->
            <div></div>

            <!--grid\table切换、sortby、显示条数-->
            <div></div>

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
                        <el-image v-else>
                            <template #error>
                                <div class="image-slot">
                                    <el-icon>
                                        <Picture/>
                                    </el-icon>
                                </div>
                            </template>
                        </el-image>
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
import {ref, onMounted} from 'vue'
import {useRouter} from "vue-router";
import axios from 'axios'
import SearchBar from '@/components/SearchBar.vue'

const searchQuery = ref('')
const artifacts = ref([])
const searched = ref(false)
const router = useRouter()

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

.image-slot {
    color: var(--el-text-color-secondary);
    font-size: 60px;
}

</style>
