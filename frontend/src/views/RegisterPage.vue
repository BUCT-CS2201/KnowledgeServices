<template>
    <!--注册-->
    <transition name="el-zoom-in-center">
        <div v-show="!show" class="transition-box">
            <!--卡片-->
            <el-card style="max-width: 480px; margin: 50px auto;" shadow="hover">
                <!--卡片头-->
                <template #header>
                    <div class="card-header" style="text-align: center">
                        <span style="font-size: larger">注册</span>
                    </div>
                </template>
                <!--表单-->
                <el-form
                    ref="formRef"
                    :model="form"
                    :rules="rules"
                    style="max-width: 400px; margin: 10px auto;"
                    label-width="auto"
                    :size="'large'"
                    status-icon
                    router
                >
                    <el-form-item label="用户名" style="margin-bottom: 20px;" prop="username">
                        <el-input v-model="form.username" autocomplete="off"/>
                    </el-form-item>
                    <el-form-item label="密码" prop="password" style="margin-bottom: 20px;">
                        <el-input
                            v-model="form.password"
                            type="password"
                            autocomplete="off"
                            show-password
                        />
                    </el-form-item>
                    <el-form-item label="确认密码" prop="confirmpass" style="margin-bottom: 20px;">
                        <el-input
                            type="password"
                            v-model="form.confirmpass"
                            autocomplete="off"
                            show-password
                        />
                    </el-form-item>
                    <el-form-item label="身份证号" style="margin-bottom: 20px;" prop="id_number">
                        <el-input autocomplete="off" v-model="form.id_number"/>
                    </el-form-item>
                    <el-form-item label="电话号码" style="margin-bottom: 20px;" prop="phone_number">
                        <el-input autocomplete="off" v-model="form.phone_number"/>
                    </el-form-item>
                </el-form>
                <div style="text-align: center;margin-top: 30px;">
                    <el-button color="black" :dark="isDark" @click="register"
                               style="border-radius: var(--el-border-radius-small);width: 150px;height: 40px;">注册
                    </el-button>
                    <el-button color="black" :dark="isDark" @click="resetForm"
                               style="border-radius: var(--el-border-radius-small);width: 150px;height: 40px;margin-left: 30px"
                               plain>清空
                    </el-button>
                    <div style="margin-top: 10px;">
                        <el-text class="">已有账号？去
                            <el-link href="/login" style="color: black;margin-bottom:5px;" type="info">登录
                            </el-link>
                        </el-text>
                    </div>
                </div>
            </el-card>
        </div>
    </transition>
</template>

<script setup>
import {onMounted, ref} from 'vue'
import router from "@/router";
import {ElMessage} from "element-plus";

const formRef = ref(null)
const show = ref(true)
const form = ref({
    username: '',
    password: '',
    confirmpass: '',
    id_number: '',
    phone_number: '',
})

//表单校验规则
const rules = {
    username: [{required: true, message: '请输入用户名', trigger: 'blur'}],
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
    confirmpass: [
        {required: true, message: '请确认密码', trigger: 'blur'},
        {
            validator: (rule, value, callback) => {
                if (value !== form.value.password) {
                    callback(new Error('两次密码输入不一致'))
                } else {
                    callback()
                }
            },
            trigger: 'blur'
        }
    ],
    id_number: [
        {required: true, message: '请输入身份证号', trigger: 'blur'},
        {
            pattern: /^[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]$/,
            message: '身份证号格式不正确',
            trigger: 'blur'
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


onMounted(async () => {
    //卡片出场动画
    show.value = !show.value;
});

//清空
const resetForm = () => {
    formRef.value.resetFields();
}

// 注册
const register = () => {
    formRef.value.validate(async (valid) => {
        if (!valid) return
        try {
            const res = await fetch('http://localhost:5000/register', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    username: form.value.username,
                    password: form.value.password,
                    id_number: form.value.id_number,
                    phone_number: form.value.phone_number,
                })
            })
            const data = await res.json()
            if (data.status === 'success') {
                //弹出消息
                ElMessage({
                    message: '注册成功', type: 'success',
                    showClose: true, plain: true, grouping: true,
                })
                router.push('/login');
            } else {
                //弹出错误消息
                ElMessage({
                    message: data.message, type: 'error',
                    showClose: true, plain: true, grouping: true,
                })
            }
        } catch (err) {
            console.error('网络错误', err)
            //弹出错误消息
            ElMessage({
                message: '网络错误', type: 'error',
                showClose: true, plain: true, grouping: true,
            })
        }
    })
}

</script>

