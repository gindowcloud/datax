<template>
  <ex-page-header title="用户管理" />
  <ex-table :data="data" :columns="columns" :loaded="loaded" :loading="loading" :total="total" @page-change="getData"
    allow-view :viewer="viewer" />
</template>

<script lang="ts" setup>
import { ref, reactive } from 'vue'
import api from '../api'

const columns = ref([
  { label: '编号', prop: 'id', width: 240 },
  { label: '用户', prop: 'username' }
])

const viewer = ref([
  { label: '用户编号', prop: 'id' },
  { label: '用户账户', prop: 'username' }
])

const loaded = ref(false)
const loading = ref(false)
const total = ref(0)
const para = reactive({ size: 15, page: 1 })
const data = ref([])
const getData = (page = 1) => {
  loading.value = true
  para.page = page
  api.users.select(para).then(ret => {
    data.value = ret.data
    total.value = ret.meta.pagination.total
  }).finally(() => {
    loading.value = false
    loaded.value = true
  })
}

getData()
</script>
