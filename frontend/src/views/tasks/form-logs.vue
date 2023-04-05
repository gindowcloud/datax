<template>
  <el-dialog :model-value="show" title="添加任务" @close="close">
    <el-form ref="form" :model="item" label-position="left" label-width="100px" label-suffix=":">
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
            <el-table-column label="操作" align="right" width="80">
              <template #default="{ row }">
                <el-link :underline="false" :disabled="row.state != 0" @click="cancel(row)">取消</el-link>
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
</template>

<script lang="ts" setup>
import type { Job, Task } from '../../types'
import { ref, computed, watchEffect } from 'vue'
import { ElMessageBox } from 'element-plus'
import api from '../../api'

const props = defineProps({
  show: { type: Boolean, default: false },
  data: { type: Object, default: {} }
})

const emit = defineEmits<{
  (event: 'submit'): void
  (event: 'close'): void
}>()

const loading = ref(false)
const item = ref<Task>({})
const states = [
  { label: '待处理', class: 'color-orange' },
  { label: '处理中', class: 'color-red' },
  { label: '已处理', class: 'color-green' },
  { label: '已取消', class: 'color-light' },
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
    api.jobs.update(row.id as number, { state: 3 }).then(() => row.state = 3)       
  })
}
</script>
