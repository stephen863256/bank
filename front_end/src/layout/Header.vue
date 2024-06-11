<template>
    <el-header>
      <div class="header-content">
        <h1>银行管理系统</h1>
        <el-dropdown>
          <span class="el-dropdown-link">
          <img :src="avatar" class="user-avatar" alt="User Avatar" /> <!-- 添加这一行 -->
          {{ username }}
          <el-icon class="el-icon--right">
            <arrow-down />
          </el-icon>
        </span>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="handleUserCenter">用户中心</el-dropdown-item>
              <el-dropdown-item @click="handleLogout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </el-header>
  </template>
  
  <script>
  import { computed } from 'vue';
  import { useStore } from 'vuex';
  import router from '@/router';
  import { ArrowDown } from '@element-plus/icons-vue'
  
  export default {
    name: 'AppHeader',
    components: {
      ArrowDown
    },
    setup() {
      const store = useStore();
      const username = computed(() => store.state.user?.username);
      const avatar = sessionStorage.getItem('avatar');
  
      const handleUserCenter = () => {
        console.log('用户中心被点击');
        router.push('/usercenter')
      };
  
      const handleLogout = () => {
        console.log('退出登录被点击');
        store.dispatch('clearUser');
        sessionStorage.clear();
        router.replace('/login')
      };
  
      return {
        username,
        avatar,
        handleUserCenter,
        handleLogout
      };
    }
  }
  </script>
  
  <style scoped>
  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background-color: #ADD8E6;
  }
  
  .el-dropdown-link {
    cursor: pointer;
    color: #000000; /* 更改为黑色 */
    padding: 10px 15px; /* 添加一些内边距 */
    border-radius: 5px; /* 添加圆角 */
    font-size: 1.2em; /* 增加字体大小 */
    font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif; 
    display: flex;
    align-items: center; 
  }
  
  .user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  margin-right: 10px;
  }

  h1 {
    color:#000000; 
    font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif
  }
  </style>