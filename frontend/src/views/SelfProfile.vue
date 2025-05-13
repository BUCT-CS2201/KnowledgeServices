<template>
    <div class="common-layout">
        <el-container>
            <el-aside width="300px" class="aside">
                <!-- 头像 -->
                <el-upload
                    class="avatar-uploader"
                    :action="`http://localhost:5000/upload_avatar/${user_id}`"
                    :show-file-list="false"
                    :on-success="handleAvatarSuccess"
                    :with-credentials="true"
                    style="text-align: center;margin: 20px auto"
                >
                    <img v-if="hasAvatar" :src="imageUrl" class="avatar" @error="onImageError"/>
                    <el-avatar shape="square" v-else :size="100">user</el-avatar>
                </el-upload>
                <!--登出-->
                <div style="text-align: center;margin: 10px auto;">
                    <el-button plain color="black" @click="logout"
                               style="border-radius: var(--el-border-radius-small);">登出
                    </el-button>
                </div>
                <!-- 信息展示 -->
                <el-descriptions title="个人信息" :column="1" label-width="70px"
                                 style="padding-left: 30px;margin: 10px 0">
                    <el-descriptions-item label="用户名">{{ userInfo.name }}</el-descriptions-item>
                    <el-descriptions-item label="手机号码">{{ maskPhone(userInfo.phone_number) }}</el-descriptions-item>
                    <el-descriptions-item label="身份证号">{{ maskIdNumber(userInfo.id_number) }}</el-descriptions-item>
                    <el-descriptions-item label="性别">
                        {{ userInfo.gender === 1 ? '男' : userInfo.gender === 0 ? '女' : '无' }}
                    </el-descriptions-item>
                    <el-descriptions-item label="年龄">{{ userInfo.age || '无' }}</el-descriptions-item>
                    <el-descriptions-item label="地址">{{ userInfo.address || '无' }}</el-descriptions-item>
                    <el-descriptions-item label="微信">{{ userInfo.wechat || '无' }}</el-descriptions-item>
                    <el-descriptions-item label="QQ">{{ userInfo.qq || '无' }}</el-descriptions-item>
                    <el-descriptions-item label="描述"></el-descriptions-item>
                    <el-descriptions-item>{{ userInfo.description || '无' }}</el-descriptions-item>
                </el-descriptions>
                <div style="text-align: center;margin-bottom: 50px">
                    <!-- 编辑信息 -->
                    <el-button color="black" plain @click="openInfoDialog"
                               style="border-radius: var(--el-border-radius-small);">
                        编辑信息
                    </el-button>
                    <!-- 修改密码 -->
                    <el-button color="black" @click="passVisible = true"
                               style="border-radius: var(--el-border-radius-small);">
                        修改密码
                    </el-button>
                </div>
                <!-- 修改信息模态框 -->
                <el-dialog title="编辑信息" v-model="InfoDialogVisible" :modal="false">
                    <el-form
                        style="max-width: 600px"
                        :model="infoForm"
                        status-icon
                        :rules="infoRules"
                        label-width="auto"
                        class="demo-ruleForm"
                        ref="infoFormRef"
                    >
                        <el-form-item label="用户名" prop="name">
                            <el-input autocomplete="off" v-model="infoForm.name"/>
                        </el-form-item>
                        <el-form-item label="简介" prop="description">
                            <el-input
                                v-model="infoForm.description"
                                :rows="2"
                                type="textarea"
                                placeholder="请输入简介"
                            />
                        </el-form-item>
                        <el-form-item label="性别：" prop="gender">
                            <el-radio-group v-model="infoForm.gender">
                                <el-radio :label="0">女</el-radio>
                                <el-radio :label="1">男</el-radio>
                            </el-radio-group>
                        </el-form-item>
                        <el-form-item label="地址：" prop="address">
                            <el-input v-model="infoForm.address"/>
                        </el-form-item>
                        <el-form-item label="年龄：" prop="age">
                            <el-input-number type="number" :min="0" v-model="infoForm.age"/>
                        </el-form-item>
                        <el-form-item label="微信：" prop="wechat">
                            <el-input v-model="infoForm.wechat"/>
                        </el-form-item>
                        <el-form-item label="QQ：" prop="qq">
                            <el-input v-model="infoForm.qq"/>
                        </el-form-item>
                    </el-form>
                    <template #footer>
                        <div class="dialog-footer">
                            <el-button @click="InfoDialogVisible = false" plain color="black"
                                       style="border-radius: var(--el-border-radius-small);">取消
                            </el-button>
                            <el-button type="primary" @click="submitInfoChange" color="black"
                                       style="border-radius: var(--el-border-radius-small);">
                                确认
                            </el-button>
                        </div>
                    </template>
                </el-dialog>
                <!-- 修改密码模态框 -->
                <el-dialog v-model="passVisible" title="修改密码" :modal="false" width="400px">
                    <el-form :rules="passRules" :model="passwordForm"
                             label-width="80px" ref="passwordFormRef"
                             status-icon>
                        <el-form-item label="新密码" prop="newPassword">
                            <el-input v-model="passwordForm.newPassword" type="password" autocomplete="off"/>
                        </el-form-item>
                        <el-form-item label="确认密码" prop="confirmPassword">
                            <el-input v-model="passwordForm.confirmPassword" type="password" autocomplete="off"/>
                        </el-form-item>
                    </el-form>
                    <template #footer>
                        <div class="dialog-footer">
                            <el-button @click="passVisible = false" plain color="black"
                                       style="border-radius: var(--el-border-radius-small);">取消
                            </el-button>
                            <el-button type="primary" @click="submitPasswordChange" color="black"
                                       style="border-radius: var(--el-border-radius-small);">确认
                            </el-button>
                        </div>
                    </template>
                </el-dialog>
            </el-aside>
            <!-- 主要部分 -->
            <el-main class="el-main-demo">
                <UserFavLike
                    :favorites="favoriteInfo"
                    :likes="likeInfo"
                    :comments="commentInfo"
                    :browse="browseInfo"
                />
            </el-main>
        </el-container>
    </div>

