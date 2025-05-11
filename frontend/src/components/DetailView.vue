<template>
    <div class="detail">
        <div class="main">
            <div class="left" ref="leftSide" @wheel.prevent="onWheel" @mousedown="startDrag" @mousemove="onDrag" @mouseup="endDrag" @mouseleave="endDrag">
                <div class="l-img" ref="mainImg" :style="{ cursor: isDragging ? 'grabbing' : 'grab' }">
                    <div class="image-container" ref="imageContainer">

                    </div>
                    <img v-if="imageSrc" :src="imageSrc" :style="imageStyle" alt="" ref="imgElement"
                    @mousedown="startDrag"
                    @mousemove="onDrag"
                    @mouseup="endDrag"
                    @mouseleave="endDrag">
                    <el-empty v-else description="无图片"/>
                    <!-- 放大时的局部显示框 -->
            <div v-if="scale > 1" class="zoom-rect" :style="zoomRectStyle"></div>
                </div>
                <!-- 缩略图预览框 -->
                <div v-if="imageSrc" class="thumbnail-box">
                    <div class="thumbnail" ref="thumbBox">
                    <img :src="imageSrc" />
                    <div
                        class="view-rect"
                        :style="thumbnailRectStyle"
                        @mousedown.prevent.stop="startThumbDrag"
                    ></div>
                    </div>
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
                                <el-icon v-if="islike"><Sunrise /></el-icon>
                                <el-icon v-else><Sunny /></el-icon>
                                点赞{{ likes_count }}
                            </h5>
                        </li>
                        <li @click="updatefavorite" style="cursor:pointer;">
                            <h5>
                                <el-icon v-if="isFav">
                                    <Star/>
                                </el-icon>
                                <el-icon v-else><StarFilled /></el-icon>
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
                <img :src="imageSrc" alt="" v-if="imageSrc">
                <el-empty v-else description="无图片"/>
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
            <!-- 视频 -->
            <div class="box_video" v-if="isVideo">
                <h1>视频</h1>
                <ul class="videoul">
                    <li v-for="item in videoData" :key="item.video_id">
                        <div v-if="item.video_url!==null">
                            <video :src="item.video_url" controls></video>
                        </div>
                        <el-empty v-else description="没有视频"/>
                        <div>
                            <h3>{{ item.title }}</h3>
                        </div>
                    </li>
                </ul>
            </div>
            
            <!-- 判断是否有返回值 -->
            <h1 v-if="!(name_list.length===0 && author_list.length===0 && dynasty_list.length===0)">相关推荐</h1>
            <h1 v-else>随机推荐</h1>
            <div class="theme" v-if="name_list.length>0">
                <div class="title">
                    <h1>主题</h1>
                </div>
                <ul class="themeul">
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
import {ref, onMounted, watch, nextTick,onUnmounted,computed} from 'vue'
import axios from 'axios'
import {ElMessage} from 'element-plus'
import {useRoute, useRouter} from 'vue-router'

