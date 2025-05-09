<script setup>
import {inject} from "vue";
import {useRouter} from "vue-router";
import {ref} from 'vue'
import {ElMessage} from 'element-plus'
import {Plus} from '@element-plus/icons-vue'
// `imageUrl` 是一个响应式数据，用来存储图片的 URL
const imageUrl = ref('');

// 头像上传成功时的回调函数
const handleAvatarSuccess = (response, uploadFile) => {
    imageUrl.value = URL.createObjectURL(uploadFile.raw);
};

// 上传文件之前的校验
const beforeAvatarUpload = (rawFile) => {
    if (rawFile.type !== 'image/jpeg') {
        ElMessage.error('Avatar picture must be JPG format!');
        return false;
    } else if (rawFile.size / 1024 / 1024 > 2) {
        ElMessage.error('Avatar picture size can not exceed 2MB!');
        return false;
    }
    return true;
};
const isLoggedIn = inject('isLoggedIn')
const router = useRouter()

//登出
const logout = () => {
    sessionStorage.clear();
    isLoggedIn.value = false;
    router.push('/login');
}
//修改信息
// 表单引用
// const ruleFormRef = ref()
const dialogVisible = ref(false)
const passVisible = ref(false)
// // 年龄验证函数
// const checkAge = (rule, value, callback) => {
//   if (!value) {
//     return callback(new Error('Please input the age'))
//   }
//   setTimeout(() => {
//     if (!Number.isInteger(value)) {
//       callback(new Error('Please input digits'))
//     } else {
//       if (value < 18) {
//         callback(new Error('Age must be greater than 18'))
//       } else {
//         callback()
//       }
//     }
//   }, 1000)
// }

// // 密码验证函数
// const validatePass = (rule, value, callback) => {
//   if (value === '') {
//     callback(new Error('Please input the password'))
//   } else {
//     if (ruleForm.checkPass !== '') {
//       if (!ruleFormRef.value) return
//       ruleFormRef.value.validateField('checkPass')
//     }
//     callback()
//   }
// }

// // 确认密码验证函数
// const validatePass2 = (rule, value, callback) => {
//   if (value === '') {
//     callback(new Error('Please input the password again'))
//   } else if (value !== ruleForm.pass) {
//     callback(new Error("Two inputs don't match!"))
//   } else {
//     callback()
//   }
// }

// // 表单数据
// const ruleForm = reactive({
//   pass: '',
//   checkPass: '',
//   age: '',
// })

// // 表单验证规则
// const rules = reactive({
//   pass: [{ validator: validatePass, trigger: 'blur' }],
//   checkPass: [{ validator: validatePass2, trigger: 'blur' }],
//   age: [{ validator: checkAge, trigger: 'blur' }],
// })

// // 提交表单
// const submitForm = (formEl) => {
//   if (!formEl) return
//   formEl.validate((valid) => {
//     if (valid) {
//       console.log('submit!')
//     } else {
//       console.log('error submit!')
//     }
//   })
// }

// // 重置表单
// const resetForm = (formEl) => {
//   if (!formEl) return
//   formEl.resetFields()
// }
</script>

<template>
    <div class="common-layout">
        <el-container>
            <el-aside width="200px" class="aside">
                <h1>个人信息</h1>
                <!-- 头像 -->
                <el-upload
                    class="avatar-uploader"
                    action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
                    :show-file-list="false"
                    :on-success="handleAvatarSuccess"
                    :before-upload="beforeAvatarUpload"
                >
                    <img v-if="imageUrl" :src="imageUrl" class="avatar"/>
                    <el-icon v-else class="avatar-uploader-icon">
                        <Plus/>
                    </el-icon>
                </el-upload>

                <!-- 修改信息 -->
                <el-button plain @click="dialogVisible = true">
                    修改信息
                </el-button>
                <el-dialog v-model="dialogVisible" :modal="false" class="el-dia">
                    <div class="title">
                        <h1>用户信息修改</h1>
                    </div>
                    <el-form
                        ref="ruleFormRef"
                        style="max-width: 600px"
                        :model="ruleForm"
                        status-icon
                        :rules="rules"
                        label-width="auto"
                        class="demo-ruleForm"
                    >

                        <el-form-item label="用户名：" prop="user">
                            <el-input type="username" autocomplete="off"/>
                        </el-form-item>
                        <el-form-item label="简介：" prop="descr">
                            <el-input
                                v-model="textarea"
                                :rows="2"
                                type="textarea"
                                placeholder="Please input"
                                class="no-resize"
                            />
                        </el-form-item>
                        <el-form-item label="性别：" prop="gender">
                            <el-input/>
                        </el-form-item>
                        <el-form-item label="地址：" prop="address">
                            <el-input/>
                        </el-form-item>
                        <el-form-item label="年龄：" prop="age">
                            <el-input/>
                        </el-form-item>
                        <el-form-item label="微信：" prop="wechat">
                            <el-input/>
                        </el-form-item>
                        <el-form-item label="QQ：" prop="qq">
                            <el-input/>
                        </el-form-item>
                    </el-form>
                    <template #footer>
                        <div class="dialog-footer">
                            <el-button @click="dialogVisible = false">Cancel</el-button>
                            <el-button type="primary" @click="dialogVisible = false">
                                Confirm
                            </el-button>
                        </div>
                    </template>
                </el-dialog>
                <!-- 信息展示 -->
                <el-card style="max-width: 480px">
                    <template #header>
                        <div class="card-header">
                            <span>Card name</span>
                        </div>
                    </template>
                    <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
                    <template #footer>Footer content</template>
                </el-card>
            </el-aside>
            <!-- 主要部分 -->
            <el-main class="el-main-demo">
                <!-- 菜单栏 -->
                <el-tabs type="border-card" class="demo-tabs">
                    <el-tab-pane label="Config">
                        <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><Star/></el-icon>
                    <span>收藏</span>
                  </span>
                        </template>
                        收藏
                    </el-tab-pane>
                    <el-tab-pane label="Role">
                        <template #label>
                  <span class="custom-tabs-label">
                    <el-icon><ChatDotSquare/></el-icon>
                    <span>评论</span>
                  </span>
                        </template>
                        评论
                    </el-tab-pane>
                </el-tabs>
            </el-main>
        </el-container>
    </div>
    <el-button @click="logout">登出</el-button>
    <!-- 修改密码 -->
    <el-button plain @click="passVisible = true">
        修改密码
    </el-button>
    <el-dialog v-model="passVisible" :modal="false">
        <el-form-item label="密码：" prop="pass">
            <el-input type="password" autocomplete="off"/>
        </el-form-item>
        <template #footer>
            <div class="dialog-footer">
                <el-button @click="passVisible = false">Cancel</el-button>
                <el-button type="primary" @click="passVisible = false">
                    Confirm
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<style scoped>
.el-menu--horizontal {
    --el-menu-horizontal-height: 70px;
    --el-menu-hover-text-color: grey;
    --el-menu-hover-bg-color: white;
}

.home {
    margin: auto 20px;
    font-size: larger;
    border-bottom: none !important;
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

.el-dia {
    display: flex;
    justify-content: center;
    align-items: center;
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

</style>
<style>
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

.demo-tabs > .el-tabs__content {
    padding: 32px;
    color: #6b778c;
    font-size: 32px;
    font-weight: 600;
}

.demo-tabs .custom-tabs-label .el-icon {
    vertical-align: middle;
}

.demo-tabs .custom-tabs-label span {
    vertical-align: middle;
    margin-left: 4px;
}

.demo-ruleForm .no-resize {
    resize: none !important;
}
</style>