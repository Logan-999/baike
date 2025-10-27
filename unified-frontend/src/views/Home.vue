<template>
  <div class="home">
    <!-- 英雄区域 -->
    <a-row class="hero-section">
      <a-col :span="24">
        <div class="hero-content">
          <h1>欢迎来到百科系统</h1>
          <p class="hero-description">
            一个现代化的知识分享平台，汇集各类专业知识和经验分享
          </p>
          
          <!-- 快速操作按钮 -->
          <div class="hero-actions">
            <a-button 
              type="primary" 
              size="large" 
              @click="$router.push('/entries')"
            >
              浏览词条
            </a-button>
            <a-button 
              v-if="authStore.isAuthenticated"
              size="large" 
              @click="$router.push('/entries/create')"
            >
              创建词条
            </a-button>
            <a-button 
              v-else
              size="large" 
              @click="$router.push('/login')"
            >
              立即登录
            </a-button>
          </div>
        </div>
      </a-col>
    </a-row>

    <!-- 特性介绍 -->
    <a-row :gutter="[24, 24]" class="features-section">
      <a-col :xs="24" :sm="12" :md="8">
        <a-card class="feature-card">
          <template #cover>
            <div class="feature-icon">📚</div>
          </template>
          <a-card-meta
            title="海量知识库"
            description="涵盖各个领域的专业知识，满足您的学习需求"
          />
        </a-card>
      </a-col>
      
      <a-col :xs="24" :sm="12" :md="8">
        <a-card class="feature-card">
          <template #cover>
            <div class="feature-icon">🔍</div>
          </template>
          <a-card-meta
            title="智能搜索"
            description="快速精准地找到您需要的知识和信息"
          />
        </a-card>
      </a-col>
      
      <a-col :xs="24" :sm="12" :md="8">
        <a-card class="feature-card">
          <template #cover>
            <div class="feature-icon">👥</div>
          </template>
          <a-card-meta
            title="社区协作"
            description="与志同道合的用户一起完善和分享知识"
          />
        </a-card>
      </a-col>
    </a-row>

    <!-- 最新词条 -->
    <a-row class="recent-entries-section">
      <a-col :span="24">
        <a-card title="最新词条" class="recent-entries-card">
          <a-list
            :data-source="recentEntries"
            :loading="loading"
            item-layout="horizontal"
          >
            <template #renderItem="{ item }">
              <a-list-item>
                <a-list-item-meta
                  :description="item.summary"
                >
                  <template #title>
                    <router-link :to="`/entries/${item.id}`">
                      {{ item.title }}
                    </router-link>
                  </template>
                  <template #avatar>
                    <a-avatar style="background-color: #87d068">
                      {{ getCategoryInitial(item.category?.name || item.category) }}
                    </a-avatar>
                  </template>
                </a-list-item-meta>
                
                <div class="entry-meta">
                  <span class="category">{{ item.category?.name || item.category || '未分类' }}</span>
                  <span class="author">by {{ item.author?.username || item.author || '未知用户' }}</span>
                  <span class="date">{{ formatDate(item.created_at) }}</span>
                </div>
              </a-list-item>
            </template>
          </a-list>
          
          <template #extra>
            <a-button type="link" @click="$router.push('/entries')">
              查看全部
            </a-button>
          </template>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useEntriesStore } from '@/stores/entries'

const authStore = useAuthStore()
const entriesStore = useEntriesStore()

const recentEntries = ref([])
const loading = ref(false)

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

const getCategoryInitial = (category) => {
  if (!category) return '?'
  const categoryStr = String(category)
  return categoryStr.charAt(0) || '?'
}

const fetchRecentEntries = async () => {
  loading.value = true
  try {
    const result = await entriesStore.fetchEntries({ limit: 5 })
    if (result.success) {
      recentEntries.value = result.data
    }
  } catch (error) {
    console.error('获取最新词条失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchRecentEntries()
})
</script>

<style scoped>
.home {
  max-width: 1200px;
  margin: 0 auto;
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 0;
  text-align: center;
  border-radius: 8px;
  margin-bottom: 48px;
}

.hero-content h1 {
  font-size: 3rem;
  margin-bottom: 16px;
  font-weight: 700;
}

.hero-description {
  font-size: 1.2rem;
  margin-bottom: 32px;
  opacity: 0.9;
}

.hero-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.features-section {
  margin-bottom: 48px;
}

.feature-card {
  text-align: center;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 48px;
  padding: 24px 0;
}

.recent-entries-card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border: none;
}

.entry-meta {
  display: flex;
  gap: 16px;
  align-items: center;
  font-size: 12px;
  color: #666;
}

.category {
  background: #f0f2f5;
  padding: 2px 8px;
  border-radius: 4px;
}

.author {
  color: #1890ff;
}

.date {
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .hero-content h1 {
    font-size: 2rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
  
  .hero-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .entry-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 4px;
  }
}
</style>