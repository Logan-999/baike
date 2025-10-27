<template>
  <div id="app">
    <!-- 导航栏 -->
    <a-layout>
      <a-layout-header class="header">
        <div class="header-content">
          <div class="logo">
            <router-link to="/">
              <h1>百科系统</h1>
            </router-link>
          </div>
          
          <!-- 搜索框 -->
          <div class="search-container">
            <a-input-search
              v-model:value="searchQuery"
              placeholder="搜索词条..."
              enter-button="搜索"
              size="large"
              @search="handleSearch"
            />
          </div>
          
          <!-- 导航菜单 -->
          <a-menu v-model:selectedKeys="currentMenu" mode="horizontal" class="nav-menu">
            <a-menu-item key="home">
              <router-link to="/">首页</router-link>
            </a-menu-item>
            <a-menu-item key="entries">
              <router-link to="/entries">词条列表</router-link>
            </a-menu-item>
            <a-menu-item key="categories">
              <router-link to="/categories">分类管理</router-link>
            </a-menu-item>
            
            <!-- 用户相关菜单 -->
            <a-sub-menu v-if="authStore.isAuthenticated" key="user">
              <template #title>
                <a-avatar :size="32" style="background-color: #87d068">
                  {{ (authStore.user?.username || '').charAt(0).toUpperCase() || 'U' }}
                </a-avatar>
                <span style="margin-left: 8px">{{ authStore.user?.username }}</span>
              </template>
              <a-menu-item key="profile">
                <router-link to="/profile">个人中心</router-link>
              </a-menu-item>
              <a-menu-item key="create">
                <router-link to="/entries/create">创建词条</router-link>
              </a-menu-item>
              <a-menu-divider />
              <a-menu-item key="logout" @click="handleLogout">
                退出登录
              </a-menu-item>
            </a-sub-menu>
            
            <a-menu-item v-else key="auth">
              <router-link to="/login">登录/注册</router-link>
            </a-menu-item>
          </a-menu>
        </div>
      </a-layout-header>
      
      <!-- 主要内容区域 -->
      <a-layout-content class="content">
        <router-view />
      </a-layout-content>
      
      <!-- 页脚 -->
      <a-layout-footer class="footer">
        <div class="footer-content">
          <p>© 2024 百科系统 - 统一前端版本</p>
        </div>
      </a-layout-footer>
    </a-layout>
    
    <!-- 全局加载状态 -->
    <a-spin :spinning="globalLoading" size="large" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 响应式数据
const searchQuery = ref('')
const currentMenu = ref(['home'])
const globalLoading = ref(false)

// 计算属性
const menuKeyMap = {
  '/': 'home',
  '/entries': 'entries',
  '/categories': 'categories',
  '/login': 'auth',
  '/register': 'auth',
  '/profile': 'user'
}

// 方法
const handleSearch = (value) => {
  if (value.trim()) {
    router.push(`/search?q=${encodeURIComponent(value.trim())}`)
  }
}

const handleLogout = async () => {
  try {
    authStore.logout()
    message.success('已退出登录')
    router.push('/')
  } catch (error) {
    console.error('退出登录失败:', error)
    message.error('退出登录失败')
  }
}

// 生命周期
onMounted(() => {
  // 检查认证状态
  authStore.checkAuth()
  
  // 根据当前路由设置菜单高亮
  const path = route.path
  for (const [routePath, menuKey] of Object.entries(menuKeyMap)) {
    if (path.startsWith(routePath)) {
      currentMenu.value = [menuKey]
      break
    }
  }
})

// 监听路由变化
watch(route, (newRoute) => {
  const path = newRoute.path
  for (const [routePath, menuKey] of Object.entries(menuKeyMap)) {
    if (path.startsWith(routePath)) {
      currentMenu.value = [menuKey]
      break
    }
  }
})
</script>

<style scoped>
#app {
  min-height: 100vh;
}

.header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: fixed;
  width: 100%;
  top: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.logo h1 {
  margin: 0;
  color: #1890ff;
  font-size: 24px;
}

.logo a {
  text-decoration: none;
  color: inherit;
}

.search-container {
  flex: 1;
  max-width: 400px;
  margin: 0 24px;
}

.nav-menu {
  border-bottom: none;
  min-width: 300px;
}

.content {
  margin-top: 64px;
  min-height: calc(100vh - 128px);
  padding: 24px;
  background: #f0f2f5;
}

.footer {
  text-align: center;
  background: #001529;
  color: #fff;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    padding: 16px;
  }
  
  .search-container {
    margin: 16px 0;
    max-width: 100%;
  }
  
  .nav-menu {
    min-width: auto;
  }
  
  .content {
    padding: 16px;
  }
}
</style>