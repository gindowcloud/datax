<template>
  <ex-page-header title="密码安全" />
  <el-result v-if="success" icon="success" title="保存成功" />
  <el-form v-else ref="form" :model="item" :rules="rules" label-width="100px" label-suffix=":" @submit.prevent="submit(form)">
    <el-form-item label="用户密码" prop="password">
      <el-input v-model="item.password" type="password" show-password />
    </el-form-item>
    <el-form-item label="设置新密码" prop="newpassword">
      <el-input v-model="item.newpassword" type="password" show-password />
    </el-form-item>
    <el-form-item label="重复新密码" prop="repassword">
      <el-input v-model="item.repassword" type="password" show-password />
    </el-form-item>
    <el-form-item>
      <el-button type="primary" :loading="loading" native-type="submit">保存</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import type { InternalRuleItem, Value } from 'async-validator'
import { ref, reactive } from 'vue'
import { FormInstance, FormRules } from 'element-plus'
import api from '../../api'

const item=ref({
  password: '',
  newpassword: '',
  repassword: ''
})

const success = ref(false)
const loading = ref(false)
const form = ref<FormInstance>()
const rules = reactive<FormRules>({
  password: [{ required: true, message: '请输入用户密码', trigger: 'blur' }],
  newpassword: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { required: true, trigger: "blur", validator: (rule: InternalRuleItem, value: Value, callback: (error?: Error) => void) => {
        value !== item.value.password ? callback() : callback(new Error("请设置新的密码"))
    } }
  ],
  repassword: [
    { required: true, message: '请输入确认密码', trigger: 'blur' },
    { required: true, trigger: "blur", validator: (rule: InternalRuleItem, value: Value, callback: (error?: Error) => void) => {
        value === item.value.newpassword ? callback() : callback(new Error("两次输入的密码不一致"))
    } }
  ]
})

const submit = async (form: FormInstance | undefined) => {
  if (!form) return
  await form.validate(valid => {
    if (!valid) return
    loading.value = true
    api.password(item.value)
      .then(() => success.value = true)
      .finally(() => loading.value = false)
  })
}
</script>

<style scoped>
.el-form { max-width: 400px; }
</style>