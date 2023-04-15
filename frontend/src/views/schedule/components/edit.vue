<template>
  <el-dialog :model-value="show" title="添加计划" @close="close">
    <el-form ref="form" class="max-width-500" :model="item" :rules="rules" label-width="100px" label-suffix=":">
      <el-form-item label="计划任务" prop="task_id">
        <el-select v-model="item.task_id" @change="taskChanged">
          <el-option v-for="item in tasks" :value="item.id" :label="item.name" />
        </el-select>
      </el-form-item>
      <el-form-item label="计划名称" prop="name">
        <el-input v-model="item.name" />
      </el-form-item>
      <el-form-item label="触发调度" prop="type" required>
        <el-radio-group v-model="item.type" @change="typeChanged">
          <el-radio-button label="cron">定时调度</el-radio-button>
          <el-radio-button label="interval">间隔调度</el-radio-button>
          <el-radio-button label="date" disabled>单次调度</el-radio-button>
        </el-radio-group>
      </el-form-item>
      <el-form-item v-if="item.type == 'cron'" label="定时时间" required>
        <el-row :gutter="4" class="wp-100">
          <el-col :span="4"><el-input v-model="cron.year" /></el-col>
          <el-col :span="4"><el-input v-model="cron.month" /></el-col>
          <el-col :span="4"><el-input v-model="cron.day_of_week" /></el-col>
          <el-col :span="4"><el-input v-model="cron.day" /></el-col>
          <el-col :span="4"><el-input v-model="cron.hour" /></el-col>
          <el-col :span="4"><el-input v-model="cron.minute" /></el-col>
        </el-row>
        <el-row :gutter="4" class="wp-100 text-center color-light">
          <el-col :span="4">年</el-col>
          <el-col :span="4">月</el-col>
          <el-col :span="4">周</el-col>
          <el-col :span="4">日</el-col>
          <el-col :span="4">时</el-col>
          <el-col :span="4">分</el-col>
        </el-row>
      </el-form-item>
      <el-form-item v-if="item.type == 'interval'" label="间隔时间" prop="interval">
        <el-row :gutter="12">
          <el-col :span="12"><el-input v-model="item.interval" /></el-col>
          <el-col :span="12">
            <el-select v-model="item.period" style="width: 111px">
              <el-option value="weeks" label="周" />
              <el-option value="days" label="天" />
              <el-option value="hours" label="小时" />
              <el-option value="minutes" label="分钟" />
              <el-option value="seconds" label="秒钟" />
            </el-select>
          </el-col>
        </el-row>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="close">取消</el-button>
      <el-button type="primary" :loading="loading" @click="submit(form)">确认</el-button>
    </template>
  </el-dialog>
</template>

<script lang="ts" setup>
import type { Task, Schedule } from '../../../types'
import { ref, reactive, watch, watchEffect } from 'vue'
import { FormInstance, FormRules } from 'element-plus'
import { scheduleTypes, scheduleTypeKeys } from '../../../types/labels'
import api from '../../../api'

const props = defineProps({
  show: { type: Boolean, default: false },
  data: { type: Object, default: {} },
  tasks: { type: Array<Task>, default: [] }
})

const emit = defineEmits<{
  (event: 'submit'): void
  (event: 'close'): void
}>()

const loading = ref(false)
const item = ref<Schedule>({})
const form = ref<FormInstance>()
const rules = reactive<FormRules>({
  name: [{ required: true, message: '请输入连接名称', trigger: 'blur' }],
  interval: [{ required: true, message: '请输入间隔时间', trigger: 'blur' }],
  task_id: [{ required: true, message: '请输入计划任务', trigger: 'blur' }],
})

const cron = reactive<{
  year?: string
  month?: string
  week?: string
  day_of_week?: string
  day?: string
  hour?: string
  minute?: string
  second?: string
}>({})

watchEffect(() => item.value.cron = cron.year + ' ' + cron.month + ' ' + cron.week + ' ' + cron.day_of_week + ' ' + cron.day + ' ' + cron.hour + ' ' + cron.minute + ' ' + cron.second)
watch(() => props.data, () => {
  const split = (props.data.cron ?? '* * * * * 2 0 0').split(' ')
  cron.year = split[0]
  cron.month = split[1]
  cron.week = split[2]
  cron.day_of_week = split[3]
  cron.day = split[4]
  cron.hour = split[5]
  cron.minute = split[6]
  cron.second = split[7]
  item.value = props.data
})

const taskChanged = () => updateName()
const typeChanged = () => updateName()
const updateName = () => {
  const task = props.tasks.find(j => j.id == item.value.task_id)
  const name = scheduleTypes[item.value.type as scheduleTypeKeys].replace('调度', '')
  item.value.name = task?.name + name + '更新计划'
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
    ? api.schedules.update(row.id, row)
    : api.schedules.create(row)
}
</script>
