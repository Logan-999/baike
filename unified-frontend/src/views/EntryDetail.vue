<template>
  <div class="entry-detail">
    <a-row type="flex" justify="space-between" align="middle" class="page-header">
      <a-col>
        <h1>{{ entry?.title || '加载中...' }}</h1>
        <p class="page-description">词条详情页面</p>
      </a-col>
      <a-col>
        <a-button v-if="authStore.isAuthenticated && authStore.user?.id === entry?.author?.id" type="primary" @click="handleEdit">
          编辑词条
        </a-button>
      </a-col>
    </a-row>

    <a-card v-if="entry" class="entry-card">
      <div class="entry-meta">
        <a-tag :color="stringToColor(entry.category?.name || entry.category)">{{ entry.category?.name || entry.category || '未分类' }}</a-tag>
        <span class="author">作者: {{ entry.author?.username || entry.author || '未知用户' }}</span>
        <span class="date">创建时间: {{ formatDate(entry.created_at) }}</span>
        <span class="views">浏览: {{ entry.view_count || 0 }} 次</span>
      </div>

      <div class="entry-content">
        <h3>摘要</h3>
        <p>{{ entry.summary }}</p>
        
        <h3>详细内容</h3>
        <div v-html="entry.content || '暂无详细内容'"></div>
      </div>

      <div class="entry-actions">
        <a-button type="primary" @click="handleLike">
          <LikeOutlined />
          点赞 ({{ entry.like_count || 0 }})
        </a-button>
        <a-button @click="handleShare">
          <ShareAltOutlined />
          分享
        </a-button>
      </div>
    </a-card>

    <a-spin v-else :spinning="loading" size="large" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { LikeOutlined, ShareAltOutlined } from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { useEntriesStore } from '@/stores/entries'
import { message } from 'ant-design-vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const entriesStore = useEntriesStore()

const entry = ref(null)
const loading = ref(false)

const stringToColor = (str) => {
  if (!str) return '#87d068'
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    hash = str.charCodeAt(i) + ((hash << 5) - hash)
  }
  const colors = ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#fa541c']
  return colors[Math.abs(hash) % colors.length]
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN') + ' ' + date.toLocaleTimeString('zh-CN', { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

const handleEdit = () => {
  router.push(`/entries/${route.params.id}/edit`)
}

const handleLike = () => {
  message.info('点赞功能开发中...')
}

const handleShare = () => {
  message.info('分享功能开发中...')
}

const fetchEntry = async () => {
  loading.value = true
  try {
    const result = await entriesStore.fetchEntry(route.params.id)
    if (result.success) {
      entry.value = result.data
    } else {
      message.error('获取词条详情失败')
    }
  } catch (error) {
    console.error('获取词条详情异常:', error)
    message.error('获取词条详情过程中发生错误')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchEntry()
})
</script>

<style scoped>
.entry-detail {
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

.entry-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.entry-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.author, .date, .views {
  color: #666;
  font-size: 0.9rem;
}

.entry-content h3 {
  color: #1890ff;
  margin: 24px 0 16px 0;
}

.entry-content p {
  line-height: 1.6;
  color: #333;
}

.entry-actions {
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
  display: flex;
  gap: 16px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .entry-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .entry-actions {
    flex-direction: column;
  }
}
</style>