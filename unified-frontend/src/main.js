import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import Antd from 'ant-design-vue'
import 'ant-design-vue/dist/reset.css'
import App from './App.vue'
import { routes } from './router'
import { message } from 'ant-design-vue'

// 创建应用实例
const app = createApp(App)

// 配置路由
const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    // 返回顶部或保存的位置
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 全局路由守卫
router.beforeEach((to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 百科系统`
  }
  
  next()
})

// 全局错误处理
router.onError((error) => {
  console.error('路由错误:', error)
  message.error('页面加载失败，请刷新重试')
})

// 配置状态管理
const pinia = createPinia()

// 注册插件
app.use(pinia)
app.use(router)
app.use(Antd)

// 全局错误处理
app.config.errorHandler = (err, instance, info) => {
  console.error('Vue错误:', err)
  console.error('错误信息:', info)
  message.error('应用发生错误，请刷新页面')
}

// 挂载应用
app.mount('#app')