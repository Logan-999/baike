<template>
  <div class="login-container">
    <a-row type="flex" justify="center" align="middle" class="login-row">
      <a-col :xs="24" :sm="12" :md="8" :lg="6">
        <a-card class="login-card" :bordered="false">
          <template #title>
            <div class="login-title">
              <h2>登录百科系统</h2>
              <p>欢迎回来，请登录您的账户</p>
            </div>
          </template>

          <a-form
            :model="formState"
            name="login"
            autocomplete="off"
            @finish="onFinish"
            @finishFailed="onFinishFailed"
          >
            <a-form-item
              name="username"
              :rules="[{ required: true, message: '请输入用户名!' }]"
            >
              <a-input 
                v-model:value="formState.username" 
                size="large" 
                placeholder="用户名"
                prefix-icon="UserOutlined"
              >
                <template #prefix>
                  <UserOutlined />
                </template>
              </a-input>
            </a-form-item>

            <a-form-item
              name="password"
              :rules="[{ required: true, message: '请输入密码!' }]"
            >
              <a-input-password
                v-model:value="formState.password"
                size="large"
                placeholder="密码"
                prefix-icon="LockOutlined"
              >
                <template #prefix>
                  <LockOutlined />
                </template>
              </a-input-password>
            </a-form-item>

            <a-form-item>
              <a-button
                type="primary"
                html-type="submit"
                size="large"
                :loading="loading"
                block
              >
                登录
              </a-button>
            </a-form-item>
          </a-form>

          <div class="login-footer">
            <p>
              还没有账户？
              <router-link to="/register">立即注册</router-link>
            </p>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserOutlined, LockOutlined } from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'

const router = useRouter()
const authStore = useAuthStore()

const formState = reactive({
  username: '',
  password: ''
})

const loading = ref(false)

const onFinish = async (values) => {
  loading.value = true
  
  try {
    const result = await authStore.login(values)
    
    if (result.success) {
      message.success('登录成功！')
      
      // 跳转到首页或之前尝试访问的页面
      const redirectPath = router.currentRoute.value.query.redirect || '/'
      router.push(redirectPath)
    } else {
      message.error(result.error || '登录失败')
    }
  } catch (error) {
    console.error('登录异常:', error)
    message.error('登录过程中发生错误')
  } finally {
    loading.value = false
  }
}

const onFinishFailed = (errorInfo) => {
  console.log('登录表单验证失败:', errorInfo)
}
</script>

<style scoped>
.login-container {
  min-height: calc(100vh - 128px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-row {
  width: 100%;
}

.login-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.login-title {
  text-align: center;
  margin-bottom: 24px;
}

.login-title h2 {
  color: #1890ff;
  margin-bottom: 8px;
}

.login-title p {
  color: #666;
  margin: 0;
}

.login-footer {
  text-align: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.login-footer p {
  margin: 0;
  color: #666;
}

.login-footer a {
  color: #1890ff;
  text-decoration: none;
}

.login-footer a:hover {
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    padding: 16px;
  }
  
  .login-card {
    margin: 0;
  }
}
</style>