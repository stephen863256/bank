<template>
  <el-card class="box-card">
    <template v-slot:header>
      <div class="clearfix">
        <span>用户列表</span>
        <el-button style="float: right; padding: 3px 0" type="primary" @click="showAddDialog = true">增加</el-button>
        <el-button style="float: right; padding: 3px 0" type="primary" @click="showSearchDialog = true">搜索</el-button>
      </div>
    </template>
    <el-table :data="tableData" style="width: 100%">
      <el-table-column prop="username" label="用户名">
          <template v-slot:default="scope">
              <span>{{scope.row.username}}</span>
          </template>
      </el-table-column>
      <el-table-column prop="password" label="密码">
          <template v-slot:default="scope">
              <el-input v-if="scope.row.editing" v-model="scope.row.password" type="password" />
              <span v-else>{{scope.row.password}}</span>
          </template>
      </el-table-column>
      <el-table-column label="操作">
        <template v-slot:default="scope">
          <el-button type="text" size="small" @click="handleEdit(scope.row)">修改密码</el-button>
          <el-button type="text" size="small" @click="handleSave(scope.row)">保存</el-button>
          <el-button type="text" size="small" @click="handleDelete(scope.row)">删除</el-button>
        </template>
      </el-table-column> 
    </el-table>
    <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[5, 10, 20]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total"></el-pagination>
  </el-card>
  <el-dialog title="添加用户" v-model ="showAddDialog">
    <el-form :model="addForm">
      <el-form-item label="用户名" label-width="100px">
        <el-input v-model="addForm.username" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" label-width="100px">
        <el-input v-model="addForm.password" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showAddDialog = false">取消</el-button>
      <el-button type="primary" @click="handleAdd()">确定</el-button>
    </template>
  </el-dialog>

  <el-dialog title="搜索用户" v-model="showSearchDialog">
    <el-form :model="searchForm">
      <el-form-item label="用户名" label-width="100px">
        <el-input v-model="searchForm.username" autocomplete="off" /> 
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showSearchDialog = false">取消</el-button>
      <el-button type="primary" @click="handleSearch()">确定</el-button>
    </template>
  </el-dialog>
</template>
  
<script>
import { reactive,ref } from 'vue';
import  request  from '../utils/api.ts';
import { ElMessage,ElMessageBox } from 'element-plus';
import { onMounted } from 'vue';
export default {
  setup() {
    const tableData = ref([]); // 用户数据
    const showAddDialog = ref(false); // 控制添加用户对话框的显示
    const showSearchDialog = ref(false); // 控制搜索用户对话框的显示
    const currentPage = ref(1); // 当前页码
    const pageSize = ref(10); // 每页显示的条数
    const total = ref(0); // 总条数
    const addForm = reactive({ 
            username: "",
            password: "",
        });
    const searchForm = reactive({
            username: "",
        });
    const loadData = async () => {
      try {
        const response = await request.post('/api/users/get/', searchForm, {
          params: {
            page: currentPage.value,
            size: pageSize.value, 
          },
        });
        if (response.data.code === 200) {
          tableData.value = response.data.data.data;
          total.value = response.data.data.count;
          console.log(response.data.data.data);
          console.log(response.data.data.count);
        } else {
          ElMessage.error(response.data.code + ":" + response.data.message);
          console.error(response.data.code + ":" + response.data.message);
        }
      } catch (error) {
        ElMessage.error(error);
        console.error(error);
      }
    };

    onMounted  (() => {
      console.log('onMounted');
      loadData();
    });
      
    const handleEdit = (row) => {
      // 编辑用户的逻辑
      row.editing = true;
    };

    const handleSave = async (row) => { 
      // 保存用户的逻辑
      row.editing = false;
      try {
        const response = await request.put('/api/users/edit/', row);
        if (response.data.code === 200) {
          // 更新成功
          console.log('Update successful');
          // 重新加载数据
        } else {
          // 更新失败
          ElMessage.error(response.data.code + ":" + response.data.message);
          console.log('Update failed');
        }
      } catch (error) {
        // 处理错误
        ElMessage.error(error);
        console.log('Error:', error);
      }
      loadData();
    };

    const handleDelete = async(row) => {
  // 弹出确认框
  try {
    await ElMessageBox.confirm('确定删除这条记录吗?', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });

    // 用户点击了确定按钮，执行删除操作
    const response = await request.delete('/api/users/delete', {data: row});
    if (response.data.code === 200) {
      // 删除成功
      console.log('Delete successful');
      // 重新加载数据
      loadData();
    } else {
      // 删除失败
      ElMessage.error(response.data.code + ":" + response.data.message);
      console.log('Delete failed');
    }
  } catch (error) {
    // 用户点击了取消按钮或删除操作出错
    if (error !== 'cancel') {
      // 处理错误
      ElMessage.error(error);
      console.log('Error:', error);
    }
  }
};

    const handleSizeChange = (val) => {
      pageSize.value = val;
      // 更新每页显示的条数
      loadData();
    };

    const handleCurrentChange = (val) => {
      currentPage.value = val;
      // 更新当前页码
      loadData();
    };

    const handleAdd = async () => {
      try {
        const response = await request.post('/api/users/add/', addForm);
        if (response.data.code === 200) {
          // 添加成功
          console.log('Add successful');
          // 关闭添加对话框
          showAddDialog.value = false;
          // 重新加载数据
          loadData();
        } else {
          // 添加失败
          ElMessage.error(response.data.code + ":" + response.data.message);
          console.log('Add failed');
        }
      } catch (error) {
        // 处理错误
        ElMessage.error(error);
        console.log('Error:', error);
      }
      showAddDialog.value = false;
      for(let key in addForm){
        addForm[key] = "";
      }
    };

    const handleSearch = async () => {
      // 搜索客户的逻辑
      await loadData();
      showSearchDialog.value = false;
      for(let key in searchForm){
        searchForm[key] = "";
      } 
    };

    return {
      tableData,
      showAddDialog,
      showSearchDialog,
      currentPage,
      pageSize,
      total,
      addForm,
      searchForm,
      loadData,
      onMounted,
      handleEdit,
      handleSave,
      handleDelete,
      handleSizeChange,
      handleCurrentChange,
      handleAdd,
      handleSearch
    };
  }
};
  </script>