<template>
  <el-dialog :model-value="show" title="添加任务" @close="close">
    <ex-loading v-if="!item.id" />
    <el-form v-else ref="form" :model="item" label-position="left" label-width="100px" label-suffix=":">
        <el-form-item label="任务名称">{{ item.name }}</el-form-item>
        <el-form-item label="读数据库">{{ item.reader?.name }} > {{ item.writer?.name }} > {{ item.table }}</el-form-item>
        <el-form-item label="运行记录">
          <el-table :data="item.jobs">
            <el-table-column label="编号">
              <template #default="{ row }">
                # {{ row.id }}
              </template>
            </el-table-column>
            <el-table-column label="状态" align="right">
              <template #default="{ row }">
                <span :class="states[row.state].class">{{ states[row.state].label }}</span>
              </template>
            </el-table-column>
            <el-table-column label="操作" align="right" width="120">
              <template #default="{ row }">
                <el-link :underline="false" :disabled="row.state != PENDING" @click="cancel(row)">取消</el-link>
                <el-link :underline="false" :disabled="row.state == PENDING || row.state == CANCELED" @click="logs(row)" class="ml-10">日志</el-link>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="close">取消</el-button>
      <el-button type="primary" :loading="loading" :disabled="disabled" @click="submit">运行</el-button>
    </template>
  </el-dialog>
  <el-dialog :model-value="logShow" title="任务日志" :modal="false" @close="logShow = false">
    <div class="log-data" v-html="logData" />
  </el-dialog>
</template>

<script lang="ts" setup>
import type { Job, Task } from '../../types'
import { ref, computed, watchEffect } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import api from '../../api'

const props = defineProps({
  show: { type: Boolean, default: false },
  data: { type: Object, default: {} }
})

const emit = defineEmits<{
  (event: 'submit'): void
  (event: 'close'): void
}>()

const PENDING = 0
const CANCELED = 3
const loading = ref(false)
const item = ref<Task>({})
const states = [
  { label: '待处理', class: 'color-blue' },
  { label: '处理中', class: 'color-orange' },
  { label: '已完成', class: 'color-green' },
  { label: '已取消', class: 'color-light' },
  { label: '已报错', class: 'color-red' },
]

// 可否添加（根据待完成任务判断）
const disabled = computed(() => {
  return (item.value.jobs?.filter(j => j.state === 0).length ?? 0) > 0
})

watchEffect(() => item.value = props.data)

const close = () => emit('close')
const submit = () => {
  loading.value = true
  api.jobs.create({task_id: item.value.id})
    .then(() => emit('submit'))
    .finally(() => loading.value = false)
}

const cancel = (row: Job) => {
  ElMessageBox.confirm('是否确认取消操作', '操作确认', {type: 'warning'}).then(() => {
    api.jobs.update(row.id as number, { state: CANCELED }).then(() => row.state = 3)       
  })
}

const logShow = ref(false)
const logData = ref('')
const logs = (row: Job) => {
  api.job_logs(row.id as number).then(ret => {
    logData.value = ret.data.replace(/\n/g, "<br>").replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;")
    logShow.value = true
  }).catch(() => ElMessage.error("暂无日志信息"))
}
</script>

<style scoped>
.log-data { background-color: #000; color: #ccc; padding: 0px 10px; line-height: 150%; height: 440px; overflow: auto; }
</style>