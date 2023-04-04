<template>
  <ex-layout :menu="data" title="数据管理平台" homepage="/dashboard" background-color="#000" text-color="#ccc" active-text-color="#fff">
    <template #account>
      <el-link :underline="false" class="logout" @click="logout"><icon-park-power class="el-icon" /></el-link>
    </template>
    <router-view />
  </ex-layout>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { ExLayout } from 'element-go'
import { Airplay, PeoplesTwo, List } from '@icon-park/vue-next'
import store from '../store'
import api from '../api'
import request from '../api/request'

const router = useRouter()
const logout = () => {
  api.logout({}).then(() => {
    store().user = {}
    request.delToken()
    router.push('/')
  })
}
const data = [
  { title: '首页', path: '/dashboard', icon: Airplay },
  { title: '任务', path: '/tasks', icon: List },
  { title: '用户', path: '/users', icon: PeoplesTwo },
]
</script>

<style scoped>
.el-main .el-aside { background-color: #fff; border-right: 1px solid #f6f6f6; padding: 20px 0; margin-right: 20px; }
.el-main .el-aside .el-menu { border-right: none; }
.el-main .el-aside .el-menu-item { height: 40px; line-height: 40px; }
.logout { font-size: 20px; }
</style>
