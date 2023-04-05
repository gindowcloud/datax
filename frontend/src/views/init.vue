<template>
  <ex-loading />
</template>

<script lang="ts" setup>
import api from '../api'
import { useRouter } from 'vue-router'

const router = useRouter()
api.init({username: 'admin', password: 'admin'}).finally(() => router.replace('/'))
</script>
