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
                    month: item.month || 1,
                    day: item.day || 1
                },
                text: {
                    headline: item.name,
                    text: item.description
                },
                media: item.image ? {
                    url: item.image,
                    caption: item.name
                } : undefined
            }))
        }

        window.timeline = new window.TL.Timeline('timeline-embed', timelineData)
    } catch (err) {
        ElMessage.error('加载时间线数据失败')
        console.error(err)
    }
}

onMounted(() => {
    if (!window.TL) {
        const script = document.createElement('script')
        script.src = 'https://cdn.knightlab.com/libs/timeline3/latest/js/timeline.js'
        script.onload = loadTimeline
        document.body.appendChild(script)

        const link = document.createElement('link')
        link.rel = 'stylesheet'
        link.href = 'https://cdn.knightlab.com/libs/timeline3/latest/css/timeline.css'
        document.head.appendChild(link)
    } else {
        loadTimeline()
    }
})
</script>

<style scoped>
</style>
