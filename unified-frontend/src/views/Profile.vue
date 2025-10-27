<template>
  <div class="profile">
    <h1>个人中心</h1>
    <p>管理您的个人信息和词条</p>
    
    <!-- 用户信息卡片 -->
    <div class="user-info">
      <h2>用户信息</h2>
      <p>用户名: {{ userInfo.username }}</p>
      <p>邮箱: {{ userInfo.email }}</p>
    </div>

    <!-- 数据可视化图表区域 -->
    <div class="charts-section">
      <h2>数据统计</h2>
      
      <!-- 词条统计趋势图 -->
      <a-card title="词条统计趋势" class="chart-card">
        <ReactChartWrapper 
          :component="EntryStatsChart" 
          :componentProps="{ data: chartData }"
        />
      </a-card>
      
      <!-- 词条分类分布图 -->
      <a-card title="词条分类分布" class="chart-card">
        <ReactChartWrapper 
          :component="CategoryDistributionChart" 
          :componentProps="{ data: categoryData }"
        />
      </a-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import ReactChartWrapper from '@/components/ReactChartWrapper.vue'
import EntryStatsChart from '@/components/react-charts/EntryStatsChart.jsx'
import CategoryDistributionChart from '@/components/react-charts/CategoryDistributionChart.jsx'

const authStore = useAuthStore()

// 用户信息
const userInfo = reactive({
  username: '',
  email: ''
})

// 图表数据
const chartData = ref([])
const categoryData = ref([])

// 获取用户信息
const fetchUserInfo = async () => {
  try {
    if (authStore.user) {
      userInfo.username = authStore.user.username
      userInfo.email = authStore.user.email || '未设置邮箱'
    }
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

// 获取图表数据
const fetchChartData = async () => {
  try {
    // 调用后端API获取真实的统计数据
    const response = await api.get('/api/encyclopedia/statistics/')
    const data = response.data
    
    // 设置月度统计数据
    chartData.value = data.monthly_stats || [
      { date: '2024-01', 词条数: 12, 浏览量: 156, 点赞数: 8 },
      { date: '2024-02', 词条数: 18, 浏览量: 234, 点赞数: 15 },
      { date: '2024-03', 词条数: 25, 浏览量: 345, 点赞数: 22 },
      { date: '2024-04', 词条数: 32, 浏览量: 421, 点赞数: 28 },
      { date: '2024-05', 词条数: 40, 浏览量: 512, 点赞数: 35 },
      { date: '2024-06', 词条数: 48, 浏览量: 623, 点赞数: 42 },
    ]
    
    // 设置分类统计数据
    categoryData.value = data.category_stats || [
      { name: '技术', value: 15 },
      { name: '科学', value: 12 },
      { name: '历史', value: 8 },
      { name: '文化', value: 10 },
      { name: '生活', value: 5 },
      { name: '其他', value: 3 },
    ]
    
    console.log('获取到统计数据:', data)
  } catch (error) {
    console.error('获取图表数据失败:', error)
    
    // 如果API调用失败，使用模拟数据作为后备
    chartData.value = [
      { date: '2024-01', 词条数: 12, 浏览量: 156, 点赞数: 8 },
      { date: '2024-02', 词条数: 18, 浏览量: 234, 点赞数: 15 },
      { date: '2024-03', 词条数: 25, 浏览量: 345, 点赞数: 22 },
      { date: '2024-04', 词条数: 32, 浏览量: 421, 点赞数: 28 },
      { date: '2024-05', 词条数: 40, 浏览量: 512, 点赞数: 35 },
      { date: '2024-06', 词条数: 48, 浏览量: 623, 点赞数: 42 },
    ]
    
    categoryData.value = [
      { name: '技术', value: 15 },
      { name: '科学', value: 12 },
      { name: '历史', value: 8 },
      { name: '文化', value: 10 },
      { name: '生活', value: 5 },
      { name: '其他', value: 3 },
    ]
  }
}

// 生命周期
onMounted(() => {
  fetchUserInfo()
  fetchChartData()
})
</script>

<style scoped>
.profile {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
}

.user-info {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #d9d9d9;
  border-radius: 8px;
}

.charts-section {
  margin-top: 40px;
}

.charts-section h2 {
  margin-bottom: 24px;
  color: #1890ff;
  border-bottom: 2px solid #1890ff;
  padding-bottom: 8px;
}

.chart-card {
  margin-bottom: 24px;
}

.chart-card :deep(.ant-card-body) {
  padding: 24px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .profile {
    padding: 16px;
  }
  
  .charts-section {
    margin-top: 24px;
  }
  
  .chart-card {
    margin-bottom: 16px;
  }
}
</style>