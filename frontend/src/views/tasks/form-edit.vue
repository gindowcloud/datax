<template>
  <el-dialog :model-value="show" title="添加任务" @close="close">
    <el-form ref="form" :model="item" :rules="rules" label-width="100px" label-suffix=":">
        <el-form-item label="任务名称" prop="name">
          <el-input v-model="item.name" />
        </el-form-item>
        <el-form-item label="读数据库" prop="reader_id">
          <el-select v-model="item.reader_id">
            <el-option v-for="(item, key) in connections.filter(j => j.direct == 'reader')" :value="item.id" :label="item.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="查询语句" prop="query">
          <el-input v-model="item.query" type="textarea" :rows="8" input-style="white-space: nowrap" />
        </el-form-item>
        <el-form-item label="写数据库" prop="writer_id">
          <el-select v-model="item.writer_id">
            <el-option v-for="item in connections.filter(j => j.direct == 'writer')" :value="item.id" :label="item.name" />
          </el-select>
        </el-form-item>
        <el-form-item label="写入表格" prop="table">
          <el-input v-model="item.table" />
        </el-form-item>
        <el-form-item label="写入字段" prop="query">
          <el-input v-model="item.column" type="textarea" :rows="4" />
        </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="close">取消</el-button>
      <el-button type="primary" :loading="loading" @click="submit(form)">确认</el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import type { Task, Connection } from '../../types'
import { ref, reactive, watchEffect } from 'vue'
import { FormInstance, FormRules } from 'element-plus'
import api from '../../api'

const props = defineProps({
  show: { type: Boolean, default: false },
  data: { type: Object, default: {} },
  connections: { type: Array<Connection>, default: [] }
})

const emit = defineEmits<{
  (event: 'submit'): void
  (event: 'close'): void
}>()

const loading = ref(false)
const item = ref<Task>({})
const form = ref<FormInstance>()
const rules = reactive<FormRules>({
  name: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
  reader_id: [{ required: true, message: '请输入读数据库', trigger: 'blur' }],
  writer_id: [{ required: true, message: '请输入写数据库', trigger: 'blur' }],
  query: [{ required: true, message: '请输入查询语句', trigger: 'blur' }],
  table: [{ required: true, message: '请输入写数据表', trigger: 'blur' }]
})

watchEffect(() => item.value = props.data)

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
    ? api.tasks.update(row.id, row)
    : api.tasks.create(row)
}
</script>
