<template>
    <!--导航栏下方内容-->
    <el-container>
        <!-- 侧边栏 -->
        <el-aside width="250px" style="background-color: #f5f5f5; padding: 20px;
            height: calc(100vh - 60px);overflow-y: auto;">
            <!--工具栏 -->
            <h3>工具栏</h3>
            <!--搜索-->
            <el-autocomplete v-model="searchKeyword" :fetch-suggestions="querySearchAsync" placeholder="输入名称或属性值"
                clearable @select="searchGraph">
                <template #default="{ item }">
                    <div class="flex justify-between">
                        <span>{{ item.value }}</span>
                        <span class="text-gray-400">{{ item.type }}</span>
                    </div>
                </template>
                <template #append>
                    <el-button @click="searchGraph">
                        <el-icon>
                            <Search />
                        </el-icon>
                    </el-button>
                </template>
            </el-autocomplete>
            <!--放大缩小保存-->
            <div style="margin-top: 10px;margin-bottom: 10px;" class="flex gap-4">
                <el-button @click="zoom(1.2)">
                    <el-icon>
                        <Plus />
                    </el-icon>
                </el-button>
                <el-button @click="zoom(0.8)">
                    <el-icon>
                        <Minus />
                    </el-icon>
                </el-button>
                <el-dropdown @command="saveAs">
                    <el-button style="margin-left: 20px">
                        <el-icon>
                            <Download />
                        </el-icon>
                    </el-button>
                    <template #dropdown>
                        <el-dropdown-menu>
                            <el-dropdown-item command="svg">保存为 SVG</el-dropdown-item>
                            <el-dropdown-item command="png">保存为 PNG</el-dropdown-item>
                        </el-dropdown-menu>
                    </template>
                </el-dropdown>
            </div>
            <!--节点详情 -->
            <h3 style="margin-top: 20px;">节点详情</h3>
            <div v-if="selectedNode">
                <p><strong>{{ selectedNode.name }}</strong></p>
                <el-table :data="tableData" border stripe style="width: 100%; margin-top: 10px;">
                    <el-table-column prop="key" label="属性名" width="90" />
                    <el-table-column prop="value" label="属性值">
                        <template #default="scope">
                            <template v-if="scope.row.key === 'img_url' || scope.row.key === 'picture'">
                                <a :href="`${scope.row.value}`" target="_blank" class="text-blue-600 hover:underline">
                                    {{ scope.row.value }}
                                </a>
                            </template>
                            <template v-else>
                                {{ scope.row.value }}
                            </template>
                        </template>
                    </el-table-column>
                </el-table>
            </div>
            <div v-else>
                <p>点击节点查看详情</p>
            </div>

        </el-aside>
        <!-- 图谱区域 -->
        <el-main v-loading="loading" element-loading-text="Loading..." style="overflow: hidden;">
            <svg style="width: 100%; height: calc(100vh - 60px); contain: strict;will-change: transform;"
                ref="svg"></svg>
        </el-main>
    </el-container>
</template>

<script setup>
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { ElMessage } from "element-plus";
import { debounce } from 'lodash';
import { onBeforeUnmount } from "vue";

const svg = ref(null);
const selectedNode = ref(null);
const tableData = ref([]);
const searchKeyword = ref('');
const route = useRoute();
const loading = ref(false);


let zoomGroup, simulation, zoomHandler;

// 新增搜索建议逻辑
const querySearchAsync = async (queryString, cb) => {
    try {
        const res = await fetch('http://localhost:5000/search-suggestions');
        const data = await res.json();

        const allSuggestions = [
            ...data.朝代.map(v => ({ value: v })),
            ...data.材质.map(v => ({ value: v })),
            ...data.博物馆.map(v => ({ value: v })),
            ...data.类型.map(v => ({ value: v })),
            ...data.作者.map(v => ({ value: v })),
            ...data.名称.map(v => ({ value: v }))
        ];

        cb(queryString
            ? allSuggestions.filter(i =>
                i.value.toLowerCase().includes(queryString.toLowerCase())
            )
            : allSuggestions
        );
    } catch (e) {
        console.error('获取搜索建议失败:', e);
        cb([]);
    }
};

