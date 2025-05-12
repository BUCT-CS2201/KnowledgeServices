<script setup>

</script>

<template>
    <!-- 菜单栏 -->
    <el-tabs type="border-card" class="demo-tabs">
        <el-tab-pane label="Like">
            <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><Pointer/></el-icon>
                    <span>点赞</span>
                  </span>
            </template>
            点赞
        </el-tab-pane>
        <el-tab-pane label="Favorate">
            <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><Star/></el-icon>
                    <span>收藏</span>
                  </span>
            </template>
            收藏
        </el-tab-pane>
        <el-tab-pane label="Comment">
            <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><ChatDotSquare/></el-icon>
                    <span>评论</span>
                  </span>
            </template>
            评论
        </el-tab-pane>
    </el-tabs>
</template>

<style scoped>

</style>