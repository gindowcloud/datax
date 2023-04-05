<template>
  <ex-page-header title="数据连接">
    <el-button link :icon="Plus" @click="create">新建</el-button>
  </ex-page-header>
  <ex-table :data="data" :columns="columns" :loaded="loaded" :loading="loading" :total="total" @page-change="getData"
    allow-view :viewer="viewer"
    allow-modify @modify="modify"
    allow-remove @remove="remove" />
  <!-- 编辑表单 -->
  <edit-form :show="show" :data="item" @close="close" @submit="submit" />
</template>

<script lang="ts" setup>
import type { Connection } from '../../types'
import { ref, reactive } from 'vue'
import { Plus  } from '@icon-park/vue-next'
import api from '../../api'
import editForm from './edit-form.vue'

const columns = ref([
  { label: '编号', prop: 'id', width: 200 },
  { label: '类型', prop: 'driver', width: 200 },
  { label: '名称', prop: 'name' },
])

const viewer = ref([
  { label: '连接编号', prop: 'id' },
  { label: '连接名称', prop: 'name' },
  { label: '连接类型', prop: 'driver' },
  { label: '数据库名', prop: 'database' },
  { label: '连接地址', prop: 'host' },
  { label: '连接端口', prop: 'port' },
])

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
  item.value = {}
  open()
}

const modify = (row: any) => {
  row.password = ''
  item.value = row
  open()
}

const submit = () => {
  close()
  getData()
}

getData()
</script>
