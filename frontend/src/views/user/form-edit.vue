<template>
  <el-dialog :model-value="show" title="添加用户" @close="close">
    <el-form ref="form" :model="item" :rules="rules" label-width="100px" label-suffix=":">
      <el-row>        
        <el-col :span="span" v-if="isCreate">
          <el-form-item label="用户账号" prop="username">
            <el-input v-model="item.username" />
          </el-form-item>
        </el-col>
        <el-col :span="span" v-if="isCreate">
          <el-form-item label="用户密码" prop="password">
            <el-input v-model="item.password" type="password" show-password />
          </el-form-item>
        </el-col>
        <el-col :span="span">
          <el-form-item label="用户姓名" prop="name">
            <el-input v-model="item.name" />
          </el-form-item>
        </el-col>
        <el-col :span="span" v-if="item.id != user.id">
          <el-form-item label="账号状态" prop="state">
            <el-switch v-model="item.state" :active-value="1" :inactive-value="0" />
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <template #footer>
      <el-button @click="close">取消</el-button>
      <el-button type="primary" :loading="loading" @click="submit(form)">确认</el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import type { User } from '../../types'
import { ref, reactive, watchEffect, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { FormInstance, FormRules } from 'element-plus'
import store from '../../store'
import api from '../../api'

const props = defineProps({
  show: { type: Boolean, default: false },
  data: { type: Object, default: {} }
})

const emit = defineEmits<{
  (event: 'submit'): void
  (event: 'close'): void
}>()

const span = 12
const loading = ref(false)
const item = ref<User>({})
const form = ref<FormInstance>()
const rules = reactive<FormRules>({
  username: [{ required: true, message: '请输入用户账号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入用户密码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入用户姓名', trigger: 'blur' }],
  state: [{ required: true, message: '请输入用户状态', trigger: 'blur' }],
})

watchEffect(() => item.value = props.data)

const { user } = storeToRefs(store())
const isCreate = computed(() => {
  return !item.value.id
})

const close = () => emit('close')
const submit = async (form: FormInstance | undefined) => {
  if (!form) return
  await form.validate(valid => {
    if (!valid) return
    loading.value = true
    save(item.value)
      .then(() => emit('submit'))
      .finally(() => loading.value = false)
  })
}

const save = (row: any) => {
  return row.id
    ? api.users.update(row.id, row)
    : api.users.create(row)
}
</script>
