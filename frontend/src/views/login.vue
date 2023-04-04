<template>
  <div class="page">
    <div class="form">
      <el-form ref="form" :model="data" :rules="rules" label-suffix=":" label-width="100px" @submit.prevent="submit(form)">
        <div class="logo">{{ appName }}</div>
        <el-form-item label="用户账户" prop="username">
          <el-input v-model="data.username" clearable placeholder="登陆账户" />
        </el-form-item>
        <el-form-item label="用户密码" prop="password">
          <el-input v-model="data.password" clearable placeholder="登陆密码" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" native-type="submit">登陆</el-button>
          <el-button @click="reset(form)">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { FormInstance, FormRules } from 'element-plus'
import cookie from 'js-cookie'
import api from '../api/index'

const appName = import.meta.env.VITE_APP_NAME
const router = useRouter()
const form = ref<FormInstance>()
const loading = ref<boolean>(false)
const data = reactive({ username: '', password: '' })
const rules = reactive<FormRules>({
  username: [{ required: true, message: '请输入用户账户', trigger: 'blur' }],
  password: [{ required: true, message: '请输入用户密码', trigger: 'blur' }]
})

const submit = async (form: FormInstance | undefined) => {
  if (!form) return
  await form.validate(valid => {
    if (!valid) return
    loading.value = true
    api.login(data).then(({ data }) => {
      cookie.set('accessToken', data, { path: '/' })
      router.push('/dashboard')
    }).finally(() => { loading.value = false })
  })
}

const reset = (form: FormInstance | undefined) => {
  if (!form) return
  form.resetFields()
}
</script>

<style scoped>
.page { min-height: 100vh; background-color: #000; }
.page .form { padding: calc(50vh - 140px) 0; }
.page .form .el-form { max-width: 400px; margin: 0 auto; padding: 40px; background-color: #fff; }
.page .form .el-form .logo { text-align: center; margin-top: 22px; padding-bottom: 28px; font-size: 20px; }
</style>
