<template>
  <ex-layout :menu="data" :title="config.appName" homepage="/dashboard" background-color="#000" text-color="#ccc" active-text-color="#fff">
    <template #account>
      <el-link :underline="false" class="logout" @click="logout"><icon-park-power class="el-icon" /></el-link>
    </template>
    <router-view />
  </ex-layout>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router'
import { ExLayout } from 'element-go'
import { Airplay, PeoplesTwo, List, SettingOne, LinkThree, Lock } from '@icon-park/vue-next'
import config from '../config'
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
  { title: '设置', path: '/settings', icon: SettingOne, children: [
    { title: '连接', path: '/connections', icon: LinkThree },
    { title: '用户', path: '/users', icon: PeoplesTwo },
    { title: '密码', path: '/password', icon: Lock },
  ]}
]
</script>

<style scoped>
.el-main .el-aside { background-color: #fff; border-right: 1px solid #f6f6f6; padding: 20px 0; margin-right: 20px; }
.el-main .el-aside .el-menu { border-right: none; }
.el-main .el-aside .el-menu-item { height: 40px; line-height: 40px; }
.logout { font-size: 20px; }
</style>
