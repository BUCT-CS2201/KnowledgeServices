<script setup>
import axios from 'axios'
const loading = ref(false);

const emit = defineEmits(['addTags', 'close'])

const author = ref('')
const name = ref('')
const museum = ref('')
const type = ref('')
const dynasty = ref('')
const afterYear = ref('')
const afterEra = ref('CE')
const beforeYear = ref('')
const beforeEra = ref('CE')
const matrials = ref('')

const handleSearch = () => {
    const tags = []

    if (author.value) tags.push(`作者：${author.value}`)
    if (name.value) tags.push(`名称：${name.value}`)
    if (museum.value) tags.push(`博物馆：${museum.value}`)
    if (type.value) tags.push(`类型：${type.value}`)
    if (dynasty.value) tags.push(`朝代：${dynasty.value}`)
    if (matrials.value) tags.push(`材料：${matrials.value}`)
    if (afterYear.value) tags.push(`之后：${afterEra.value}${afterYear.value}`)
    if (beforeYear.value) tags.push(`以前：${beforeEra.value}${beforeYear.value}`)

    emit('addTags', tags)
    emit('close')
}

const fetchSuggestions = async (type, queryString, cb) => {
    try {
        loading.value = true;
        const { data } = await axios.get('http://localhost:5000/search-suggestions');

        Object.entries(data).flatMap(([type, values]) =>
            values.map(value => ({
                value: `${value}`,
                type: type,
                raw: value
            }))
        );
        // 根据类型获取对应维度的建议词（如type为"作者"时，取data["作者"]）
        const dimensionSuggestions = data[type] || [];
        // 过滤包含查询字符串的建议词，并格式化为el-autocomplete需要的{value, label}结构
        const filtered = dimensionSuggestions.filter(item =>
            item.toLowerCase().includes(queryString.toLowerCase())
        ).map(item => ({ value: item, label: item }));
        cb(filtered);
        // cb(suggestions.filter(item =>
        //     item.raw.toLowerCase().includes(queryString.toLowerCase())
        // ));
    } catch (error) {
        console.error('获取建议失败:', error);
        cb([]);
    } finally {
        loading.value = false;
    }
};

</script>

<template>
    <el-dialog fullscreen :model-value="true" @close="$emit('close')">
        <template #header>
            <h1>高级搜索</h1>
        </template>
        <el-form style="margin-left: 10px" label-width="auto">
            <el-form-item label="作者" class="advance_input">
                <el-autocomplete :fetch-suggestions="(query, cb) => fetchSuggestions('作者', query, cb)"
                    v-model="author" />
            </el-form-item>
            <el-form-item label="名称" class="advance_input">
                <el-autocomplete :fetch-suggestions="(query, cb) => fetchSuggestions('名称', query, cb)" v-model="name" />
            </el-form-item>
            <el-form-item label="博物馆" class="advance_input">
                <el-autocomplete :fetch-suggestions="(query, cb) => fetchSuggestions('博物馆', query, cb)"
                    v-model="museum" />
            </el-form-item>
            <el-form-item label="时间">
                <el-col :span="3">
                    <div style="text-align: center">在...之后</div>
                    <el-input-number controls-position="right" v-model="afterYear" type="number" :min="0" />
                </el-col>
                <el-col :span="1"></el-col>
                <el-col :span="4">
                    <el-radio-group v-model="afterEra">
                        <el-radio label="BCE">公元前</el-radio>
                        <el-radio label="CE">公元后</el-radio>
                    </el-radio-group>
                </el-col>
                <el-col :span="3">
                    <div style="text-align: center">在...之前</div>
                    <el-input-number controls-position="right" :min="0" v-model="beforeYear" type="number" />
                </el-col>
                <el-col :span="1"></el-col>
                <el-col :span="4">
                    <el-radio-group v-model="beforeEra">
                        <el-radio label="BCE">公元前</el-radio>
                        <el-radio label="CE">公元后</el-radio>
                    </el-radio-group>
                </el-col>
            </el-form-item>
            <el-form-item label="类型" class="advance_input">
                <el-autocomplete :fetch-suggestions="(query, cb) => fetchSuggestions('类型', query, cb)" v-model="type" />
            </el-form-item>
            <el-form-item label="材料" class="advance_input">
                <el-autocomplete :fetch-suggestions="(query, cb) => fetchSuggestions('材料', query, cb)"
                    v-model="matrials" />
            </el-form-item>
            <el-form-item label="朝代" class="advance_input">
                <el-autocomplete :fetch-suggestions="(query, cb) => fetchSuggestions('朝代', query, cb)"
                    v-model="dynasty" />
            </el-form-item>
        </el-form>

        <!--页脚-->
        <template #footer>
            <div class="dialog-footer">
                <el-button color="black" @click="$emit('close')"
                    style="border-radius: var(--el-border-radius-small); width: 150px; height: 40px; margin-left: 30px"
                    plain>取消
                </el-button>
                <el-button color="black" @click="handleSearch"
                    style="border-radius: var(--el-border-radius-small); width: 150px; height: 40px;">
                    搜索
                </el-button>
            </div>
        </template>
    </el-dialog>
</template>

<style scoped>
.advance_input {
    width: 30% !important;
}

.el-radio__input.is-checked .el-radio__inner {
    background-color: black;
    border-color: black;
}

.el-radio__input.is-checked+.el-radio__label {
    color: black;
}

.el-radio__inner {
    border-color: black;
}

:deep(.el-radio__input.is-checked .el-radio__inner) {
    background-color: black;
    border-color: black;
}

:deep(.el-radio__input.is-checked + .el-radio__label) {
    color: black;
}

:deep(.el-radio__inner) {
    border-color: black;
}

:deep(.el-radio__input:hover .el-radio__inner) {
    border-color: black;
}

:deep(.el-radio__input.is-checked:hover .el-radio__inner) {
    background-color: black;
    border-color: black;
}

:deep(.el-radio__input:hover + .el-radio__label) {
    color: black;
}
</style>
