<template>
  <ex-page-header title="任务管理">
    <el-button link :icon="Plus" @click="create">新建</el-button>
  </ex-page-header>
  <ex-table :data="data" :columns="columns" :loaded="loaded" :loading="loading" :total="total" @page-change="getData"
    allow-view :viewer="viewer" :viewer-column="1"
    allow-modify @modify="modify"
    allow-remove @remove="remove">
    <template #cell="{ col, row }">
      <div v-if="col.prop == 'reader.name'">
        <span>{{ row.reader.name }}</span>
        <span class="color-light ml-10 mr-10">&gt;</span>
        <span>{{ row.writer.name }}</span>
        <span class="color-light ml-10 mr-10">/</span>
        <span class="color-green">{{ row.table }}</span>
      </div>
      <div v-if="col.prop == 'incremental'">
        <span v-if="row.incremental" class="color-green">是</span>
        <span v-else class="color-orange">否</span>
      </div>
      <icon-park-dot v-if="col.prop == 'state' && row.state" class="icon-state" :class="row.state == 1 ? 'color-green' : 'color-red'" />
    </template>
    <template #link="{ row }">
      <el-button link :icon="Airplay" @click="exec(row)">运行</el-button>
    </template>
  </ex-table>
  <!-- 编辑表单 -->
  <form-edit :show="show" :data="item" :connections="connections" @close="close" @submit="submit" />
  <!-- 运行菜单 -->
  <form-logs :show="logs" :data="item" @submit="done" @close="logs = false" />
</template>

<script lang="ts" setup>
import type { Task, Connection } from '../../types'
import { ref, reactive } from 'vue'
import { Plus, Airplay } from '@icon-park/vue-next'
import { ElMessage } from 'element-plus'
import { $copy } from '../../utils'
import api from '../../api'
import formEdit from './form-edit.vue'
import formLogs from './form-logs.vue'

const columns = ref([
  { label: '名称', prop: 'name', width: 200 },
  { label: '数据库', prop: 'reader.name' },
  { label: '增量更新', prop: 'incremental', align: 'center', width: 120 },
  { label: '最后执行', prop: 'executed_at', align: 'right', width: 160 },
  { label: '', prop: 'state', width: 40 }
])

const viewer = ref([
  { label: '任务名称', prop: 'name' },  
  { label: '读数据库', prop: 'reader.name' },
  { label: '查询语句', prop: 'query' },
  { label: '写数据库', prop: 'writer.name' },
  { label: '写数据表', prop: 'table' },
  { label: '写入字段', prop: 'column' },
])

const item = ref<Task>({})
const show = ref(false)
const loaded = ref(false)
const loading = ref(false)
const total = ref(0)
const para = reactive({ size: 15, page: 1 })
const data = ref([])
const getData = (page = 1) => {
  loading.value = true
  para.page = page
  api.tasks.select(para).then(ret => {
    data.value = ret.data.map((task: Task) => {
      task.executed_at = task.executed_at ? new Date(task.executed_at).toLocaleString() : '-'
      return task
    })
    total.value = ret.meta.pagination.total
  }).finally(() => {
    loading.value = false
    loaded.value = true
  })
}

const connections = ref<Connection[]>([])
const getConnections = () => {
  api.connections.select().then(ret => connections.value = ret.data)
}

const remove = (row: any) => {
  api.tasks.delete(row.id).then(() => getData(para.page))
}

const open = () => { show.value = true }
const close = () => { show.value = false }
const create = () => {
  item.value = {
    reader_id: connections.value.find(j => j.direct == 'reader')?.id,
    writer_id: connections.value.find(j => j.direct == 'writer')?.id
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

const logs = ref(false)
const exec = (row: Task) => {  
  logs.value = true
  api.jobs.select({ size: 5, task_id: row.id }).then(({ data }) => {
    item.value = row
    item.value.jobs = data
  })  
}

const done = () => {
  ElMessage.success('添加成功')
  logs.value = false
  getData(para.page)
}

getData()
getConnections()
</script>
