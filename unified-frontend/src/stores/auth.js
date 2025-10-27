import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import api from '@/services/api'
import { message } from 'ant-design-vue'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isAuthenticated = computed(() => !!token.value)
  const loading = ref(false)

  // 持久化token到localStorage
  watch(token, (newToken) => {
    if (newToken) {
      localStorage.setItem('token', newToken)
      api.defaults.headers.common['Authorization'] = `Token ${newToken}`
    } else {
      localStorage.removeItem('token')
      delete api.defaults.headers.common['Authorization']
    }
  })

  // 操作
  const login = async (credentials) => {
    loading.value = true
    try {
      const response = await api.post('/api/auth/login/', credentials)
      
      if (response.data.token) {
        token.value = response.data.token
        user.value = response.data.user
        message.success('登录成功')
        return { success: true, data: response.data }
      }
    } catch (error) {
      console.error('登录失败:', error)
      const errorMessage = error.response?.data?.message || '登录失败'
      message.error(errorMessage)
      return { 
        success: false, 
        error: errorMessage
      }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    token.value = null
    user.value = null
    message.success('已退出登录')
  }

  const register = async (userData) => {
    loading.value = true
    try {
      const response = await api.post('/api/auth/register/', {
        username: userData.username,
        email: userData.email,
        password: userData.password,
        password_confirm: userData.password_confirm
      })
      message.success('注册成功，请登录')
      return { success: true, data: response.data }
    } catch (error) {
      console.error('注册失败:', error)
      const errorMessage = error.response?.data?.message || '注册失败'
      message.error(errorMessage)
      return { 
        success: false, 
        error: errorMessage
      }
    } finally {
      loading.value = false
    }
  }

  const checkAuth = async () => {
    if (!token.value) return false
    
    try {
      // 验证token有效性
      const response = await api.get('/api/auth/check-auth/')
      if (response.data.is_authenticated) {
        user.value = response.data.user
        return true
      } else {
        logout()
        return false
      }
    } catch (error) {
      console.error('验证token失败:', error)
      logout()
      return false
    }
  }

  const updateProfile = async (profileData) => {
    try {
      const response = await api.put('/api/auth/profile/', profileData)
      user.value = response.data
      message.success('个人信息更新成功')
      return { success: true, data: response.data }
    } catch (error) {
      console.error('更新个人信息失败:', error)
      const errorMessage = error.response?.data?.message || '更新失败'
      message.error(errorMessage)
      return { 
        success: false, 
        error: errorMessage
      }
    }
  }

  return {
    user,
    token,
    isAuthenticated,
    loading,
    login,
    logout,
    register,
    checkAuth,
    updateProfile
  }
})