<template>
  <ex-page-header title="数据连接">
    <el-button link :icon="Plus" @click="create">新建</el-button>
  </ex-page-header>
  <ex-table :data="data" :columns="columns" :loaded="loaded" :loading="loading" :total="total" @page-change="getData"
    allow-view :viewer="viewer"
    allow-modify @modify="modify"
    allow-remove @remove="remove">
    <template #cell="{ col, row }">
      <el-tag v-if="col.prop == 'direct'" effect="dark" :type="directs.find(j => j.value == row.direct)?.type">
        {{ directs.find(j => j.value == row.direct)?.label }}
      </el-tag>
    </template>
  </ex-table>
  <!-- 编辑表单 -->
  <form-edit :show="show" :data="item" @close="close" @submit="submit" />
</template>

<script lang="ts" setup>
import type { Connection } from '../../types'
import { ref, reactive } from 'vue'
import { Plus  } from '@icon-park/vue-next'
import { $copy } from '../../utils'
import api from '../../api'
import formEdit from './components/edit.vue'

const columns = ref([
  { label: '方向', prop: 'direct', width: 150 },
  { label: '类型', prop: 'driver', width: 200 },
  { label: '名称', prop: 'name' }
])

const viewer = ref([
  { label: '连接方向', prop: 'direct' },
  { label: '连接类型', prop: 'driver' },
  { label: '连接名称', prop: 'name' },  
  { label: '数据库名', prop: 'database' },
  { label: '连接地址', prop: 'host' },
  { label: '连接端口', prop: 'port' },
  { label: '连接用户', prop: 'username' },
])

const directs = [
  { value: 'reader', label: '读库', type: 'success' },
  { value: 'writer', label: '写库', type: 'danger' }
]
const item = ref<Connection>({})
const show = ref(false)
const loaded = ref(false)
const loading = ref(false)
const total = ref(0)
const para = reactive({ size: 15, page: 1 })
const data = ref([])
const getData = (page = 1) => {
  loading.value = true
  para.page = page
  api.connections.select(para).then(ret => {
    data.value = ret.data
    total.value = ret.meta.pagination.total
  }).finally(() => {
    loading.value = false
    loaded.value = true
  })
}

const remove = (row: any) => {
  api.connections.delete(row.id).then(() => getData(para.page))
}

const open = () => { show.value = true }
const close = () => { show.value = false }
const create = () => {
  item.value = {
    direct: 'reader',
    driver: 'mysql',
    port: '3306'
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
</script>
