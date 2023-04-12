<template>
  <ex-layout :menu="data" :title="config.appName" homepage="/dashboard" background-color="#000" text-color="#ccc" active-text-color="#fff">
    <template #account><view-account /></template>
    <router-view />
  </ex-layout>
</template>

<script lang="ts" setup>
import { ExLayout } from 'element-go'
import { Airplay, PeoplesTwo, List, SettingOne, LinkThree, AlarmClock } from '@icon-park/vue-next'
import config from '../config'
import viewAccount from './components/account.vue'

const data = [
  { title: '首页', path: '/dashboard', icon: Airplay },
  { title: '任务', path: '/tasks', icon: List },
  { title: '计划', path: '/schedule', icon: AlarmClock },
  { title: '设置', path: '/settings', icon: SettingOne, children: [
    { title: '用户', path: '/users', icon: PeoplesTwo },
    { title: '连接', path: '/connections', icon: LinkThree },
  ]}
]
</script>

<style scoped>
.el-main .el-aside { background-color: #fff; border-right: 1px solid #f6f6f6; padding: 20px 0; margin-right: 20px; }
.el-main .el-aside .el-menu { border-right: none; }
.el-main .el-aside .el-menu-item { height: 40px; line-height: 40px; }
.logout { font-size: 20px; }
</style>
