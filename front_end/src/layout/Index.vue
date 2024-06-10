<template>
    <div class="common-layout">
      <el-container>
        <el-header class="header"> <Header /></el-header>
        <el-container>
          <el-aside class="sidebar" width="200px"> <SideBar /></el-aside>
          <el-main>
            <router-view />
          </el-main>
        </el-container>
      </el-container>
    </div>
  </template>
  

<script>
import SideBar from './SideBar.vue'
import Header from './Header.vue'

export default {
  name: 'IndexLayout',
  components: {
    SideBar,
    Header
  }
}
</script>

<style>
.header {
  margin-bottom: 10px; /* 添加底部边距 */
}

.sidebar {
  margin-top: 10px; /* 添加顶部边距 */
}
</style>