</template>

<script setup>
import {inject, onMounted} from "vue";
import {useRouter} from "vue-router";
import {ref} from 'vue'
import {ElMessage} from 'element-plus'
import UserFavLike from "@/components/UserFavLike.vue";
import axios from "axios";

const InfoDialogVisible = ref(false)//编辑信息模态框可见性
const passVisible = ref(false)//修改密码模态框可见性
const passwordForm = ref({
    newPassword: '',
    confirmPassword: ''
})//修改密码表单内容
const infoForm = ref({
    name: '',
    description: '',
    gender: null,
    address: '',
    age: null,
    wechat: '',
    qq: ''
})//编辑信息表单内容
const passRules = {
    newPassword: [
        {required: true, message: '请输入新密码', trigger: 'blur'},
        {
            validator: (rule, value, callback) => {
                if (value.length < 6) {
                    callback(new Error('密码长度不能小于6'));
                } else {
                    callback();
                }
            }
        }
    ],
    confirmPassword: [
        {required: true, message: '请确认密码', trigger: 'blur'},
        {
            validator: (rule, value, callback) => {
                if (value !== passwordForm.value.newPassword) {
                    callback(new Error('两次密码不一致'))
                } else {
                    callback()
                }
            }
        }
    ],
}//修改密码表单验证
const infoRules = {
    name: [
        {required: true, message: '用户名不能为空', trigger: 'blur'}
    ]
}//编辑信息表单验证
const passwordFormRef = ref(null)//修改密码表单
const infoFormRef = ref(null)//编辑信息表单

const user_id = sessionStorage.getItem("user_id")
const isLoggedIn = inject('isLoggedIn')
const router = useRouter()
const imageUrl = ref(`http://localhost:5000/static/avatar/${user_id}.png`);//获取用户头像
const userInfo = ref({})//用户信息展示
const favoriteInfo = ref({})//用户收藏展示
const likeInfo = ref({})//用户点赞展示
const commentInfo = ref({})//用户评论展示
const browseInfo = ref({})//用户浏览记录展示
const hasAvatar = ref(true)

// 上传成功后，强制刷新图片（避免缓存）
const handleAvatarSuccess = () => {
    // 加时间戳避免缓存
    imageUrl.value = `http://localhost:5000/static/avatar/${user_id}.png?t=${Date.now()}`;
};

//头像加载失败
function onImageError() {
    hasAvatar.value = false
}

