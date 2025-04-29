<template>
    <div>
        <!--登录-->
        <transition name="el-zoom-in-center">
            <div v-show="!show" class="transition-box">
                <!--卡片-->
                <el-card style="max-width: 480px; margin: 50px auto;" shadow="hover">
                    <!--卡片头-->
                    <template #header>
                        <div class="card-header" style="text-align: center">
                            <span style="font-size: larger">登录</span>
                        </div>
                    </template>
                    <!--表单-->
                    <el-form
                        style="max-width: 400px; margin: 10px auto;"
                        label-width="auto"
                        :size="'large'"
                        :model="form"
                        :rules="rules"
                        ref="formRef"
                        status-icon
                        router
                    >
                        <el-form-item label="手机号码" style="margin-bottom: 40px;" prop="phone_number">
                            <el-input v-model="form.phone_number" autocomplete="off"/>
                        </el-form-item>
                        <el-form-item label="密码" prop="password" style="margin-bottom: 40px;">
                            <el-input
                                v-model="form.password"
                                type="password"
                                autocomplete="off"
                                show-password
                            />
                        </el-form-item>
                    </el-form>
                    <div style="text-align: center;margin-top: 30px;">
                        <el-button color="black" :dark="isDark" @click="login"
                                   style="border-radius: var(--el-border-radius-small);width: 150px;height: 40px;">登录
                        </el-button>
                        <el-button color="black" :dark="isDark" @click="resetForm"
                                   style="border-radius: var(--el-border-radius-small);width: 150px;height: 40px;margin-left: 30px"
                                   plain>清空
                        </el-button>
                        <div style="margin-top: 10px;">
                            <el-text class="">没有账号？去
                                <el-link href="/register" style="color: black;margin-bottom:5px;" type="info">注册
                                </el-link>
                            </el-text>
                        </div>
                    </div>
                </el-card>
            </div>
        </transition>
    </div>
</template>

<script setup>
import {onMounted, ref, inject} from 'vue'
import {useRouter} from "vue-router";
import {ElMessage} from "element-plus";

const formRef = ref(null)
const router = useRouter()
const show = ref(true)
const isLoggedIn = inject('isLoggedIn')
const form = ref({
    password: '',
    phone_number: '',
})

const login = async () => {
    try {
        // console.log(phone_number, password)
        const res = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                phone_number: form.value.phone_number,
                password: form.value.password
            })
        });
        const data = await res.json();
        if (data.status === 'success') {
            // 保存到 sessionStorage
            sessionStorage.setItem('isLoggedIn', 'true');
            sessionStorage.setItem('username', data.username);
            isLoggedIn.value = true; // 更新前端响应式变量
            //弹出消息
            ElMessage({
                message: '登录成功', type: 'success',
                showClose: true, plain: false, grouping: true,
            })
            router.push('/profile'); // 登录成功后跳转到个人信息页面
        } else {
            //弹出错误消息
            ElMessage({
                message: data.message, type: 'error',
                showClose: true, plain: true, grouping: true,
            })
        }
    } catch (err) {
        console.error('网络错误', err);
        //弹出错误消息
        ElMessage({
            message: '网络错误', type: 'error',
            showClose: true, plain: true, grouping: true,
        })
    }
}

onMounted(async () => {
    //卡片出场动画
    show.value = !show.value;
});

const resetForm = () => {
    formRef.value.resetFields();
}

//表单校验规则
const rules = {
    password: [
        {required: true, message: '请输入密码', trigger: 'blur'},
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
    phone_number: [
        {required: true, message: '请输入手机号', trigger: 'blur'},
        {
            pattern: /^1[3-9]\d{9}$/,
            message: '手机号格式不正确',
            trigger: 'blur'
        }
    ]
}

</script>
