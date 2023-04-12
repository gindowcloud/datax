import request from './request'

class Resources {
  url: string
  auth: boolean

  constructor (url: string, auth = false) {
    this.url = url
    this.auth = auth
  }

  select (para?: {} | null) { return request.get(this.url, para, this.auth) }
  create (para?: {} | null) { return request.post(this.url, para, this.auth) }
  find (id: number, para?: {} | null) { return request.get(this.url + '/' + id, para, this.auth) }
  update (id: number, para?: {} | null) { return request.patch(this.url + '/' + id, para, this.auth) }
  delete (id: number, para?: {} | null) { return request.delete(this.url + '/' + id, para, this.auth) }
  async get (para: { size: number }) {
    para.size = 1
    return this.select(para).then(ret => {
      ret.data = ret.data[0] || {}
      return ret
    })
  }
}

export default {
  setup: (data?: {}) => request.post('v1/setup', data),
  login: (data?: {}) => request.post('v1/login', data),
  logout: (para?: {}) => request.post('v1/logout', para, true),
  profile: (para?: {}) => request.get('v1/profile', para, true),
  setting: (para?: {}) => request.post('v1/profile', para, true),
  password: (para?: {}) => request.post('v1/password', para, true),
  users: new Resources('v1/users', true),
  connections: new Resources('v1/connections', true),
  tasks: new Resources('v1/tasks', true),
  jobs: new Resources('v1/jobs', true),
  job_logs: (id: number, para?: {}) => request.get(`v1/jobs/${id}/logs`, para, true),
  schedules: new Resources('v1/schedules', true),
} 
