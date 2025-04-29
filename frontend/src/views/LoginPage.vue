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
                    >
                        <el-form-item label="用户名" style="margin-bottom: 40px;">
                            <el-input v-model="username" autocomplete="off"/>
                        </el-form-item>
                        <el-form-item label="密码" prop="pass" style="margin-bottom: 40px;">
                            <el-input
                                v-model="password"
                                type="password"
                                autocomplete="off"
                                show-password
                            />
                        </el-form-item>
                        <!--错误信息-->
                        <p style="color: red">{{ errorMsg }}</p>
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
                                <el-link href="#" style="color: black;margin-bottom:5px;" type="info">注册</el-link>
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

const username = ref('')
const password = ref('')
const errorMsg = ref('')
const router = useRouter()
const show = ref(true)
const isLoggedIn = inject('isLoggedIn')


const login = async () => {
    try {
        const res = await fetch('http://localhost:5000/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                username: username.value,
                password: password.value
            })
        });
        const data = await res.json();
        if (data.status === 'success') {
            // 保存到 sessionStorage
            sessionStorage.setItem('isLoggedIn', 'true');
            sessionStorage.setItem('username', username.value);
            isLoggedIn.value = true; // 更新前端响应式变量
            router.push('/profile'); // 登录成功后跳转到个人信息页面
        } else {
            errorMsg.value = data.message;
        }
        //更改isLogin

    } catch (err) {
        console.error('网络错误', err);
        errorMsg.value = '网络错误';
    }
}

onMounted(async () => {
    //卡片出场动画
    show.value = !show.value;
});

const resetForm = () => {
    username.value = '';
    password.value = '';
    errorMsg.value = '';
}

</script>

<style>

</style>