function handleResize() {
    if (!svg.value || loading.value) return;

    const { offsetWidth, offsetHeight } = svg.value;
    const aspectRatio = offsetWidth / offsetHeight;

    // 仅当宽高比变化超过5%时刷新
    if (Math.abs(aspectRatio - window.innerWidth / window.innerHeight) > 0.05) {
        fetchGraph(searchKeyword.value);
    }
}

onBeforeUnmount(() => {
    window.removeEventListener('resize', debounce(handleResize, 300));
});

//挂载知识图谱
onMounted(async () => {
    window.addEventListener('resize', debounce(handleResize, 300));
    const keyword = route.params.keyword || ''
    searchKeyword.value = keyword
    fetchGraph(keyword)
    ElMessage({
        message: "知识图谱受限，只展示前300条记录", type: 'info',
        showClose: true, plain: false, grouping: true,
    })
});

//渲染知识图谱
function renderGraph(data) {
    const width = window.innerWidth - 250; // 减去 aside 宽度
    const height = window.innerHeight - 60; // 减去 header 高度
    const svgEl = d3.select(svg.value)
        .attr("width", width)
        .attr("height", height);

    svgEl.selectAll("*").remove(); // 清空旧图

    //颜色映射
    const labels = [...new Set(data.nodes.map(n => n.label))]
    const colorScale = d3.scaleOrdinal()
        .domain(labels)
        .range(d3.schemeSet3)

    //滚轮缩放
    zoomHandler = d3.zoom().on("zoom", (event) => {
        zoomGroup.attr("transform", event.transform);
    });
    svgEl.call(zoomHandler);

    // 添加箭头
    svgEl.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 24)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "#999");

    zoomGroup = svgEl.append("g");

    simulation = d3.forceSimulation(data.nodes)
        .force("link", d3.forceLink(data.links).id(d => d.id).distance(400))
        .force("charge", d3.forceManyBody().strength(-300))
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collide", d3.forceCollide().radius(50)); // 添加碰撞检测

    const link = zoomGroup.selectAll("line")
        .data(data.links)
        .enter().append("line")
        .attr("marker-end", "url(#arrow)")
        .style("stroke", "#999");

    const linkText = zoomGroup.selectAll(".link-text")
        .data(data.links)
        .enter().append("text")
        .text(d => d.type)
        .style("font-size", "10px").style("fill", "#555");

    const nodeGroup = zoomGroup.selectAll("g")
        .data(data.nodes)
        .enter().append("g")
        .call(drag(simulation))
        .on("click", (_, d) => {
            if (loading.value) {
                ElMessage({
                    message: "图谱加载中，请稍后", type: 'warning',
                    showClose: true, plain: false, grouping: true,
                })
                return;
            }
            // 添加点击防抖
            debounce(() => {
                selectedNode.value = d;
                // 强制重新计算布局
                requestAnimationFrame(() => {
                    simulation.alpha(0.3).restart();
                });
            }, 150)();
        });

    const getDisplayText = (node) => {
        return node?.properties?.name
            || node?.properties?.dynasty_name
            || node?.properties?.material_name
            || node?.properties?.address_text
            || node?.properties?.museum_name
            || node?.properties?.img_url
            || node?.properties?.label
            || node?.properties?.type
            || node.elementId?.split(':').pop()
            || node.id; // 最后保障使用节点ID
    };

    nodeGroup.append("circle")
        .attr("r", d => Math.min(6 + (getDisplayText(d).length || 3) * 6, 45))
        .style("fill", d => colorScale(d.label))
        .style("stroke", "#333") // 添加边框颜色
        .style("stroke-width", 2); // 边框宽度

    nodeGroup.append("text").each(function (d) {
        const rawText = getDisplayText(d);
        const text = rawText ? rawText.substring(0, 15) : d.id; // 双重保障机制
        const lines = [];

        if (text.length > 7) {
            lines.push(text.slice(0, 4));
            lines.push(text.slice(4, 8) + "...");
        } else {
            lines.push(text);
        }

        const textElement = d3.select(this)
            .style("fill", "black")
            .style("font-size", "12px")
            .style("text-anchor", "middle")
            .style("dominant-baseline", "central")
            .style("pointer-events", "none");

        if (lines.length === 1) {
            // 单行，垂直居中
            textElement.append("tspan")
                .attr("x", 0)
                .attr("dy", 0)
                .text(lines[0]);
        } else {
            // 多行，第一行上移，第二行下移
            lines.forEach((line, i) => {
                textElement.append("tspan")
                    .attr("x", 0)
                    .attr("dy", i === 0 ? "-0.5em" : "1em")
                    .text(line);
            });
        }
    });

    simulation.on("tick", () => {
        link.attr("x1", d => d.source.x)
            .attr("y1", d => d.source.y)
            .attr("x2", d => d.target.x)
            .attr("y2", d => d.target.y);

        linkText
            .attr("x", d => (d.source.x + d.target.x) / 2)
            .attr("y", d => (d.source.y + d.target.y) / 2);

        nodeGroup.attr("transform", d => `translate(${d.x},${d.y})`);
    });
    // ---- 添加图例（Legend） ----
    const legend = svgEl.append("g")
        .attr("class", "legend")
        .attr("transform", `translate(${width - 200}, 40)`);

    // 先添加背景
    legend.insert('rect', ':first-child')
        .attr('x', -30)
        .attr('y', -20)
        .attr('width', 160)
        .attr('height', labels.length * 25 + 25)
        .attr('rx', 8)
        .style('fill', 'white')
        .style('opacity', 0.8)
        .style('z-index', -1); // 设置背景层级

    labels.forEach((label, i) => {
        const g = legend.append("g")
            .attr("transform", `translate(0, ${i * 25})`);

        g.append("circle")
            .attr("r", 8)
            .attr("fill", colorScale(label));

        g.append("text")
            .text(label)
            .attr("x", 16)
            .attr("y", 4)
            .style("fill", "#333")
            .style("font-size", "14px");
    });

}

