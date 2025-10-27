<template>
  <div class="entry-list">
    <!-- 页面标题和操作栏 -->
    <a-row type="flex" justify="space-between" align="middle" class="page-header">
      <a-col>
        <h1>词条列表</h1>
        <p class="page-description">浏览和搜索所有词条内容</p>
      </a-col>
      <a-col>
        <a-button 
          v-if="authStore.isAuthenticated"
          type="primary" 
          size="large"
          @click="$router.push('/entries/create')"
        >
          <template #icon>
            <PlusOutlined />
          </template>
          创建新词条
        </a-button>
      </a-col>
    </a-row>

    <!-- 搜索和筛选区域 -->
    <a-card class="filter-card">
      <a-row :gutter="[16, 16]">
        <a-col :xs="24" :sm="12" :md="8">
          <a-input-search
            v-model:value="searchQuery"
            placeholder="搜索词条标题或内容..."
            enter-button="搜索"
            @search="handleSearch"
            @change="handleSearchChange"
          />
        </a-col>
        
        <a-col :xs="24" :sm="12" :md="8">
          <a-select
            v-model:value="categoryFilter"
            placeholder="选择分类"
            style="width: 100%"
            allow-clear
            @change="handleFilterChange"
          >
            <a-select-option v-for="category in categories" :key="category" :value="category.name || category">
              {{ category.name || category }}
            </a-select-option>
          </a-select>
        </a-col>
        
        <a-col :xs="24" :sm="12" :md="8">
          <a-select
            v-model:value="sortBy"
            placeholder="排序方式"
            style="width: 100%"
            @change="handleSortChange"
          >
            <a-select-option value="-created_at">最新创建</a-select-option>
            <a-select-option value="created_at">最早创建</a-select-option>
            <a-select-option value="title">标题排序</a-select-option>
          </a-select>
        </a-col>
      </a-row>
    </a-card>

    <!-- 词条列表 -->
    <a-card class="entries-card">
      <a-list
        :data-source="entriesStore.entries"
        :loading="entriesStore.loading"
        :pagination="{
          current: entriesStore.pagination.current,
          pageSize: entriesStore.pagination.pageSize,
          total: entriesStore.pagination.total,
          showSizeChanger: true,
          showQuickJumper: true,
          showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`,
          onChange: handlePageChange,
          onShowSizeChange: handlePageSizeChange
        }"
        item-layout="vertical"
      >
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta
              :description="item.summary"
            >
              <template #title>
                <router-link :to="`/entries/${item.id}`" class="entry-title">
                  {{ item.title }}
                </router-link>
              </template>
              <template #avatar>
                <a-avatar 
                  :style="{ backgroundColor: stringToColor(item.category?.name || item.category) }"
                  size="large"
                >
                  {{ getCategoryInitial(item.category?.name || item.category) }}
                </a-avatar>
              </template>
            </a-list-item-meta>
            
            <div class="entry-content">
              <p class="entry-summary">{{ truncateText(item.summary, 200) }}</p>
            </div>
            
            <template #actions>
              <span>
                <EyeOutlined />
                {{ item.view_count || 0 }} 次浏览
              </span>
              <span>
                <LikeOutlined />
                {{ item.like_count || 0 }} 个赞
              </span>
              <span>
                <MessageOutlined />
                {{ item.comment_count || 0 }} 条评论
              </span>
              
              <!-- 操作按钮 -->
              <span v-if="authStore.isAuthenticated && authStore.user?.id === item.author?.id">
                <a-button 
                  type="link" 
                  size="small"
                  @click="handleEdit(item.id)"
                >
                  编辑
                </a-button>
                <a-button 
                  type="link" 
                  size="small"
                  danger
                  @click="handleDelete(item.id)"
                >
                  删除
                </a-button>
              </span>
            </template>
            
            <div class="entry-footer">
              <a-tag :color="stringToColor(item.category?.name)">
                {{ item.category?.name || '未分类' }}
              </a-tag>
              <span class="entry-author">作者: {{ item.author?.username || '未知用户' }}</span>
              <span class="entry-date">{{ formatDate(item.created_at) }}</span>
            </div>
          </a-list-item>
        </template>
      </a-list>
    </a-card>
    
    <!-- 删除确认对话框 -->
    <a-modal
      v-model:open="deleteModalVisible"
      title="确认删除"
      @ok="confirmDelete"
      @cancel="cancelDelete"
    >
      <p>确定要删除这个词条吗？此操作不可撤销。</p>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { 
  PlusOutlined, 
  EyeOutlined, 
  LikeOutlined, 
  MessageOutlined 
} from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useEntriesStore } from '@/stores/entries'
import { message, Modal } from 'ant-design-vue'

const router = useRouter()
const authStore = useAuthStore()
const entriesStore = useEntriesStore()

// 响应式数据
const searchQuery = ref('')
const categoryFilter = ref('')
const sortBy = ref('-created_at')
const categories = ref([])
const deleteModalVisible = ref(false)
const entryToDelete = ref(null)

// 方法
const handleSearch = (value) => {
  fetchEntries()
}

const handleSearchChange = (e) => {
  if (!e.target.value) {
    fetchEntries()
  }
}

const handleFilterChange = () => {
  fetchEntries()
}

const handleSortChange = () => {
  fetchEntries()
}

const handlePageChange = (page, pageSize) => {
  entriesStore.pagination.current = page
  entriesStore.pagination.pageSize = pageSize
  fetchEntries()
}

const handlePageSizeChange = (current, size) => {
  entriesStore.pagination.current = current
  entriesStore.pagination.pageSize = size
  fetchEntries()
}

const handleEdit = (id) => {
  router.push(`/entries/${id}/edit`)
}

const handleDelete = (id) => {
  entryToDelete.value = id
  deleteModalVisible.value = true
}

const confirmDelete = async () => {
  if (!entryToDelete.value) return
  
  try {
    const result = await entriesStore.deleteEntry(entryToDelete.value)
    if (result.success) {
      message.success('词条删除成功')
      fetchEntries() // 重新加载列表
    } else {
      message.error('删除失败')
    }
  } catch (error) {
    console.error('删除词条异常:', error)
    message.error('删除过程中发生错误')
  } finally {
    deleteModalVisible.value = false
    entryToDelete.value = null
  }
}

const cancelDelete = () => {
  deleteModalVisible.value = false
  entryToDelete.value = null
}

const stringToColor = (str) => {
  if (!str) return '#87d068'
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  const colors = ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#fa541c']
  return colors[Math.abs(hash) % colors.length]
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const getCategoryInitial = (category) => {
  if (!category) return '?'
  const categoryStr = String(category)
  return categoryStr.charAt(0) || '?'
}

const fetchEntries = async () => {
  const params = {
    search: searchQuery.value,
    category: categoryFilter.value,
    ordering: sortBy.value
  }
  
  await entriesStore.fetchEntries(params)
  
  // 提取分类列表
  if (entriesStore.entries.length > 0) {
    const uniqueCategories = [...new Set(entriesStore.entries.map(entry => entry.category?.name || entry.category).filter(Boolean))]
    categories.value = uniqueCategories
  }
}

// 生命周期
onMounted(() => {
  fetchEntries()
})

// 监听路由参数变化
watch(() => router.currentRoute.value.query, (newQuery) => {
  if (newQuery.search) {
    searchQuery.value = newQuery.search
    fetchEntries()
  }
}, { immediate: true })
</script>

<style scoped>
.entry-list {
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0;
  color: #1890ff;
  font-size: 2rem;
}

.page-description {
  margin: 8px 0 0 0;
  color: #666;
}

.filter-card {
  margin-bottom: 24px;
}

.entries-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.entry-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1890ff;
  text-decoration: none;
}

.entry-title:hover {
  text-decoration: underline;
}

.entry-summary {
  color: #666;
  line-height: 1.6;
  margin: 8px 0 0 0;
}

.entry-footer {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.entry-author {
  color: #666;
  font-size: 0.9rem;
}

.entry-date {
  color: #999;
  font-size: 0.8rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .entry-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>