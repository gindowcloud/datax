import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { install } from '@icon-park/vue-next/es/all'
import App from './App.vue'
import router from './router'
import config from './config'
import ElementGo from 'element-go'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import './assets/index.css'

document.title = config.appName
const app = createApp(App).use(router).use(ElementPlus).use(ElementGo).use(createPinia())
install(app, 'icon-park')
app.mount('#app')
