<template>
  <div class="category-list">
    <!-- 页面标题和操作栏 -->
    <a-row type="flex" justify="space-between" align="middle" class="page-header">
      <a-col>
        <h1>分类管理</h1>
        <p class="page-description">管理词条分类和标签</p>
      </a-col>
      <a-col>
        <a-button 
          v-if="authStore.isAuthenticated"
          type="primary" 
          size="large"
          @click="showCreateModal"
        >
          <template #icon>
            <PlusOutlined />
          </template>
          新建分类
        </a-button>
      </a-col>
    </a-row>

    <!-- 分类列表 -->
    <a-card class="categories-card">
      <a-list
        :data-source="categories"
        :loading="loading"
        item-layout="horizontal"
      >
        <template #renderItem="{ item }">
          <a-list-item>
            <a-list-item-meta
              :description="item.description || '暂无描述'"
            >
              <template #title>
                <span class="category-name">{{ item.name }}</span>
                <a-tag color="blue" style="margin-left: 8px;">
                  {{ item.entry_count }} 个词条
                </a-tag>
              </template>
              <template #avatar>
                <a-avatar 
                  :style="{ backgroundColor: stringToColor(item.name) }"
                  size="large"
                >
                  {{ getCategoryInitial(item.name) }}
                </a-avatar>
              </template>
            </a-list-item-meta>
            
            <template #actions>
              <span class="category-date">
                创建时间: {{ formatDate(item.created_at) }}
              </span>
              
              <!-- 操作按钮 -->
              <span v-if="authStore.isAuthenticated">
                <a-button 
                  type="link" 
                  size="small"
                  @click="showEditModal(item)"
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
          </a-list-item>
        </template>
      </a-list>
    </a-card>
    
    <!-- 创建/编辑分类对话框 -->
    <a-modal
      v-model:open="modalVisible"
      :title="modalTitle"
      @ok="handleModalOk"
      @cancel="handleModalCancel"
    >
      <a-form
        ref="formRef"
        :model="formState"
        :rules="rules"
        layout="vertical"
      >
        <a-form-item label="分类名称" name="name">
          <a-input v-model:value="formState.name" placeholder="请输入分类名称" />
        </a-form-item>
        <a-form-item label="分类描述" name="description">
          <a-textarea 
            v-model:value="formState.description" 
            placeholder="请输入分类描述"
            :rows="3"
          />
        </a-form-item>
      </a-form>
    </a-modal>
    
    <!-- 删除确认对话框 -->
    <a-modal
      v-model:open="deleteModalVisible"
      title="确认删除"
      @ok="confirmDelete"
      @cancel="cancelDelete"
    >
      <p>确定要删除这个分类吗？此操作不可撤销。</p>
    </a-modal>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { PlusOutlined } from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'
import { message } from 'ant-design-vue'

const authStore = useAuthStore()

// 响应式数据
const categories = ref([])
const loading = ref(false)
const modalVisible = ref(false)
const deleteModalVisible = ref(false)
const modalTitle = ref('新建分类')
const editingCategory = ref(null)
const categoryToDelete = ref(null)

// 表单数据
const formState = reactive({
  name: '',
  description: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入分类名称', trigger: 'blur' },
    { min: 2, max: 50, message: '分类名称长度应在2-50个字符之间', trigger: 'blur' }
  ],
  description: [
    { max: 200, message: '分类描述不能超过200个字符', trigger: 'blur' }
  ]
}

// 方法
const fetchCategories = async () => {
  loading.value = true
  try {
    const response = await api.get('/api/categories/')
    categories.value = response.data
  } catch (error) {
    console.error('获取分类列表失败:', error)
    message.error('获取分类列表失败')
  } finally {
    loading.value = false
  }
}

const showCreateModal = () => {
  modalTitle.value = '新建分类'
  editingCategory.value = null
  formState.name = ''
  formState.description = ''
  modalVisible.value = true
}

const showEditModal = (category) => {
  modalTitle.value = '编辑分类'
  editingCategory.value = category
  formState.name = category.name
  formState.description = category.description || ''
  modalVisible.value = true
}

const handleModalOk = async () => {
  try {
    if (editingCategory.value) {
      // 编辑分类
      await api.put(`/api/categories/${editingCategory.value.id}/`, formState)
      message.success('分类更新成功')
    } else {
      // 创建分类
      await api.post('/api/categories/', formState)
      message.success('分类创建成功')
    }
    
    modalVisible.value = false
    fetchCategories() // 重新加载列表
  } catch (error) {
    console.error('保存分类失败:', error)
    const errorMessage = error.response?.data?.message || '保存分类失败'
    message.error(errorMessage)
  }
}

const handleModalCancel = () => {
  modalVisible.value = false
  editingCategory.value = null
}

const handleDelete = (id) => {
  categoryToDelete.value = id
  deleteModalVisible.value = true
}

const confirmDelete = async () => {
  if (!categoryToDelete.value) return
  
  try {
    await api.delete(`/api/categories/${categoryToDelete.value}/`)
    message.success('分类删除成功')
    fetchCategories() // 重新加载列表
  } catch (error) {
    console.error('删除分类失败:', error)
    const errorMessage = error.response?.data?.message || '删除分类失败'
    message.error(errorMessage)
  } finally {
    deleteModalVisible.value = false
    categoryToDelete.value = null
  }
}

const cancelDelete = () => {
  deleteModalVisible.value = false
  categoryToDelete.value = null
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

const getCategoryInitial = (name) => {
  if (!name) return '?'
  const nameStr = String(name)
  return nameStr.charAt(0) || '?'
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN')
}

// 生命周期
onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.category-list {
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

.categories-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.category-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #1890ff;
}

.category-date {
  color: #999;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .category-name {
    font-size: 1.1rem;
  }
}
</style>