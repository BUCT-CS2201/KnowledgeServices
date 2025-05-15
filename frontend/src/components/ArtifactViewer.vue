<template>
    <div class="viewer-wrapper">
        <div ref="viewerRef" class="osd-container"></div>
    </div>
</template>

<script setup>
import {ref, onMounted, defineExpose, defineProps} from 'vue'
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
    })
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

.toolbar {
    position: absolute;
    bottom: 10px;
    left: 10px;
    display: flex;
    gap: 10px;
    background: rgba(255, 255, 255, 0.7);
    padding: 6px 10px;
    border-radius: 8px;
}
</style>
