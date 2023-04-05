import type { User } from '../types'
import { defineStore } from 'pinia'

const user: User = {}

export default defineStore('main', {
  state: () => {
    return { user }
  }
})
