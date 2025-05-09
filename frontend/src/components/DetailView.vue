<template>
    <div class="detail">
        <div class="main">
            <div class="left" ref="leftSide">
                <div class="l-img">
                    <img v-if="imageSrc" :src="imageSrc" :style="{ transform: `scale(${scale})` }" alt="">
                    <el-empty v-else description="无图片"/>
                </div>
                <div class="bm" ref="leftBm">
                    <ul>
                        <li @click="zoomIn" style="cursor: pointer;">
                            <h5>放大</h5>
                            <el-icon>
                                <ZoomIn/>
                            </el-icon>
                        </li>
                        <li @click="zoomOut" style="cursor: pointer;">
                            <h5>缩小</h5>
                            <el-icon>
                                <ZoomOut/>
                            </el-icon>
                        </li>
                        <li @click="updatelike" style="cursor:pointer;">
                            <h5>
                                <el-icon>
                                    <Pointer/>
                                </el-icon>
                                点赞 {{ likes_count }}
                            </h5>
                        </li>
                        <li @click="updatefavorite" style="cursor:pointer;">
                            <h5>
                                <el-icon>
                                    <Star/>
                                </el-icon>
                                收藏
                            </h5>
                        </li>
                        <li>
                            <h5>浏览记录 {{ views_count + 1 }}</h5>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="right" ref="rightSide" @scroll="handleScroll">
                <div class="content">
                    <div class="r-main">
                        <div class="m-content">
                            <h1>{{ name }}</h1>
                            <h3>{{ entry_time }}</h3>
                            <h1>{{ author }}</h1>
                            <p style="text-decoration: underline;">{{ dynasty }}</p>
                            <p>{{ matrials }}/{{ type }}</p>
                            <p style="text-decoration: underline;">{{ size }}</p>
                            <p>{{ location }}</p>
                        </div>
                    </div>
                    <div class="r-bm">
                        <h1>下载，分享</h1>
                        <ul>
                            <li @click="download" style="cursor: pointer;">
                                <h4>下载</h4>
                                <el-icon :size="20">
                                    <Download/>
                                </el-icon>
                            </li>
                            <li @click="share" style="cursor: pointer;">
                                <h4>分享</h4>
                                <el-icon :size="20">
                                    <Share/>
                                </el-icon>
                            </li>
                        </ul>
                        <div class="know">
                            <h1>描述</h1>
                            <p>
                                {{ description }}
                            </p>
                        </div>
                        <div class="comment">
                            <div class="title">
                                <h1>评论</h1>
                                <el-icon class="add" :size="30" @click="showimage" v-show="!isShow" ref="myadd">
                                    <CirclePlus/>
                                </el-icon>
                                <el-icon :size="30" class="jian" v-show="isShow" @click="hideimage" ref="myjian">
                                    <RemoveFilled/>
                                </el-icon>
                            </div>
                            <div class="c-content" v-show="isShow">
                                <div class="btn">
                                    <button>查看</button>
                                    <button>评论</button>
                                </div>
                                <textarea name="" id="" v-model="message" rows="10" cols="66"></textarea>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div class="reco">
        <div class="r-left">
            <div class="l-content">
                <img :src="imageSrc" alt="">
                <!-- <h3>推荐组件</h3>
                <p>???</p> -->
                <div class="l-content">
                    <!-- <h1>{{ create_time }}</h1> -->
                    <h1>{{ name }}</h1>
                    <h3>{{ entry_time }}</h3>
                    <h1>{{ author }}</h1>
                    <p style="text-decoration: underline;">{{ dynasty }}</p>
                    <p>{{ matrials }}/{{ type }}</p>
                    <p style="text-decoration: underline;">{{ size }}</p>
                    <p>{{ location }}</p>
                </div>
            </div>
        </div>
        <div class="r-right">
            <!-- 判断是否有返回值 -->
            <h1 v-if="!(name_list.length===0 && author_list.length===0 && dynasty_list.length===0)">相关推荐</h1>
            <h1 v-else>随机推荐</h1>
            <div class="theme">
                <div class="title">
                    <h1>主题</h1>
                </div>
                <ul class="themeul" v-if="name_list.length>0">
                    <li v-for="item in name_list" :key="item.relic_id" @click="goto_next(item.relic_id)">
                        <div v-if="item.img_url">
                            <img :src="item.img_url" alt="relic image"/>
                        </div>
                        <el-empty v-else description="没有图片"/>
                        <div>
                            <h3>{{ item.name }}</h3>
                            <p>{{ item.author }}</p>
                            <p>{{ item.dynasty }}</p>
                            <p>{{ item.description }}</p>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="author" v-if="author_list.length>0">
                <div class="title">
                    <h1>作者</h1>
                </div>
                <ul class="authorul">
                    <li v-for="item in author_list" :key="item.relic_id" @click=" goto_next(item.relic_id)">
                        <div v-if="item.img_url">
                            <img :src="item.img_url" alt="relic image"/>
                        </div>
                        <el-empty v-else description="没有图片"/>
                        <div>
                            <h3>{{ item.name }}</h3>
                            <p>{{ item.author }}</p>
                            <p>{{ item.dynasty }}</p>
                            <p>{{ item.description }}</p>
                        </div>
                    </li>
                </ul>
            </div>
            <div class="dynasty" v-if="dynasty_list.length>0">
                <div class="title">
                    <h1>朝代</h1>
                </div>
                <ul class="dynastyul">
                    <li v-for="item in dynasty_list" :key="item.relic_id" @click=" goto_next(item.relic_id)">
                        <div v-if="item.img_url">
                            <img :src="item.img_url" alt="relic image"/>
                        </div>
                        <el-empty v-else description="没有图片"/>
                        <div>
                            <h3>{{ item.name }}</h3>
                            <p>{{ item.author }}</p>
                            <p>{{ item.dynasty }}</p>
                            <p>{{ item.description }}</p>
                        </div>
                    </li>
                </ul>
            </div>
            <!-- 判断是否有返回值 -->
            <div class="rand" v-if="name_list.length===0 && author_list.length===0 && dynasty_list.length===0">
                <ul class="dynastyul">
                    <li v-for="item in randlist" :key="item.relic_id" @click=" goto_next(item.relic_id)">
                        <div v-if="item.img_url">
                            <img :src="item.img_url" alt="relic image"/>
                        </div>
                        <el-empty v-else description="没有图片"/>
                        <div>
                            <h3>{{ item.name }}</h3>
                            <p>{{ item.author }}</p>
                            <p>{{ item.dynasty }}</p>
                            <p>{{ item.description }}</p>
                        </div>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup name="DetailView">
