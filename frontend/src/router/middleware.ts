import type { User } from '../types'
import store from '../store'
import request from '../api/request'
import api from '../api'

const user: User = {}

const middleware = {

  user,

  async getUser() {
    this.user = store().user
    if (this.user.id) return
    const token = request.getToken()
    if (token) {
      try {
        const { data } = await api.profile({})
        store().user = this.user = data
      } catch {
        request.delToken()
      }
    }
  }

}

export default middleware
