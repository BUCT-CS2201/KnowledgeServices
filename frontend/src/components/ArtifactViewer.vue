<template>
    <div class="viewer-wrapper">
        <div ref="viewerRef" class="osd-container"></div>
    </div>
</template>

<script setup>
import {ref, onMounted, defineExpose, defineProps, onUnmounted, watch} from 'vue'
import OpenSeadragon from 'openseadragon'

const viewerRef = ref(null)
let viewer = null

const props = defineProps({
    imageUrl: {
        type: String,
        required: true
    }
})

onMounted(() => {
    viewer = OpenSeadragon({
        element: viewerRef.value,
        prefixUrl: 'https://openseadragon.github.io/openseadragon/images/',
        tileSources: {
            type: 'image',
            url: props.imageUrl
        },
        showNavigator: true,
        navigatorPosition: 'TOP_RIGHT',
        defaultZoomLevel: 0.9,
        minZoomLevel: 0.2,
        maxZoomLevel: 10,
        zoomPerClick: 1.5,
        gestureSettingsMouse: {
            scrollToZoom: true,
            clickToZoom: true,
            dblClickToZoom: true,
            dragToPan: true
        },
        showZoomControl: false,
        showFullPageControl: false,
        showHomeControl: false,
        navigatorAutoFade: false,
    })
})

// 响应式更新图像源
watch(() => props.imageUrl, (newUrl) => {
    if (viewer) {
        viewer.open({
            type: 'image',
            url: newUrl
        })
    }
})


function zoomIn() {
    viewer.viewport.zoomBy(1.2)
    viewer.viewport.applyConstraints()
}

function zoomOut() {
    viewer.viewport.zoomBy(0.8)
    viewer.viewport.applyConstraints()
}

function toggleFullScreen() {
    viewer.setFullScreen(!viewer.isFullPage())
}

defineExpose({viewer, zoomIn, zoomOut, toggleFullScreen})

onUnmounted(() => {
    if (viewer) {
        viewer.destroy()
        viewer = null
    }
})

</script>

<style scoped>
.viewer-wrapper {
    position: relative;
    width: 100%;
    height: 600px;
}

.osd-container {
    width: 100%;
    height: 100%;
    border: 1px solid #ccc;
}
</style>