import {ref, onMounted, watch, nextTick} from 'vue'
import axios from 'axios'
import {ElMessage} from 'element-plus'
import {useRoute, useRouter} from 'vue-router'

const route = useRoute()
let id = route.params.id
// 使用 useRoute 获取路由对象
const router = useRouter()
// 从 route.params 中获取动态参数 :id
// 放大、缩小功能
let scale = ref(1.0)
let imageSrc = ref('')
let create_time = ref('')
let name = ref('')
let entry_time = ref(null)
let author = ref('')
let dynasty = ref('')
let matrials = ref('')
let size = ref('')
let type = ref('')
let location = ref('')
let description = ref('')
let name_list = ref([])
let author_list = ref([])
let dynasty_list = ref([])
let views_count = ref(null)
let likes_count = ref(null)
let randlist = ref([])
// 页面打开渲染图片
// 父组件给子组件image_id
//根据所给的image_id查找url，根据relic_id查找到详细信息
async function detailRender(id) {
    try {
        let relicData = await axios.get('http://localhost:5000/api/detail_inform', {
            params: {relic_id: id}
        })
        const {img_url, relic_inform, namelist, authorlist, dynastylist, rand_list} = relicData.data
        imageSrc.value = img_url
        name_list.value = namelist
        console.log(name_list.value)
        author_list.value = authorlist
        console.log(author_list.value)
        console.log(authorlist.length)
        dynasty_list.value = dynastylist
        console.log(dynasty_list.value)
        randlist.value = rand_list
        console.log('rand_list', rand_list)
        create_time.value = relic_inform.create_time
        name.value = relic_inform.name
        entry_time.value = relic_inform.entry_time
        author.value = relic_inform.author
        dynasty.value = relic_inform.dynasty
        matrials.value = relic_inform.matrials
        type.value = relic_inform.type
        size.value = relic_inform.size
        location.value = relic_inform.museum_id
        description.value = relic_inform.description
        views_count.value = relic_inform.views_count
        likes_count.value = relic_inform.likes_count
        //进入页面浏览+1
        axios.put(`http://localhost:5000/api/put_view/${id}`, {
            views_count: views_count.value + 1
        })
        // 页面右侧滑动窗口滚动到顶部
        nextTick(() => {
            if (rightSide.value) {
                rightSide.value.scrollTop = 0
            }
        })
    } catch (error) {
        // 显示错误信息给用户
        ElMessage({
            message: error.response.statusText,
            type: 'false',
        })
    }
}

