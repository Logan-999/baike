import { useAuthStore } from './auth'
import { useEntriesStore } from './entries'

// 集中导出所有store，便于统一管理
export { useAuthStore, useEntriesStore }

// 可选：创建全局store管理函数
export const useStore = () => {
  return {
    auth: useAuthStore(),
    entries: useEntriesStore()
  }
}