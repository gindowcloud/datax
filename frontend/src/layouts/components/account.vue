<template>
  <el-dropdown @command="command">
    <icon-park-user class="avatar" />
    <template #dropdown>
      <el-dropdown-menu>
        <el-dropdown-item command="profile">我的资料</el-dropdown-item>
        <el-dropdown-item command="password">密码安全</el-dropdown-item>
        <el-dropdown-item command="logout">退出登陆</el-dropdown-item>
      </el-dropdown-menu>
    </template>
  </el-dropdown>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import store from '../../store'
import api from '../../api'
import request from '../../api/request'

const router = useRouter()
const command = (item: string | number | object) => {
  switch (item) {
  case 'profile': router.push('/account/profile'); break
  case 'password': router.push('/account/password'); break
  case 'logout': logout(); break
  }
}

// 退出登陆
const logout = () => {
  api.logout({}).then(() => {
    store().user = {}
    request.delToken()
    router.push('/')
  })
}
</script>

<style scoped>
.avatar { height: 20px; font-size: 20px; }
</style>
