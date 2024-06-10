import { createApp } from 'vue'
import App from './App.vue'
import "@/assets/css/main.css"
import 'element-plus/dist/index.css'
import store from './store/index'
import ElementPlus from 'element-plus'
import router from './router/index'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import '@/mock/index.js'

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(router)
.use(ElementPlus)
.use(store)
.mount('#app')
