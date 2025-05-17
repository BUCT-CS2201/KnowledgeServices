<template>
    <el-collapse>
        <el-collapse-item name="1">
            <!-- 标题 -->
            <template #title>
                <div class="comment-title">
                    <span>评论</span>
                    <span>
                        <el-icon>
                            <Comment />
                        </el-icon>
                    </span>
                </div>
            </template>
            <!-- 内容面板 -->
            <el-button @click="userComment">我也要评论</el-button>
            <!-- 评论卡片 -->
            <el-card class="comment-card" shadow="never" v-for="comment in comments" :key="comment.comment_id">
                <div class="comment-wrapper">
                    <!-- 头像 -->
                    <el-avatar class="comment-avatar" shape="square" :size="40" :icon="UserFilled"
                        :src="`http://localhost:5000/static/avatar/${comment.user_id}.png`" />
                    <!-- 右侧文字和图片区域 -->
                    <div class="comment-content">
                        <!-- 用户名 -->
                        <div class="comment-username">{{ comment.name }}</div>

                        <!-- 评论文字 -->
                        <div class="comment-text">
                            {{ comment.content }}
                        </div>

                        <!-- 评论图片 -->
                        <div class="comment-images" v-if="comment.images.length > 0">
                            <el-image v-for="img in comment.images" :key="img" :src="`${img}`" fit="cover"
                                style="width: 80px; height: 80px; margin: 4px; border-radius: 8px"
                                :preview-src-list="comment.images" />
                        </div>
                        <!-- 操作按钮 -->
                        <div class="comment-actions">
                            <el-button size="small" text type="primary" @click="replyComment(comment.comment_id)">
                                回复{{ comment.reply_count }}
                            </el-button>
                        </div>
                    </div>
                </div>
                <!-- 子评论区域 -->
                <div class="sub-comments" v-if="comment.children && comment.children.length">
                    <div v-for="sub in comment.children" :key="sub.comment_id" class="sub-comment">
                        <div class="sub-comment-name">{{ sub.name }}</div>
                        <div class="sub-comment-content">{{ sub.content }}</div>
                    </div>
                </div>
            </el-card>
            <!--评论模态框-->
            <el-dialog v-model="DialogVisible">
                <el-form>
                    <el-form-item>
                        <!-- 文本输入 -->
                        <el-input type="textarea" v-model="message" :rows="6" placeholder="这一刻的想法..."></el-input>
                    </el-form-item>
                    <el-form-item>
                        <!-- 图片上传 -->
                        <el-upload action="" list-type="picture-card" :auto-upload="false" v-model:file-list="fileList"
                            :on-change="handleChange" :on-remove="handleRemove" :limit="9" multiple
                            :disabled="fileList.length >= 9">
                            <el-icon>
                                <Plus />
                            </el-icon>
                        </el-upload>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <el-button @click="DialogVisible = false">取消</el-button>
                    <!-- 提交按钮 -->
                    <el-button type="primary" @click="submitComment">评论</el-button>
                </template>
            </el-dialog>
            <!--回复评论模态框-->
            <el-dialog v-model="ReplyCommentVisible">
                <el-form>
                    <el-form-item>
                        <!-- 文本输入 -->
                        <el-input type="textarea" v-model="message" :rows="6" placeholder="这一刻的想法..."></el-input>
                    </el-form-item>
                </el-form>
                <template #footer>
                    <el-button @click="ReplyCommentVisible = false">取消</el-button>
                    <!-- 提交按钮 -->
                    <el-button type="primary" @click="submitReply">评论</el-button>
                </template>
            </el-dialog>
        </el-collapse-item>
    </el-collapse>
</template>

