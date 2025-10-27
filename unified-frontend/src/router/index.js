import { defineAsyncComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'

// 异步加载组件，优化性能
const Home = defineAsyncComponent(() => import('@/views/Home.vue'))
const EntryList = defineAsyncComponent(() => import('@/views/EntryList.vue'))
const EntryDetail = defineAsyncComponent(() => import('@/views/EntryDetail.vue'))
const EntryCreate = defineAsyncComponent(() => import('@/views/EntryCreate.vue'))
const EntryEdit = defineAsyncComponent(() => import('@/views/EntryEdit.vue'))
const CategoryList = defineAsyncComponent(() => import('@/views/CategoryList.vue'))
const Login = defineAsyncComponent(() => import('@/views/Login.vue'))
const Register = defineAsyncComponent(() => import('@/views/Register.vue'))
const Profile = defineAsyncComponent(() => import('@/views/Profile.vue'))
const SearchResults = defineAsyncComponent(() => import('@/views/SearchResults.vue'))

// 路由守卫函数
const authGuard = (to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // 重定向到登录页面
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else {
    next()
  }
}

// 错误处理组件
const ErrorPage = defineAsyncComponent(() => import('@/views/ErrorPage.vue'))

export const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
    meta: { title: '首页' }
  },
  {
    path: '/entries',
    name: 'EntryList',
    component: EntryList,
    meta: { title: '词条列表' }
  },
  {
    path: '/entries/:id',
    name: 'EntryDetail',
    component: EntryDetail,
    meta: { title: '词条详情' }
  },
  {
    path: '/entries/create',
    name: 'EntryCreate',
    component: EntryCreate,
    meta: { title: '创建词条', requiresAuth: true },
    beforeEnter: authGuard
  },
  {
    path: '/entries/:id/edit',
    name: 'EntryEdit',
    component: EntryEdit,
    meta: { title: '编辑词条', requiresAuth: true },
    beforeEnter: authGuard
  },
  {
    path: '/categories',
    name: 'CategoryList',
    component: CategoryList,
    meta: { title: '分类管理' }
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
    meta: { title: '注册' }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { title: '个人中心', requiresAuth: true },
    beforeEnter: authGuard
  },
  {
    path: '/search',
    name: 'SearchResults',
    component: SearchResults,
    meta: { title: '搜索结果' }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: ErrorPage,
    meta: { title: '页面未找到' }
  }
]