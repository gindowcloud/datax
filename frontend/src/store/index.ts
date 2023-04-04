import type { TypeUser } from '@/types'
import { defineStore } from 'pinia'

const user: TypeUser = {}

export default defineStore('main', {
  state: () => {
    return { user }
  }
})