onMounted(() => {
    window.scrollTo(0, 0);
    detailRender(id);
})

//监听id是否改变
watch(() => route.params.id, (newvalue) => {
    window.scrollTo(0, 0);
    detailRender(newvalue);
})


//点击点赞like+1
function updatelike() {
    likes_count.value += 1
    axios.put(`http://localhost:5000/api/put_like/${id}`, {
        likes_count: likes_count.value
    })
}

//点击收藏
function updatefavorite() {

}

//放大
function zoomIn() {
    if (scale.value <= 3) {
        scale.value += 0.2
        console.log(scale.value)
    }
}

//缩小
function zoomOut() {
    if (scale.value > 1) {
        scale.value -= 0.2
    }
}

//下载
// 实现 Download 功能
function download() {
    const imageUrl = imageSrc.value;  // 获取当前图片的 URL
    if (!imageUrl) {
        ElMessage({
            message: 'No image available for download',
            type: 'error',
        });
        return;
    }
    const link = document.createElement('a');
    link.href = imageUrl;  // 设置下载链接为图片的 URL
    link.download = imageUrl.split('/').pop();  // 设置下载文件名为图片的文件名
    link.click();  // 触发下载
}

//分享
// 分享功能
function share() {
    const shareData = {
        title: name.value,
        text: description.value,
        url: window.location.href, // 分享当前页面的 URL
    };

    if (navigator.share) {
        // 如果浏览器支持 Web Share API
        navigator.share(shareData)
            .then(() => {
                ElMessage({
                    message: 'Shared successfully!',
                    type: 'success',
                });
            })
            .catch((error) => {
                ElMessage({
                    message: 'Share failed: ' + error,
                    type: 'error',
                });
            });
    } else {
        // 如果不支持 Web Share API，您可以提供一些替代方案
        ElMessage({
            message: 'Your browser does not support sharing.',
            type: 'warning',
        });
    }
}

// 评论区
let isShow = ref(false)
let message = ref('')

function showimage() {
    isShow.value = true
}

function hideimage() {
    isShow.value = false
}

// 监听右侧滚动
const leftSide = ref(null)
const rightSide = ref(null)
const leftBm = ref(null)

function handleScroll() {
    if (!rightSide.value || !leftSide.value || !leftSide.value.querySelector('.l-img')) return

    const titleEl = rightSide.value.querySelector('.comment .title')
    const lImgEl = leftSide.value.querySelector('.l-img')

    if (!titleEl || !lImgEl) return

    const titleRect = titleEl.getBoundingClientRect()
    const lImgRect = lImgEl.getBoundingClientRect()

    const isAligned = Math.abs(titleRect.top - lImgRect.top) <= 5

    if (isAligned) {
        const scrollTop = rightSide.value.scrollTop
        leftSide.value.style.overflow = 'auto'
        leftSide.value.scrollTop = scrollTop
    } else {
        leftSide.value.scrollTop = 0
        leftSide.value.style.overflow = 'hidden'
    }
}

//点击图片导向详情页
function goto_next(id) {
    console.log(id)
    router.push(`/detail/${id}`)
}


</script>

<style>
.detail {
    width: 100%;
    min-height: 88vh;
    margin-top: 20px;
}

.main {
    display: flex;
    flex-direction: row;
    height: 88vh;
    overflow: hidden;
}