//详情展示
watch(selectedNode, (newVal) => {
    if (newVal) {
        tableData.value = Object.entries(newVal.properties || {}).map(([key, value]) => ({
            key,
            value
        }));
    } else {
        tableData.value = [];
    }
});

//监听搜索框
watch(() => route.params.keyword, (newKeyword) => {
    searchKeyword.value = newKeyword || ''
    fetchGraph(searchKeyword.value)
})

//拖拽管理
function drag(simulation) {
    return d3.drag()
        .on("start", (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
        })
        .on("drag", (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
        })
        .on("end", (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
        });
}

//缩放管理
function zoom(factor) {
    if (loading.value) {
        ElMessage({
            message: "图谱加载中，请稍后", type: 'warning',
            showClose: true, plain: false, grouping: true,
        })
        return;
    }
    const svgEl = d3.select(svg.value);
    svgEl.transition().duration(300).call(zoomHandler.scaleBy, factor);
}

//保存图片
function saveAs(type) {
    if (loading.value) {
        ElMessage({
            message: "图谱加载中，请稍后", type: 'warning',
            showClose: true, plain: false, grouping: true,
        })
        return;
    }
    const svgElement = svg.value;
    const svgData = new XMLSerializer().serializeToString(svgElement);

    if (type === 'svg') {
        const blob = new Blob([svgData], { type: "image/svg+xml;charset=utf-8" });
        const a = document.createElement("a");
        a.href = URL.createObjectURL(blob);
        a.download = "graph.svg";
        a.click();
        return;
    }

    if (type === 'png') {
        const canvas = document.createElement("canvas");
        const ctx = canvas.getContext("2d");
        const img = new Image();
        const svgSize = svgElement.getBoundingClientRect();
        canvas.width = svgSize.width;
        canvas.height = svgSize.height;

        img.onload = () => {
            ctx.drawImage(img, 0, 0);
            const a = document.createElement("a");
            a.download = "graph.png";
            a.href = canvas.toDataURL("image/png");
            a.click();
        };
        img.src = "data:image/svg+xml;base64," + btoa(unescape(encodeURIComponent(svgData)));
    }
}

const fetchGraph = async (keyword = '') => {
    loading.value = true; // 开始加载
    try {
        const res = await fetch(`http://localhost:5000/graph-data?keyword=${encodeURIComponent(keyword)}`);
        const data = await res.json();
        renderGraph(data);
    } catch (e) {
        ElMessage({
            message: '知识图谱加载失败', type: 'error',
            showClose: true, plain: false, grouping: true,
        });
    } finally {
        loading.value = false; // 加载完成
    }
}

const searchGraph = () => {
    fetchGraph(searchKeyword.value);
}

</script>

<style scoped>
.el-main {
    contain: strict;
    will-change: transform;
}

.el-aside {
    contain: strict;
    will-change: transform;
}

svg {
    isolation: isolate;
}
</style>