//数据渲染
async function renderInfo() {
    try {
        const response = await axios.get(`http://localhost:5000/user_info/${user_id}`)
        userInfo.value = response.data.user_info
        favoriteInfo.value = response.data.favorites
        likeInfo.value = response.data.likes
        commentInfo.value = response.data.comments
        browseInfo.value = response.data.browsing_history
    } catch (error) {
        ElMessage.error("获取用户信息失败")
        console.error(error)
    }
}

//挂载
onMounted(async () => {
    renderInfo();
})

//登出
const logout = () => {
    sessionStorage.clear();
    isLoggedIn.value = false;
    router.push('/login');
}

// 脱敏手机号（如：181****0000）
const maskPhone = (phone) => {
    if (!phone) return '';
    return phone.replace(/^(\d{3})\d{4}(\d{4})$/, '$1****$2');
}

// 脱敏身份证号（如：3201**********1234）
const maskIdNumber = (id) => {
    if (!id) return '';
    return id.replace(/^(\d{4})\d{10}(\d{4})$/, '$1**********$2');
}

// 提交修改密码请求
const submitPasswordChange = async () => {
    try {
        await passwordFormRef.value.validate()

        if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
            ElMessage.error('两次密码不一致，请重新输入确认密码')
            passwordForm.value.confirmPassword = ''
            return
        }

        const response = await axios.post(`http://localhost:5000/update_password`, {
            user_id: user_id,
            new_password: passwordForm.value.newPassword
        }, {
            withCredentials: true
        })

        if (response.data.status) {
            ElMessage.success('密码修改成功！')
            passVisible.value = false
            passwordForm.value.newPassword = ''
            passwordForm.value.confirmPassword = ''
        } else {
            ElMessage.error(response.data.message || '密码修改失败')
        }
    } catch (err) {
        ElMessage.error('提交失败：' + (err.response?.data?.message || err.message))
    }
}

// 打开编辑信息时获取已有信息
const openInfoDialog = async () => {
    const data = userInfo.value
    infoForm.value = {
        name: data.name || '',
        description: data.description || '',
        gender: data.gender !== null ? Number(data.gender) : null,
        address: data.address || '',
        age: data.age || null,
        wechat: data.wechat || '',
        qq: data.qq || ''
    }
    InfoDialogVisible.value = true
    console.log(infoForm.value)
}

// 提交编辑信息
const submitInfoChange = async () => {
    await infoFormRef.value.validate()
    try {
        const response = await axios.post('http://localhost:5000/update_user_info', {
            user_id: user_id,
            ...infoForm.value
        })

        if (response.data.status === 'success') {
            ElMessage.success('用户信息更新成功')
            InfoDialogVisible.value = false
        } else {
            ElMessage.error(response.data.message || '更新失败')
        }
        renderInfo()
    } catch (err) {
        ElMessage.error('请求失败：' + err.message)
    }
}

</script>

<style scoped>
.el-upload {
    margin: 0 auto;
}

.avatar-uploader .avatar {
    width: 100px;
    height: 100px;
    display: block;
}

.el-menu-popper-demo {
    display: flex;
    justify-content: space-evenly;
}

.el-dia .title {
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center; /* 垂直居中 */
    height: 50px; /* 设置高度使内容垂直居中 */
}

.demo-ruleForm {
    width: 100%; /* 让表单宽度占满容器 */
    max-width: 600px; /* 最大宽度 */
    margin: auto; /* 自动设置外边距以实现居中 */
}

.dialog-footer {
    display: flex;
    justify-content: center;
}

.avatar-uploader .el-upload {
    border: 1px dashed var(--el-border-color);
    border-radius: 6px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
    border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
    font-size: 28px;
    color: #8c939d;
    width: 100px;
    height: 100px;
    text-align: center;
}

.el-radio__input.is-checked .el-radio__inner {
    background-color: black;
    border-color: black;
}

.el-radio__input.is-checked + .el-radio__label {
    color: black;
}

.el-radio__inner {
    border-color: black;
}

:deep(.el-radio__input.is-checked .el-radio__inner) {
    background-color: black;
    border-color: black;
}

:deep(.el-radio__input.is-checked + .el-radio__label) {
    color: black;
}

:deep(.el-radio__inner) {
    border-color: black;
}

:deep(.el-radio__input:hover .el-radio__inner) {
    border-color: black;
}

:deep(.el-radio__input.is-checked:hover .el-radio__inner) {
    background-color: black;
    border-color: black;
}

:deep(.el-radio__input:hover + .el-radio__label) {
    color: black;
}

</style>