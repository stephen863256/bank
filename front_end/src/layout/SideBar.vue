<template>
  <el-menu
    default-active="2"
    class="el-menu-vertical-demo"
    @close="handleClose"
  >
    <el-menu-item
      v-for="route in filteredLayoutmap"
      :key="route.path"
      :index="route.path"
    >
      <router-link :to="'/layout/' + route.path">
        <span class="route-name">{{ route.name }}</span>
      </router-link>
    </el-menu-item>
  </el-menu> 
</template>

<script lang="ts" setup>
import { computed } from 'vue' 
import { useStore } from 'vuex'
import {Layoutmap} from '@/router/index'

const store = useStore()
const roles = computed(() => store.state.roles)
const filteredLayoutmap = computed(() => {
  return Layoutmap.filter(route => !route.meta || !route.meta.roles || roles.value.includes(route.meta.roles))
})

const handleClose = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
}

</script>

<style>
.el-menu-vertical-demo {
  width: 200px;
  min-height: 400px;
  border-left: 2px solid #333;
  background-color: #ADD8E6;
}

.route-name {
  color: #000000; /* 更改这里的颜色 */
  font-size: 16px; /* 更改这里的字体大小 */
  font-family:'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif
}
</style>