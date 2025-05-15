<template>
    <div style="padding: 20px">
        <div id="timeline-embed" style="width: 100%; height: 600px;"></div>
    </div>
</template>

<script setup>
import {onMounted} from 'vue'
import {ElMessage} from 'element-plus'

const loadTimeline = async () => {
    try {
        const res = await fetch('http://localhost:5000/timeline-data')
        const data = await res.json()

        const timelineData = {
            title: {
                text: {
                    headline: '文物时间线',
                    text: '展示博物馆中的重要文物及其历史时间点'
                }
            },
            events: data.map(item => ({
                start_date: {
                    year: item.year,
                },
                text: {
                    headline: item.type,
                    text: `
                        <p><strong>描述：</strong> ${item.description || '无'}</p>
                        <p><strong>博物馆：</strong> ${item.museum}</p>
                        <p><strong>类型：</strong> ${item.type}</p>
                        <p><strong>朝代：</strong> ${item.dynasty}</p>
                        <p><strong>作者：</strong> ${item.author || '未知'}</p>
                        <p><strong>尺寸：</strong> ${item.size || '无'}</p>
                        <p><strong>材质：</strong> ${item.matrials || '无'}</p>
                        <p><strong>点赞：</strong> ${item.likes_count}</p>
                        <p><strong>浏览：</strong> ${item.views_count}</p>
                    `
                },
                media: item.image ? {
                    url: item.image,
                    caption: item.name
                } : undefined
            }))
        }

        window.timeline = new window.TL.Timeline('timeline-embed', timelineData)
    } catch (err) {
        ElMessage({
            message: '加载时间线数据失败', type: 'error',
            showClose: true, plain: false, grouping: true,
        })
        console.error(err)
    }
}

onMounted(() => {
    if (!window.TL) {
        const script = document.createElement('script')
        script.src = '/libs/timeline3/js/timeline.js'
        script.onload = loadTimeline
        document.body.appendChild(script)

        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = '/libs/timeline3/css/timeline.css'
        document.head.appendChild(link)
    } else {
        loadTimeline()
    }
})
</script>

<style scoped>
</style>