const route = useRoute()
let id = route.params.id
// 使用 useRoute 获取路由对象
const router = useRouter()
// 从 route.params 中获取动态参数 :id
// 放大、缩小功能
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
let museum_id = ref(null)
let videoData=ref('')
let isVideo=ref(false)
//判断是否点赞
let islike = ref(false)
//判断是否收藏
let isFav=ref(false)
// 页面打开渲染图片
// 父组件给子组件image_id
//根据所给的image_id查找url，根据relic_id查找到详细信息
async function detailRender(id) {
    try {
        let relicData = await axios.get('http://localhost:5000/api/detail_inform', {
            params: {relic_id: id}
        })
        const { img_url, relic_inform, namelist, authorlist, dynastylist, rand_list,museum,video_data} = relicData.data
        console.log(museum)
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
        location.value = museum.museum_name
        museum_id.value=relic_inform.museum_id
        console.log(location.value)
        description.value = relic_inform.description
        views_count.value = relic_inform.views_count
        likes_count.value = relic_inform.likes_count
        videoData.value = video_data
        console.log(videoData.value.video_url)
        console.log(videoData.value.type)
        if (videoData.value) {
            isVideo.value=true
        }
        else {
            isVideo.value=false
        }
        
        const data = await axios.get('http://localhost:5000/api/get_thumsbup', {
            params: { relic_id: id }
    })
        console.log(data.data.user_id)
    //判断点赞
    if (data.data.user_id===null) {
        islike.value=true
    } else {
        islike.value=false
        }
        console.log(islike.value)
        //判断收藏
        if (data.data.user_favid === null) {
        isFav.value=true
        } else {
        isFav.value=false
    }
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



//监听id是否改变
watch(() => route.params.id, (newvalue) => {
    window.scrollTo(0, 0);
    detailRender(newvalue);
})

onMounted(() => {
    window.scrollTo(0, 0);
    detailRender(id);
})
// function isLike() {
//     islike.value=!islike.value
// }
//点击点赞like+1
function updatelike() {
    if (islike.value) {
        likes_count.value += 1
        console.log('+1')
    } else {
        likes_count.value -= 1
        console.log('-1')
        console.log(likes_count.value)
    }
    axios.put(`http://localhost:5000/api/put_like/${id}`, {
        likes_count: likes_count.value,
        user_id:sessionStorage.getItem('user_id'),
        islike: islike.value,
    })
    islike.value=!islike.value
}

//点击收藏
function updatefavorite() {
    axios.put(`http://localhost:5000/api/put_Fav/${id}`, {
        user_id: sessionStorage.getItem('user_id'),
        museum_id: museum_id.value,
        isFav:isFav.value
    })
    isFav.value=!isFav.value
}

//放大
// function zoomIn() {
//     if (scale.value <= 3) {
//         scale.value += 0.2
//         console.log(scale.value)
//     }
// }

//缩小
// function zoomOut() {
//     if (scale.value > 1) {
//         scale.value -= 0.2
//     }
// }
const scale = ref(1)
const posX = ref(0)
const posY = ref(0)
const isDragging = ref(false)
const dragStart = ref({ x: 0, y: 0 })
const isThumbDragging = ref(false)
const thumbStart = ref({ x: 0, y: 0 })
const imgElement = ref(null);
const mainImg = ref(null);
const thumbBox = ref(null);
const imageStyle = computed(() => ({
  transform: `scale(${scale.value}) translate(${posX.value}px, ${posY.value}px)`
}))
const thumbnailRectStyle = computed(() => {
  if (!imgElement.value || !thumbBox.value) {
    return {};
  }

  const imgWidth = imgElement.value.clientWidth;
  const imgHeight = imgElement.value.clientHeight;
  const thumbWidth = thumbBox.value.clientWidth;
  const thumbHeight = thumbBox.value.clientHeight;

  // 计算红框的大小（缩略图上的可视区域）
  const rectWidth = (thumbWidth / scale.value);
  const rectHeight = (thumbHeight / scale.value);

  // 计算红框的位置（映射 posX 和 posY 到缩略图坐标系）
  // 大图的偏移量 (posX, posY) 是相对于其原始尺寸的，缩略图需要按比例映射
  let rectLeft = (-posX.value / imgWidth) * thumbWidth;
  let rectTop = (-posY.value / imgHeight) * thumbHeight;

  // 边界检查：确保红框不会超出缩略图
  rectLeft = Math.max(0, Math.min(thumbWidth - rectWidth, rectLeft));
  rectTop = Math.max(0, Math.min(thumbHeight - rectHeight, rectTop));

  return {
    width: `${rectWidth}px`,
    height: `${rectHeight}px`,
    left: `${rectLeft}px`,
    top: `${rectTop}px`,
    border: '2px solid red',
    position: 'absolute',
  };
});
const zoomIn = () => {
  scale.value = Math.min(scale.value + 0.1, 5)
}
const zoomOut = () => {
  scale.value = Math.max(scale.value - 0.1, 0.5)
}

const startDrag = (event) => {
  isDragging.value = true;
  dragStart.value = { x: event.clientX, y: event.clientY };
};

const onWheel = (event) => {
  const delta = event.deltaY
  if (delta < 0) {
    zoomIn()
  } else {
    zoomOut()
  }
}

const onDrag = (event) => {
  if (!isDragging.value) return
  posX.value += (event.clientX - dragStart.value.x) / scale.value
  posY.value += (event.clientY - dragStart.value.y) / scale.value
  dragStart.value = { x: event.clientX, y: event.clientY }
}
const endDrag = () => {
  isDragging.value = false
}
const startThumbDrag = (event) => {
  isThumbDragging.value = true
  thumbStart.value = { x: event.clientX, y: event.clientY }
  document.addEventListener('mousemove', onThumbDrag)
  document.addEventListener('mouseup', endThumbDrag)
}
const onThumbDrag = (event) => {
  if (!isThumbDragging.value || !imgElement.value || !thumbBox.value) return;

  const thumbBoxRect = thumbBox.value.getBoundingClientRect();
  const imgWidth = imgElement.value.clientWidth;
  const imgHeight = imgElement.value.clientHeight;

  // 计算鼠标移动的增量（缩略图坐标系）
  const deltaX = event.clientX - thumbStart.value.x;
  const deltaY = event.clientY - thumbStart.value.y;

  // 将缩略图上的移动增量映射到大图的偏移量
  const newPosX = posX.value - (deltaX / thumbBoxRect.width) * imgWidth * scale.value;
  const newPosY = posY.value - (deltaY / thumbBoxRect.height) * imgHeight * scale.value;

  // 计算最大允许偏移量（确保大图不会超出容器）
  const maxX = Math.max(0, (imgWidth * scale.value - thumbBoxRect.width) / 2);
  const maxY = Math.max(0, (imgHeight * scale.value - thumbBoxRect.height) / 2);

  // 限制 posX 和 posY 在合理范围内
  posX.value = Math.max(-maxX, Math.min(maxX, newPosX));
  posY.value = Math.max(-maxY, Math.min(maxY, newPosY));

  // 更新起始位置
  thumbStart.value = { x: event.clientX, y: event.clientY };
};
const endThumbDrag = () => {
  isThumbDragging.value = false
  document.removeEventListener('mousemove', onThumbDrag)
  document.removeEventListener('mouseup', endThumbDrag)
}
onUnmounted(() => {
  // 清理监听
  document.removeEventListener('mousemove', onThumbDrag)
  document.removeEventListener('mouseup', endThumbDrag)
})
// 边界限制
watch([posX, posY, scale], () => {
  if (!imgElement.value || !mainImg.value) return;

  const imgWidth = imgElement.value.clientWidth;
  const imgHeight = imgElement.value.clientHeight;
  const containerWidth = mainImg.value.clientWidth;
  const containerHeight = mainImg.value.clientHeight;

  // 计算最大允许偏移量（确保大图不会超出容器）
  const maxX = Math.max(0, (imgWidth * scale.value - containerWidth) / 2);
  const maxY = Math.max(0, (imgHeight * scale.value - containerHeight) / 2);

  // 限制 posX 和 posY 在合理范围内
  posX.value = Math.max(-maxX, Math.min(maxX, posX.value));
  posY.value = Math.max(-maxY, Math.min(maxY, posY.value));
}, { immediate: true });
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
    user-select: none;
    transition: transform 0.3s ease;
}
.thumbnail-box {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 120px;
  height: 120px;
  border: 1px solid #ccc;
  background: #fff;
  z-index: 100;
  overflow: hidden;
}

.thumbnail {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.view-rect {
  position: absolute;
  border: 2px solid red;
  cursor: move;
  box-sizing: border-box;
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
    margin: 0;
    padding: 0;
}

.r-right .themeul li, .r-right .authorul li, .r-right .dynastyul li {
    list-style: none;
    flex: 1 1 200px;
    max-width:200px ;
    margin-right: 20px;
}

.r-right .themeul li img, .r-right .authorul li img, .r-right .dynastyul li img {
    width: 100%;
    height: auto;
    object-fit: cover;
}
.r-right .videoul li{
    list-style: none;
    flex: 1 1 200px;
    max-width: 400px;
    margin-right: 20px;
}
.r-right .videoul li video{
    width: 100%;
    height: auto;
    object-fit: cover;
    height: 400px;
}

.r-right .box_video,
.r-right .theme,
.r-right .author,
.r-right .dynasty {
    margin: 10px;
}
</style>