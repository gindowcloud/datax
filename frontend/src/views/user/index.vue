<template>
  <ex-page-header title="用户管理">
    <el-button link :icon="Plus" @click="create">新建</el-button>
  </ex-page-header>
  <ex-table :data="data" :columns="columns" :loaded="loaded" :loading="loading" :total="total" @page-change="getData"
    allow-view :viewer="viewer"
    allow-modify @modify="modify"
    allow-remove @remove="remove">
    <template #cell="{ col, row }">
      <icon-park-reduce-one v-if="col.prop == 'state'" class="icon-state" :class="row.state ? 'color-light' : 'color-red'" />
    </template>
  </ex-table>
  <!-- 编辑表单 -->
  <form-edit :show="show" :data="item" @close="close" @submit="submit" />    
</template>

<script lang="ts" setup>
import type { User } from '../../types'
import { ref, reactive } from 'vue'
import { Plus  } from '@icon-park/vue-next'
import { $copy } from '../../utils'
import store from '../../store'
import api from '../../api'
import formEdit from './components/edit.vue'

const columns = ref([
  { prop: 'state', width: 40 },
  { label: '账户', prop: 'username', width: 250 },
  { label: '姓名', prop: 'name' }
])

const viewer = ref([
  { label: '用户账户', prop: 'username' },
  { label: '用户姓名', prop: 'name' },
])

const item = ref<User>({})
const show = ref(false)
const session = store().user
const loaded = ref(false)
const loading = ref(false)
const total = ref(0)
const para = reactive({ size: 15, page: 1 })
const data = ref([])
const getData = (page = 1) => {
  loading.value = true
  para.page = page
  api.users.select(para).then(ret => {
    data.value = ret.data.map((j: any) => {
      j.$removeDisabled = j.id === session.id
      return j
    })
    total.value = ret.meta.pagination.total
  }).finally(() => {
    loading.value = false
    loaded.value = true
  })
}

const remove = (item: any) => {
  api.users.delete(item.id).then(() => getData())
}

const open = () => { show.value = true }
const close = () => { show.value = false }
const create = () => {
  item.value = {
    state: 1
  }
  open()
}

const modify = (row: any) => {
  item.value = $copy(row)
  open()
}

const submit = () => {
  close()
  getData()
}

getData()
</script>
