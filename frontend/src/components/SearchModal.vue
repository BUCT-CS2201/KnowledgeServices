<script setup>
import {ref, defineEmits} from 'vue'

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

</script>

<template>
    <el-dialog fullscreen :model-value="true" @close="$emit('close')">
        <template #header>
            <h1>高级搜索</h1>
        </template>
        <el-form style="margin-left: 10px" label-width="auto">
            <el-form-item label="作者">
                <el-input class="advance_input" v-model="author"/>
            </el-form-item>
            <el-form-item label="名称">
                <el-input class="advance_input" v-model="name"/>
            </el-form-item>
            <el-form-item label="博物馆">
                <el-input class="advance_input" v-model="museum"/>
            </el-form-item>
            <el-form-item label="时间">
                <el-col :span="3">
                    <div style="text-align: center">在...之后</div>
                    <el-input-number controls-position="right" v-model="afterYear" type="number" :min="0"/>
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
                    <el-input-number controls-position="right" :min="0" v-model="beforeYear" type="number"/>
                </el-col>
                <el-col :span="1"></el-col>
                <el-col :span="4">
                    <el-radio-group v-model="beforeEra">
                        <el-radio label="BCE">公元前</el-radio>
                        <el-radio label="CE">公元后</el-radio>
                    </el-radio-group>
                </el-col>
            </el-form-item>
            <el-form-item label="类型">
                <el-input class="advance_input" v-model="type"/>
            </el-form-item>
            <el-form-item label="材料">
                <el-input class="advance_input" v-model="matrials"/>
            </el-form-item>
            <el-form-item label="朝代">
                <el-input class="advance_input" v-model="dynasty"/>
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
    width: 30%;
}

.el-radio__input.is-checked .el-radio__inner {
    background-color: black;
    border-color: black;
}

.el-radio__input.is-checked + .el-radio__label {
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
