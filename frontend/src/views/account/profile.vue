<template>
  <ex-page-header title="用户资料" />
  <ex-loading v-if="!loaded" />
  <template v-else>
    <el-result v-if="success" icon="success" title="保存成功" />
    <el-form v-else ref="form" :model="item" :rules="rules" label-width="100px" label-suffix=":" @submit.prevent="submit(form)">
      <el-form-item label="用户姓名" prop="name">
        <el-input v-model="item.name" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" :loading="loading" native-type="submit">保存</el-button>
      </el-form-item>
    </el-form>
  </template>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import store from '../../store'
import { FormInstance, FormRules } from 'element-plus'
import api from '../../api'

const item=ref({
  name: '',
})

const success = ref(false)
const loaded = ref(false)
const loading = ref(false)
const form = ref<FormInstance>()
const rules = reactive<FormRules>({
  name: [{ required: true, message: '请输入用户姓名', trigger: 'blur' }],
})

const submit = async (form: FormInstance | undefined) => {
  if (!form) return
  await form.validate(valid => {
    if (!valid) return
    loading.value = true
    api.setting(item.value)
      .then(() => success.value = true)
      .finally(() => loading.value = false)
  })
}

const getData = () => {
  api.profile()
    .then(({ data }) => item.value.name = data.name)
    .finally(() => loaded.value = true)
}

getData()
</script>

<style scoped>
.el-form { max-width: 400px; }
</style>
