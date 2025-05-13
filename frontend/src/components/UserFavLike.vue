<script setup>
import router from "@/router";

// eslint-disable-next-line no-undef
defineProps({
    favorites: Array,
    likes: Array,
    comments: Array,
    browse: Array
})

const goToDetail = (id) => {
    router.push(`/detail/${id}`)
}
</script>

<template>
    <!-- 菜单栏 -->
    <el-tabs type="border-card" class="demo-tabs">
        <!--点赞-->
        <el-tab-pane label="Like">
            <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><Pointer/></el-icon>
                    <span>点赞</span>
                  </span>
            </template>
            <div v-if="likes.length>0">
                <div v-for="item in likes" :key="item.relic_id" style="margin-bottom: 16px">
                    <el-card shadow="hover" @click="goToDetail(item.relic_id)">
                        <div style="font-size: large;margin: 0 0 10px 10px">{{ item.name }}</div>
                        <el-row :gutter="24">
                            <el-col :span="5">
                                <el-image :src="item.img_url"
                                          v-if="item.img_url"></el-image>
                                <el-empty :image-size="70" style="" v-else description="无图片"></el-empty>
                            </el-col>
                            <el-col :span="19">
                                <div>类型：{{ item.type }}</div>
                                <div>材料：{{ item.matrials }}</div>
                                <div>朝代：{{ item.dynasty }}</div>
                                <div>作者：{{ item.author }}</div>
                                <div>所属博物馆：{{ item.museum_name }}</div>
                            </el-col>
                        </el-row>
                    </el-card>
                </div>
            </div>
            <el-empty v-else description="暂无数据"></el-empty>
        </el-tab-pane>
        <!--收藏-->
        <el-tab-pane label="Favorate">
            <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><Star/></el-icon>
                    <span>收藏</span>
                  </span>
            </template>
            <div v-if="favorites.length>0">
                <div v-for="item in favorites" :key="item.relic_id" style="margin-bottom: 16px">
                    <el-card shadow="hover" @click="goToDetail(item.relic_id)">
                        <div style="font-size: large;margin: 0 0 10px 10px">{{ item.name }}</div>
                        <el-row :gutter="24">
                            <el-col :span="5">
                                <el-image :src="item.img_url"
                                          v-if="item.img_url"></el-image>
                                <el-empty :image-size="70" style="" v-else description="无图片"></el-empty>
                            </el-col>
                            <el-col :span="19">
                                <div>类型：{{ item.type }}</div>
                                <div>材料：{{ item.matrials }}</div>
                                <div>朝代：{{ item.dynasty }}</div>
                                <div>作者：{{ item.author }}</div>
                                <div>所属博物馆：{{ item.museum_name }}</div>
                            </el-col>
                        </el-row>
                    </el-card>
                </div>
            </div>
            <el-empty v-else description="暂无数据"></el-empty>
        </el-tab-pane>
        <!--浏览记录-->
        <el-tab-pane label="browse">
            <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><MessageBox/></el-icon>
                    <span>浏览历史</span>
                  </span>
            </template>
            <div v-if="browse.length>0">
                <div v-for="item in browse" :key="item.relic_id" style="margin-bottom: 16px">
                    <el-card shadow="hover" @click="goToDetail(item.relic_id)">
                        <div style="font-size: large;margin: 0 0 10px 10px">{{ item.name }}</div>
                        <el-row :gutter="24">
                            <el-col :span="5">
                                <el-image :src="item.img_url"
                                          v-if="item.img_url"></el-image>
                                <el-empty :image-size="70" style="" v-else description="无图片"></el-empty>
                            </el-col>
                            <el-col :span="19">
                                <div>类型：{{ item.type }}</div>
                                <div>材料：{{ item.matrials }}</div>
                                <div>朝代：{{ item.dynasty }}</div>
                                <div>作者：{{ item.author }}</div>
                                <div>所属博物馆：{{ item.museum_name }}</div>
                            </el-col>
                        </el-row>
                    </el-card>
                </div>
            </div>
            <el-empty v-else description="暂无数据"></el-empty>
        </el-tab-pane>
        <!--评论-->
        <el-tab-pane label="Comment">
            <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><ChatDotSquare/></el-icon>
                    <span>评论</span>
                  </span>
            </template>
            <div v-if="comments.length>0">
                <div v-for="item in comments" :key="item.relic_id" style="margin-bottom: 16px">
                    <el-card shadow="hover" @click="goToDetail(item.relic_id)">
                        <div style="font-size: large;margin: 0 0 10px 10px">{{ item.name }}</div>
                        <el-row :gutter="24">
                            <el-col :span="5">
                                <el-image :src="item.img_url"
                                          v-if="item.img_url"></el-image>
                                <el-empty :image-size="70" style="" v-else description="无图片"></el-empty>
                            </el-col>
                            <el-col :span="19">
                                <div>类型：{{ item.type }}</div>
                                <div>材料：{{ item.matrials }}</div>
                                <div>朝代：{{ item.dynasty }}</div>
                                <div>作者：{{ item.author }}</div>
                                <div>所属博物馆：{{ item.museum_name }}</div>
                            </el-col>
                        </el-row>
                    </el-card>
                </div>
            </div>
            <el-empty v-else description="暂无数据"></el-empty>
        </el-tab-pane>
    </el-tabs>
</template>

<style scoped>
.el-empty {
    --el-empty-padding: 10px 0;
}
</style>