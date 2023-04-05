<template>
  <ex-page-header title="数据连接" />
  <ex-table :data="data" :columns="columns" :loaded="loaded" :loading="loading" :total="total" @page-change="getData"
    allow-view :viewer="viewer"
    allow-remove @remove="remove" />
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import api from '../api'

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

const remove = (item: any) => {
  api.connections.delete(item.id).then(() => getData())
}

getData()
</script>
