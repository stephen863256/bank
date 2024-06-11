<template>
    <div class="container">
    <h1 class="title">银行管理系统登录界面</h1> <!-- 添加这一行 -->
    <el-form
      ref="formRef"
      style="max-width: 600px;"
      :model="loginForm"
      label-width="auto"
      class="demo-ruleForm"
    >
      <el-form-item
        label="Username"
        prop="username"
        :rules="[
          { required: true, message: 'Username is required' },
        ]"
        class="label-style"
      >
        <el-input
          v-model="loginForm.username"
          type="text"
          autocomplete="off"
          class="input-style"
        />
      </el-form-item>
      <el-form-item
        label="Password"
        prop="password"
        :rules="[
          { required: true, message: 'Password is required' },
        ]"
        class="label-style"
      >
        <el-input
          v-model="loginForm.password"
          type="password"
          autocomplete="off"
          class="input-style"
        />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">Submit</el-button>
        <el-button @click="resetForm">Reset</el-button>
      </el-form-item>
    </el-form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue'
  import request from '@/utils/api.ts'
  import {useStore} from 'vuex'
  import { useRouter } from 'vue-router';
  import { ElMessage } from 'element-plus';

  export default {
    setup() {
      const store = useStore()
      const router = useRouter()
      const formRef = ref()
      const loginForm = ref({
        username: '',
        password: '',
      })
  
      const submitForm = async () => {
        const { username, password } = loginForm.value
        formRef.value.validate(async (valid) => {
          if (valid) { 
            try { 
              const response = await request.post('/api/login', { username, password })
              if (response.data.message != 'Login successful') {
                ElMessage.error('登录失败: ' + response.data.code + ": " + response.data.message);
                console.log('Login failed:',response.data.code,":",response.data.message)
              } else {
                ElMessage.success('登录成功');
                console.log('Login successful')
                let userDetails = {
                    username: username,
                    password: password,
                }
                store.dispatch('setUser', userDetails)
                sessionStorage.setItem('avatar', response.data.avatar)
                sessionStorage.setItem('token', response.data.token)
                //sessionStorage.setItem('user', JSON.stringify(userDetails))
                router.replace('/Layout')
              }
            } catch (error) {
              ElMessage.error('请求失败: ' + error);
              console.log('Request failed:', error)
            }
          } else {
            ElMessage.error('表单验证失败');
            console.log('Form validation failed')
          }
        })
      }
  
      const resetForm = () => {
        formRef.value.resetFields()
      }
  
      return {
        formRef,
        loginForm,
        submitForm,
        resetForm,
      }
    },
  }
  </script>

<style scoped>

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 200vw; 
  background-image: url('~@/assets/background.png');
  background-size: cover;
  background-position: center;
}

.input-style {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  color: #333;
  font-size: 16px;
}

.title {
  margin-bottom: 20px;
}

.label-style {
  color: #555;
  font-size: 20px;
  font-weight: bold;
}
</style>
