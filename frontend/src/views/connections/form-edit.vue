<template>
  <el-dialog :model-value="show" title="添加连接" @close="close">
    <el-form ref="form" :model="item" :rules="rules" label-width="100px" label-suffix=":">
      <el-row>        
        <el-col :span="span">
          <el-form-item label="连接方向" prop="direct">
            <el-radio-group v-model="item.direct">
              <el-radio-button label="reader">读数据</el-radio-button>
              <el-radio-button label="writer">写数据</el-radio-button>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :span="span">
          <el-form-item label="连接类型" prop="driver">
            <el-select v-model="item.driver" @change="driverChange">
              <el-option value="mysql" label="MySQL" />
              <el-option value="clickhouse" label="ClickHouse" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="span">
          <el-form-item label="连接名称" prop="name">
            <el-input v-model="item.name" />
          </el-form-item>
        </el-col>
        <el-col :span="span">
          <el-form-item label="数据库名" prop="database">
            <el-input v-model="item.database" />
          </el-form-item>
        </el-col>
        <el-col :span="span">
          <el-form-item label="连接地址" prop="host">
            <el-input v-model="item.host" />
          </el-form-item>
        </el-col>
        <el-col :span="span">
          <el-form-item label="连接端口" prop="port">
            <el-input v-model="item.port" />
          </el-form-item>
        </el-col>
        <el-col :span="span">
          <el-form-item label="连接用户" prop="username">
            <el-input v-model="item.username" />
          </el-form-item>
        </el-col>
        <el-col :span="span">
          <el-form-item label="连接密码" prop="password">
            <el-input v-model="item.password" />
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
import type { Connection } from '../../types'
import { ref, reactive, watchEffect } from 'vue'
import { FormInstance, FormRules } from 'element-plus'
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
const item = ref<Connection>({})
const form = ref<FormInstance>()
const rules = reactive<FormRules>({
  driver: [{ required: true, message: '请输入连接类型', trigger: 'blur' }],
  name: [{ required: true, message: '请输入连接名称', trigger: 'blur' }],
  host: [{ required: true, message: '请输入连接地址', trigger: 'blur' }],
  port: [{ required: true, message: '请输入连接端口', trigger: 'blur' }],
  username: [{ required: true, message: '请输入连接用户', trigger: 'blur' }],
  database: [{ required: true, message: '请输入数据库名', trigger: 'blur' }]
})

watchEffect(() => item.value = props.data)

const mappings = [
  { driver: 'mysql', port: '3306' },
  { driver: 'clickhouse', port: '8123' }
]

const driverChange = (driver: string) => {
  item.value.port = mappings.find(j => j.driver == driver)?.port
}

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
    ? api.connections.update(row.id, row)
    : api.connections.create(row)
}
</script>