<script setup>
import { onMounted, ref, defineProps, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from "axios";
import { UserFilled } from "@element-plus/icons-vue";
import { useRoute, useRouter } from "vue-router";

const props = defineProps({
    relic_id: {
        type: Number,
        required: true
    }
})


const message = ref('')// 上传评论文字
const fileList = ref([])// 上传图片列表
const DialogVisible = ref(false)
const comments = ref([])//评论展示
const ReplyCommentVisible = ref(false)
const router = useRouter()
const route = useRoute()
const currentReplyCommentId = ref(null)

// 监听路由变化
watch(() => props.relic_id, async (newRelicId) => {
    await renderComments(newRelicId);
});

//评论渲染
async function renderComments(relic_id) {
    const res = await axios.get('http://localhost:5000/get/comments', {
        params: {
            relic_id: relic_id
        }
    })
    comments.value = res.data
}

//挂载
onMounted(() => {
    renderComments(props.relic_id);
})

//弹出评论模态框
const userComment = () => {
    if (sessionStorage.getItem('isLoggedIn')) {
        DialogVisible.value = true
    } else {
        ElMessage({
            message: '请登录后再操作', type: 'warning',
            showClose: true, plain: false, grouping: true,
        })
        router.push({
            path: '/login',
            query: { redirect: route.fullPath }
        })
    }
}


// 处理文件改变
const handleChange = (file, fileListNew) => {
    fileList.value = fileListNew
}

// 删除文件
const handleRemove = (file, fileListNew) => {
    fileList.value = fileListNew
}

//提交评论
const submitComment = async () => {
    if (!message.value && fileList.value.length === 0) {
        ElMessage({
            message: '请输入评论内容或至少上传一张图片', type: 'warning',
            showClose: true, plain: true, grouping: true,
        })
        return
    }

    const formData = new FormData()
    formData.append('text', message.value)
    formData.append('relic_id', props.relic_id)
    formData.append('user_id', sessionStorage.getItem('user_id'))
    fileList.value.forEach(file => {
        formData.append('images', file.raw)
    })

    try {
        const res = await axios.post('http://localhost:5000/user/comment', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })

        if (res.data.status === 'success') {
            ElMessage({
                message: '评论提交成功，请等待审核', type: 'success',
                showClose: true, plain: true, grouping: true,
            })
            // 清空数据
            message.value = ''
            fileList.value = []
            DialogVisible.value = false
            await renderComments(props.relic_id);
        } else {
            ElMessage({
                message: '评论失败：' + res.data.message, type: 'error',
                showClose: true, plain: true, grouping: true,
            })
        }
    } catch (error) {
        ElMessage({
            message: '提交失败：' + error.message, type: 'error',
            showClose: true, plain: true, grouping: true,
        })
    }
}

//回复评论
const submitReply = async () => {
    const res = await fetch('http://localhost:5000/user/reply', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            parent_id: currentReplyCommentId.value,
            user_id: sessionStorage.getItem('user_id'),
            content: message.value
        })
    })
    const data = await res.json()
    if (data.status === 'success') {
        ElMessage.success("回复成功，请等待审核")
        ReplyCommentVisible.value = false
        message.value = ''
        currentReplyCommentId.value = null
        await renderComments(props.relic_id);
    } else {
        ElMessage.error(data.message || '回复失败')
    }
}

//回复评论按钮
const replyComment = (commentId) => {
    if (sessionStorage.getItem('isLoggedIn')) {
        currentReplyCommentId.value = commentId
        ReplyCommentVisible.value = true
    } else {
        ElMessage({
            message: '请登录后再操作', type: 'warning',
            showClose: true, plain: false, grouping: true,
        })
        router.push({
            path: '/login',
            query: { redirect: route.fullPath }
        })
    }
}
</script>

<style scoped>
.comment-title {
    font-family: "Georgia", "Times New Roman", Times, serif;
    font-size: xx-large;
    color: black;
    margin-left: 10px;
}

.comment-wrapper {
    display: flex;
    align-items: flex-start;
}

.comment-avatar {
    margin-right: 10px;
}

.comment-content {
    flex: 1;
}

.comment-username {
    font-weight: bold;
    margin-bottom: 4px;
}

.comment-text {
    margin-bottom: 6px;
    line-height: 1.4;
}

.comment-images {
    display: flex;
    flex-wrap: wrap;
    margin-bottom: 6px;
}

.comment-actions {
    display: flex;
    gap: 12px;
}

.comment-card {
    margin: 20px 20px 20px 0;
}

.sub-comments {
    margin-left: 50px;
    border-left: 2px solid #f0f0f0;
    padding-left: 12px;
    margin-top: 12px;
}

.sub-comment {
    margin-top: 10px;
    padding: 8px 10px;
    background-color: #f9f9f9;
    border-radius: 8px;
}

.sub-comment-name {
    font-weight: bold;
    color: #409EFF;
    margin-bottom: 4px;
}

.sub-comment-content {
    line-height: 1.5;
}
</style>
