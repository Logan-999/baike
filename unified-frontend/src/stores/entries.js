import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'
import { message } from 'ant-design-vue'

export const useEntriesStore = defineStore('entries', () => {
  // 状态
  const entries = ref([])
  const currentEntry = ref(null)
  const loading = ref(false)
  const searchResults = ref([])
  const error = ref(null)
  const pagination = ref({
    current: 1,
    pageSize: 10,
    total: 0
  })

  // 计算属性
  const totalEntries = computed(() => entries.value.length)
  const hasEntries = computed(() => entries.value.length > 0)
  const hasSearchResults = computed(() => searchResults.value.length > 0)

  // 操作
  const fetchEntries = async (params = {}) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/entries/', { params })
      entries.value = response.data
      
      // 更新分页信息
      if (response.headers['x-total-count']) {
        pagination.value.total = parseInt(response.headers['x-total-count'])
      }
      
      return { success: true, data: response.data }
    } catch (error) {
      console.error('获取词条列表失败:', error)
      const errorMessage = error.response?.data?.message || '获取词条列表失败'
      error.value = errorMessage
      message.error(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const fetchEntry = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/api/entries/${id}/`)
      currentEntry.value = response.data
      return { success: true, data: response.data }
    } catch (error) {
      console.error('获取词条详情失败:', error)
      const errorMessage = error.response?.data?.message || '获取词条详情失败'
      error.value = errorMessage
      message.error(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const createEntry = async (entryData) => {
    error.value = null
    try {
      const response = await api.post('/api/entries/', entryData)
      entries.value.unshift(response.data)
      message.success('词条创建成功')
      return { success: true, data: response.data }
    } catch (error) {
      console.error('创建词条失败:', error)
      const errorMessage = error.response?.data?.message || '创建词条失败'
      error.value = errorMessage
      message.error(errorMessage)
      return { success: false, error: errorMessage }
    }
  }

  const updateEntry = async (id, entryData) => {
    error.value = null
    try {
      const response = await api.put(`/api/entries/${id}/`, entryData)
      const index = entries.value.findIndex(entry => entry.id === id)
      if (index !== -1) {
        entries.value[index] = response.data
      }
      if (currentEntry.value?.id === id) {
        currentEntry.value = response.data
      }
      message.success('词条更新成功')
      return { success: true, data: response.data }
    } catch (error) {
      console.error('更新词条失败:', error)
      const errorMessage = error.response?.data?.message || '更新词条失败'
      error.value = errorMessage
      message.error(errorMessage)
      return { success: false, error: errorMessage }
    }
  }

  const deleteEntry = async (id) => {
    error.value = null
    try {
      await api.delete(`/api/entries/${id}/`)
      entries.value = entries.value.filter(entry => entry.id !== id)
      if (currentEntry.value?.id === id) {
        currentEntry.value = null
      }
      message.success('词条删除成功')
      return { success: true }
    } catch (error) {
      console.error('删除词条失败:', error)
      const errorMessage = error.response?.data?.message || '删除词条失败'
      error.value = errorMessage
      message.error(errorMessage)
      return { success: false, error: errorMessage }
    }
  }

  const searchEntries = async (query) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/api/entries/', { 
        params: { search: query } 
      })
      searchResults.value = response.data
      return { success: true, data: response.data }
    } catch (error) {
      console.error('搜索词条失败:', error)
      const errorMessage = error.response?.data?.message || '搜索词条失败'
      error.value = errorMessage
      message.error(errorMessage)
      return { success: false, error: errorMessage }
    } finally {
      loading.value = false
    }
  }

  const clearSearchResults = () => {
    searchResults.value = []
    error.value = null
  }

  const clearError = () => {
    error.value = null
  }

  const setPagination = (page, pageSize) => {
    pagination.value.current = page
    pagination.value.pageSize = pageSize
  }

  return {
    // 状态
    entries,
    currentEntry,
    loading,
    searchResults,
    error,
    pagination,
    
    // 计算属性
    totalEntries,
    hasEntries,
    hasSearchResults,
    
    // 操作
    fetchEntries,
    fetchEntry,
    createEntry,
    updateEntry,
    deleteEntry,
    searchEntries,
    clearSearchResults,
    clearError,
    setPagination
  }
})