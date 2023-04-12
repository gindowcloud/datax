<template>
  <ex-page-header title="计划管理">
    <el-button link :icon="Plus" @click="create">添加</el-button>
  </ex-page-header>
  <ex-table :data="data" :columns="columns" :loaded="loaded" :loading="loading" :total="total" @page-change="getData"
    allow-view :viewer="viewer"
    allow-modify @modify="modify"
    allow-remove @remove="remove" />
  <!-- 编辑表单 -->
  <form-edit :show="show" :data="item" :tasks="tasks" @close="close" @submit="submit" />
</template>

<script lang="ts" setup>
import type { Schedule } from '../../types'
import { ref, reactive } from 'vue'
import { Plus  } from '@icon-park/vue-next'
import { $copy } from '../../utils'
import { scheduleTypes } from '../../types/labels'
import api from '../../api'
import formEdit from './components/edit.vue'


const columns = ref([
  { label: '计划名称', prop: 'name', width: 250 },
  { label: '任务名称', prop: 'task.name', width: 250 },
  { label: '计划类型', prop: 'typeName', width: 250 },
  { label: '执行时间', prop: 'time' },
])

const viewer = ref([
  { label: '计划名称', prop: 'name' },
  { label: '任务名称', prop: 'task.name' },
  { label: '计划类型', prop: 'typeName' },
  { label: '定时时间', prop: 'time' },
])

const item = ref<Schedule>({})
const show = ref(false)
const loaded = ref(false)
const loading = ref(false)
const total = ref(0)
const para = reactive({ size: 15, page: 1 })
const data = ref([])
const getData = (page = 1) => {
  loading.value = true
  para.page = page
  api.schedules.select(para).then(ret => {
    data.value = ret.data.map((item: any) => {
      item.typeName = scheduleTypes[item.type as 'cron' | 'interval' | 'date']
      if (item.type == 'cron') item.time = item.cron
      else if (item.type == 'interval') item.time = item.interval + ' ' + item.period
      return item
    })
    total.value = ret.meta.pagination.total
  }).finally(() => {
    loading.value = false
    loaded.value = true
  })
}

const tasks = ref([])
const getTask = () => {
  api.tasks.select({ size: 500 }).then(ret => tasks.value = ret.data)
}

const remove = (row: any) => {
  api.schedules.delete(row.id).then(() => getData(para.page))
}

const open = () => { show.value = true }
const close = () => { show.value = false }
const create = () => {
  item.value = {
    type: 'cron',
    period: 'days'    
  }
  open()
}

const modify = (row: any) => {
  row.password = ''
  item.value = $copy(row)
  open()
}

const submit = () => {
  close()
  getData()
}

getData()
getTask()
</script>
