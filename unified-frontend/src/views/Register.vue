<template>
  <div class="register-container">
    <a-row type="flex" justify="center" align="middle" class="register-row">
      <a-col :xs="24" :sm="12" :md="8" :lg="6">
        <a-card class="register-card" :bordered="false">
          <template #title>
            <div class="register-title">
              <h2>注册新账户</h2>
              <p>加入百科系统，开始分享知识</p>
            </div>
          </template>

          <a-form
            :model="formState"
            name="register"
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
              name="email"
              :rules="[
                { required: true, message: '请输入邮箱!' },
                { type: 'email', message: '请输入有效的邮箱地址!' }
              ]"
            >
              <a-input 
                v-model:value="formState.email" 
                size="large" 
                placeholder="邮箱"
                prefix-icon="MailOutlined"
              >
                <template #prefix>
                  <MailOutlined />
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

            <a-form-item
              name="password_confirm"
              :rules="[
                { required: true, message: '请确认密码!' },
                { validator: validatePassword }
              ]"
            >
              <a-input-password
                v-model:value="formState.password_confirm"
                size="large"
                placeholder="确认密码"
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
                注册
              </a-button>
            </a-form-item>
          </a-form>

          <div class="register-footer">
            <p>
              已有账户？
              <router-link to="/login">立即登录</router-link>
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
import { UserOutlined, MailOutlined, LockOutlined } from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'

const router = useRouter()
const authStore = useAuthStore()

const formState = reactive({
  username: '',
  email: '',
  password: '',
  password_confirm: ''
})

const loading = ref(false)

const validatePassword = async (_rule, value) => {
  if (value === '') {
    return Promise.reject('请确认密码!')
  }
  if (value !== formState.password) {
    return Promise.reject('两次输入的密码不一致!')
  }
  return Promise.resolve()
}

const onFinish = async (values) => {
  loading.value = true
  
  try {
    const result = await authStore.register({
      username: values.username,
      email: values.email,
      password: values.password,
      password_confirm: values.password_confirm
    })
    
    if (result.success) {
      message.success('注册成功！请登录')
      router.push('/login')
    } else {
      message.error(result.error || '注册失败')
    }
  } catch (error) {
    console.error('注册异常:', error)
    message.error('注册过程中发生错误')
  } finally {
    loading.value = false
  }
}

const onFinishFailed = (errorInfo) => {
  console.log('注册表单验证失败:', errorInfo)
}
</script>

<style scoped>
.register-container {
  min-height: calc(100vh - 128px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-row {
  width: 100%;
}

.register-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.register-title {
  text-align: center;
  margin-bottom: 24px;
}

.register-title h2 {
  color: #1890ff;
  margin-bottom: 8px;
}

.register-title p {
  color: #666;
  margin: 0;
}

.register-footer {
  text-align: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

.register-footer p {
  margin: 0;
  color: #666;
}

.register-footer a {
  color: #1890ff;
  text-decoration: none;
}

.register-footer a:hover {
  text-decoration: underline;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .register-container {
    padding: 16px;
  }
  
  .register-card {
    margin: 0;
  }
}
</style>