.left,
.right {
    flex: 1 1 48%;
    margin: 10px;
    display: flex;
    flex-direction: column;
}

.left {
    position: sticky;
    top: 0;
    height: 100%;
    overflow: hidden;
    /* 初始不滚动 */
}

.right {
    height: 100%;
    overflow-y: auto;
}

.right::-webkit-scrollbar {
    display: none;
}

.left .l-img {
    width: 100%;
    height: 85%;
    display: flex;
    overflow: hidden;
    justify-content: center;
    background-color: #f5f5f5;
}

.left img {
    width: 80%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}

.left .bm {
    overflow: hidden;
    width: 100%;
    height: 15%;
    background-color: #ddd;
    margin-top: 10px;
}

.left .bm ul {
    display: flex;
    width: 100%;
    justify-content: space-evenly;
    align-items: center;
    padding: 0;
    margin-top: 20px;
}

.left .bm ul li {
    display: flex;
    justify-content: space-evenly;
    align-items: center;
    height: 40px;
    list-style: none;
    border: 2px solid #000;
    flex: 1;
    margin: 10px;
}

.left .bm ul li img {
    width: 20px;
    height: 20px;
    margin-left: 10px;
}

.right .content {
    width: 100%;
    height: 100%;
}

.right .r-main {
    overflow: hidden;
    width: 100%;
    height: 500px;
    background-color: #fff;
}

.right .r-main .m-content {
    width: 80%;
    margin: 20px auto;
}

/* .right .r-main .m-content h1,
h2,
p {
  margin-top: 5px;
} */

.right .r-main .m-content h1 {
    font-weight: 400;
}

.right .r-main .m-content p {
    font-size: 20px;
}

.right .r-bm {
    overflow: hidden;
    width: 100%;
    background-color: #fff;
}

.right .r-bm h1 {
    margin: 10px;
}

.right .r-bm ul {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-evenly;
    width: 100%;
    height: auto;
    padding: 0;
    margin: 0;
}

.right .r-bm ul li {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 40px;
    text-align: center;
    line-height: 40px;
    list-style: none;
    border: 2px solid #000;
    flex: 1;
    margin: 10px;
}

.right .r-bm ul li img {
    height: 20px;
    width: 20px;
    margin-left: 10px;
}

.right .r-bm .know p {
    margin-left: 10px;
}

.right .r-bm .comment {
    width: 100%;
}

.right .r-bm .comment .title {
    display: flex;
    align-items: center;
}

.right .r-bm .comment .title img {
    width: 40px;
    height: 40px;
}

.right .r-bm .comment .c-content .btn button {
    width: 50px;
    height: 30px;
    margin-left: 20px;
}

.right .r-bm .comment .c-content textarea {
    margin-left: 20px;
    margin-top: 10px;
    resize: none;
    outline: none;
}

/* 响应式布局：窄屏下变上下排列 */
@media (max-width: 800px) {
    .main {
        flex-direction: column;
        height: auto;
    }

    .left,
    .right {
        flex: 1 1 100%;
        height: auto;
    }

    .left {
        position: relative;
        overflow: visible;
    }
}

/* //recommend */
.reco {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-around;
    gap: 20px;
    width: 100%;
    margin-top: 20px;
}

.r-left {
    flex: 1 1 300px;
    display: flex;
    justify-content: center;
    width: 400px;
    height: 800px;
    background-color: #fff;
}

.r-left .l-content {
    width: 85%;
    background-color: #fff;
}

.r-left .l-content img {
    width: 100%;
    height: auto;
    object-fit: cover;
}

.r-right {
    flex: 2 1 600px;
    width: 1000px;
}

.r-right .themeul, .authorul, .dynastyul {
    margin-top: 10px;
    display: flex;
    width: 100%;
    justify-content: space-between;
    margin: 0;
    padding: 0;
}

.r-right .themeul li, .r-right .authorul li, .r-right .dynastyul li {
    list-style: none;
    flex: 1 1 200px;
}

.r-right .themeul li img, .r-right .authorul li img, .r-right .dynastyul li img {
    width: 100%;
    height: auto;
    object-fit: cover;
}

.r-right .theme,
.r-right .author,
.r-right .dynasty {
    margin: 10px;
}
</style>