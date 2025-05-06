<template>
  <div class="reco">
    <div class="left">
      <div class="l-content">
        <img src="/image/dog.jpg" alt="">
        <h3>推荐组件</h3>
        <p>???</p>
      </div>
    </div>
    <div class="right">
      <div class="theme">
        <div class="title">
          <h1>Theme</h1>
        </div>
        <ul>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
        </ul>
      </div>
      <div class="author">
        <div class="title">
          <h1>Author</h1>
        </div>
        <ul>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
        </ul>
      </div>
      <div class="dynasty">
        <div class="title">
          <h1>Dynasty</h1>
        </div>
        <ul>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
          <li>
            <img src="/image/dog.jpg" alt="">
            <h3>主要内容介绍</h3>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup name="RecommendView">

</script>

<style scoped>
.reco {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  gap: 20px;
  width: 100%;
  background-color: #ca3720;
  margin-top: 20px;
}

.left {
  flex: 1 1 300px;
  display: flex;
  justify-content: center;
  width: 400px;
  height: 800px;
  background-color: #46d33c;
}

.left .l-content {
  width: 85%;
  height: 600px;
  background-color: #dce613;
}

.left .l-content img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.right {
  flex: 2 1 600px;
  width: 1000px;
  background-color: pink;
}

.right ul {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
}

.right ul li {
  list-style: none;
  flex: 1 1 200px;
}

.right ul li img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.right .theme,
.right .author,
.right .dynasty {
  margin: 10px;
}
</style>