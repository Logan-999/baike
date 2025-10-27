<template>
  <div class="entry-edit">
    <!-- 页面标题 -->
    <a-row type="flex" justify="space-between" align="middle" class="page-header">
      <a-col>
        <h1>编辑词条</h1>
        <p class="page-description">修改和完善词条内容</p>
      </a-col>
      <a-col>
        <a-button 
          type="default" 
          size="large"
          @click="$router.push('/entries')"
        >
          返回词条列表
        </a-button>
      </a-col>
    </a-row>

    <!-- 编辑词条表单 -->
    <a-card class="edit-form-card">
      <a-form
        ref="formRef"
        :model="formState"
        :rules="rules"
        layout="vertical"
        @finish="handleSubmit"
      >
        <a-row :gutter="[24, 16]">
          <a-col :xs="24" :md="16">
            <a-form-item label="词条标题" name="title">
              <a-input 
                v-model:value="formState.title" 
                placeholder="请输入词条标题"
                size="large"
              />
            </a-form-item>
          </a-col>
          
          <a-col :xs="24" :md="8">
            <a-form-item label="分类" name="category">
              <a-select
                v-model:value="formState.category"
                placeholder="选择分类"
                size="large"
                allow-clear
                :loading="categoriesLoading"
              >
                <a-select-option 
                  v-for="category in categories" 
                  :key="category.id" 
                  :value="category.id"
                >
                  {{ category.name }}
                </a-select-option>
              </a-select>
            </a-form-item>
          </a-col>
        </a-row>

        <a-form-item label="摘要" name="summary">
          <a-textarea 
            v-model:value="formState.summary" 
            placeholder="请输入词条摘要（可选）"
            :rows="3"
            show-count
            :maxlength="500"
          />
        </a-form-item>

        <a-form-item label="词条内容" name="content">
          <a-textarea 
            v-model:value="formState.content" 
            placeholder="请输入详细的词条内容"
            :rows="12"
            show-count
            :maxlength="10000"
          />
        </a-form-item>

        <a-form-item name="is_published">
          <a-checkbox v-model:checked="formState.is_published">
            发布词条
          </a-checkbox>
        </a-form-item>

        <a-form-item>
          <a-space size="large">
            <a-button 
              type="primary" 
              size="large" 
              html-type="submit"
              :loading="submitting"
            >
              更新词条
            </a-button>
            <a-button 
              size="large" 
              @click="handleReset"
            >
              重置修改
            </a-button>
            <a-button 
              type="danger" 
              size="large" 
              @click="handleDelete"
            >
              删除词条
            </a-button>
          </a-space>
        </a-form-item>
      </a-form>
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
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useEntriesStore } from '@/stores/entries'
import api from '@/services/api'
import { message } from 'ant-design-vue'

const router = useRouter()
const route = useRoute()
const entriesStore = useEntriesStore()

// 响应式数据
const categories = ref([])
const categoriesLoading = ref(false)
const submitting = ref(false)
const deleteModalVisible = ref(false)
const entryId = ref(null)

// 表单数据
const formState = reactive({
  title: '',
  content: '',
  summary: '',
  category: null,
  is_published: true
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入词条标题', trigger: 'blur' },
    { min: 2, max: 200, message: '标题长度应在2-200个字符之间', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入词条内容', trigger: 'blur' },
    { min: 10, message: '词条内容至少需要10个字符', trigger: 'blur' }
  ],
  summary: [
    { max: 500, message: '摘要不能超过500个字符', trigger: 'blur' }
  ]
}

// 方法
const fetchCategories = async () => {
  categoriesLoading.value = true
  try {
    const response = await api.get('/api/categories/')
    categories.value = response.data
  } catch (error) {
    console.error('获取分类列表失败:', error)
    message.error('获取分类列表失败')
  } finally {
    categoriesLoading.value = false
  }
}

const fetchEntry = async () => {
  try {
    const result = await entriesStore.fetchEntry(entryId.value)
    if (result.success) {
      const entry = result.data
      formState.title = entry.title
      formState.content = entry.content
      formState.summary = entry.summary || ''
      formState.category = entry.category?.id || null
      formState.is_published = entry.is_published
    }
  } catch (error) {
    console.error('获取词条详情失败:', error)
    message.error('获取词条详情失败')
    router.push('/entries')
  }
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    const result = await entriesStore.updateEntry(entryId.value, formState)
    if (result.success) {
      message.success('词条更新成功！')
      router.push(`/entries/${entryId.value}`)
    }
  } catch (error) {
    console.error('更新词条失败:', error)
  } finally {
    submitting.value = false
  }
}

const handleReset = () => {
  // 重置为原始值
  fetchEntry()
}

const handleDelete = () => {
  deleteModalVisible.value = true
}

const confirmDelete = async () => {
  try {
    const result = await entriesStore.deleteEntry(entryId.value)
    if (result.success) {
      message.success('词条删除成功')
      router.push('/entries')
    }
  } catch (error) {
    console.error('删除词条失败:', error)
  } finally {
    deleteModalVisible.value = false
  }
}

const cancelDelete = () => {
  deleteModalVisible.value = false
}

// 生命周期
onMounted(() => {
  entryId.value = route.params.id
  if (entryId.value) {
    fetchCategories()
    fetchEntry()
  } else {
    message.error('词条ID不存在')
    router.push('/entries')
  }
})
</script>

<style scoped>
.entry-edit {
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

.edit-form-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
  
  .edit-form-card {
    margin: 0 -16px;
    border-radius: 0;
    box-shadow: none;
    border-top: 1px solid #f0f0f0;
    border-bottom: 1px solid #f0f0f0;
  }
}
</style>