<template>
  <div class="detail">
    <div class="main">
      <div class="left" ref="leftSide">
        <div class="l-img">
          <img :src="imageSrc" :style="{ transform: `scale(${scale})` }" alt="">
        </div>
        <div class="bm" ref="leftBm">
          <ul>
            <li @click="zoomIn">
              <h5>Zoom In</h5>
              <img src="/image/zoom-in.png" alt="">
            </li>
            <li @click="zoomOut">
              <h5>Zoom Out</h5>
              <img src="/image/zoom-out.png" alt="">
            </li>
            <li>
              <h5>Thumbs Up</h5>
            </li>
            <li>
              <h5>Bookmark</h5>
            </li>
            <li>
              <h5>Views</h5>
            </li>
          </ul>
        </div>
      </div>
      <div class="right" ref="rightSide" @scroll="handleScroll">
        <div class="content">
          <div class="r-main">
            <div class="m-content">
              <h3>create_time+name</h3>
              <p>entry_time</p>
              <h3>author</h3>
              <p>region+dynasty</p>
              <p>matrials+type</p>
              <p>location</p>
            </div>

          </div>
          <div class="r-bm">
            <h1>Download,Share</h1>
            <ul>
              <li>
                <h4>Download</h4>
                <img src="/image/download.png" alt="">
              </li>
              <li>
                <h4>Share</h4>
                <img src="/image/share.png" alt="">
              </li>
            </ul>
            <div class="know">
              <h1>Description</h1>
              <p>Hottō Enmyō Kokushi, is a posthumous title bestowed upon the Zen Buddhist monk Shinchi Kakushin
                (1203–1298) by the emperor Go-Daigo. The title means “perfectly awakened national teacher of the Dharma
                lamp.” Considered a fine example of “Kamakura realism,” while downplaying detail in the body, the
                sculpture emphasizes fidelity in representing the visage of Kakushin.
              </p>
            </div>
            <div class="comment">
              <div class="title">
                <h1>Comment</h1>
                <img class="add" @click="showimage" v-show="!isShow" ref="myadd" src="/image/add.png" alt="">
                <img class="jian" v-show="isShow" @click="hideimage" ref="myjian" src="/image/jian.png" alt="">
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
</template>

<script setup name="DetailView">
import { ref } from 'vue'

// 放大、缩小功能
let scale = ref(1.0)
const imageSrc = ref('/image/dog.jpg')

function zoomIn() {
  if (scale.value <= 3) {
    scale.value += 0.2
    console.log(scale.value)
  }
}

function zoomOut() {
  if (scale.value > 1) {
    scale.value -= 0.2
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
</script>

<style scoped>
.detail {
  width: 100%;
  min-height: 88vh;
  background-color: skyblue;
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
  background-color: pink;
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
  background-color: greenyellow;
}

.right .r-main .m-content {
  width: 80%;
  margin: 20px auto;
}

.right .r-main .m-content p,
h3 {
  margin-top: 10px;
}

.right .r-bm {
  overflow: hidden;
  width: 100%;
  background-color: #ddd;
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
</style>