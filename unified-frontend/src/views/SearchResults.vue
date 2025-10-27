<template>
  <div class="search-results">
    <a-row type="flex" justify="space-between" align="middle" class="page-header">
      <a-col>
        <h1>搜索结果</h1>
        <p class="page-description">搜索 "{{ searchQuery }}" 的结果</p>
      </a-col>
      <a-col>
        <span class="result-count">找到 {{ results.length }} 个结果</span>
      </a-col>
    </a-row>

    <div v-if="loading" class="loading-container">
      <a-spin size="large" />
      <p>正在搜索中...</p>
    </div>

    <div v-else-if="results.length === 0" class="no-results">
      <a-card>
        <a-empty description="没有找到相关结果">
          <template #description>
            <p>没有找到与 "{{ searchQuery }}" 相关的词条</p>
            <p>请尝试使用其他关键词或检查拼写</p>
          </template>
        </a-empty>
      </a-card>
    </div>

    <div v-else class="results-container">
      <a-list
        :data-source="results"
        :loading="loading"
        item-layout="vertical"
        size="large"
      >
        <template #renderItem="{ item }">
          <a-list-item key="item.id">
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
                  :style="{ backgroundColor: stringToColor(item.category?.name || item.category || '未分类') }"
                  size="large"
                >
                  {{ getCategoryInitial(item.category?.name || item.category || '未分类') }}
                </a-avatar>
              </template>
            </a-list-item-meta>
            
            <div class="entry-meta">
              <a-tag :color="stringToColor(item.category?.name || item.category || '未分类')">
                {{ item.category?.name || item.category || '未分类' }}
              </a-tag>
              <span class="author">作者: {{ item.author?.username || item.author || '未知用户' }}</span>
              <span class="view-count">浏览: {{ item.view_count || 0 }}</span>
              <span class="like-count">点赞: {{ item.like_count || 0 }}</span>
              <span class="created-at">{{ formatDate(item.created_at) }}</span>
            </div>
          </a-list-item>
        </template>
      </a-list>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useEntriesStore } from '@/stores/entries'

const route = useRoute()
const entriesStore = useEntriesStore()
const searchQuery = ref('')
const results = ref([])
const loading = ref(false)

// 字符串转颜色函数
const stringToColor = (str) => {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  const hue = hash % 360
  return `hsl(${hue}, 70%, 65%)`
}

// 获取分类首字母
const getCategoryInitial = (categoryName) => {
  if (!categoryName || categoryName === '未分类') return '?'
  return categoryName.charAt(0).toUpperCase()
}

// 格式化日期
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 执行搜索
const performSearch = async (query) => {
  if (!query.trim()) {
    results.value = []
    return
  }
  
  loading.value = true
  try {
    const response = await entriesStore.searchEntries(query)
    if (response.success) {
      results.value = response.data
    } else {
      results.value = []
    }
  } catch (error) {
    console.error('搜索失败:', error)
    results.value = []
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  searchQuery.value = route.query.q || ''
  if (searchQuery.value) {
    performSearch(searchQuery.value)
  }
})

// 监听路由变化
watch(() => route.query.q, (newQuery) => {
  searchQuery.value = newQuery || ''
  if (searchQuery.value) {
    performSearch(searchQuery.value)
  } else {
    results.value = []
  }
})
</script>

<style scoped>
.search-results {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.page-header {
  margin-bottom: 32px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.page-header h1 {
  margin: 0;
  color: #1890ff;
  font-size: 2rem;
  font-weight: 600;
}

.page-description {
  margin: 8px 0 0 0;
  color: #666;
  font-size: 1.1rem;
}

.result-count {
  color: #666;
  font-size: 1rem;
  font-weight: 500;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
}

.loading-container p {
  margin-top: 16px;
  color: #666;
}

.no-results {
  margin-top: 40px;
}

.results-container {
  margin-top: 24px;
}

.entry-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1890ff;
  text-decoration: none;
  transition: color 0.3s;
}

.entry-title:hover {
  color: #40a9ff;
}

.entry-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-top: 12px;
  flex-wrap: wrap;
}

.entry-meta .author,
.entry-meta .view-count,
.entry-meta .like-count,
.entry-meta .created-at {
  color: #666;
  font-size: 0.9rem;
}

.entry-meta .author {
  font-weight: 500;
}

@media (max-width: 768px) {
  .search-results {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    text-align: center;
  }
  
  .entry-meta {
    gap: 8px;
  }
  
  .entry-meta .author,
  .entry-meta .view-count,
  .entry-meta .like-count,
  .entry-meta .created-at {
    font-size: 0.8rem;
  }
}
</style>