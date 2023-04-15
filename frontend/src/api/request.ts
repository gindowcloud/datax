import { ElMessage } from 'element-plus'
import axios from  'axios'
import cookie from 'js-cookie'
import config from '../config'

declare module "axios" {
  interface AxiosResponse<T = any> {
    meta: { pagination: { total: number } }
  }
}

// 请求失败
const reject = (data: any) => {
  ElMessage.error(data?.message ?? "请求失败") // 提示后台消息
  return Promise.reject(data)
}

// 发送请求
const request = axios.create({ baseURL: config.baseURL })

// 响应处理
request.interceptors.response.use(
  response => response.data.code === 200 ? response.data : reject(response.data),
  error => reject(error.response.data)
)

export default {

  baseURL: config.baseURL,
  accessToken: '', // 认证信息

  get (url: string, params?: {} | null, auth = false) { return this.request('get', url, params, null, auth) },
  put (url: string, data?: {} | null, auth = false) { return this.request('put', url, null, data, auth) },
  patch (url: string, data?: {} | null, auth = false) { return this.request('patch', url, null, data, auth) },
  delete (url: string, params?: {} | null, auth = false) { return this.request('delete', url, params, null, auth) },
  post (url: string, data?: {} | null, auth = false) { return this.request('post', url, null, data, auth) },

  request (method: string, url: string, params?:  {} | null, data?:  {} | null, auth?: boolean) {
    const headers = { Accept: 'application/json', Authorization: '' }
    if (auth) {
      const accessToken = this.getToken()
      if (accessToken) headers.Authorization = 'Bearer ' + accessToken
    }
    return request({ method, url, params, data, headers })
  },

  getToken () {
    return this.accessToken = this.accessToken || cookie.get('accessToken') || ''
  },

  delToken () {
    this.accessToken = ''
    cookie.remove('accessToken')
  }
}
