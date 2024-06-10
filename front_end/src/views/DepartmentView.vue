<template>
    <el-card class="box-card">
      <template v-slot:header>
        <div class="clearfix">
          <span>部门列表</span>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showAddDialog = true">增加</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showSearchDialog = true">搜索</el-button>
        </div>
      </template>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="departmentId" label="部门号">
            <template v-slot:default="scope">
                <span>{{scope.row.departmentId}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="departmentName" label="部门名称">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.departmentName" />
                <span v-else>{{scope.row.departmentName}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="branchId" label="所属支行号">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.branchId" disabled />
            <span v-else>{{scope.row.branchId}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="manager" label="部门管理者">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.manager" />
                <span v-else>{{scope.row.manager}}</span>
            </template>
        </el-table-column>
        <el-table-column label="操作">
          <template v-slot:default="scope">
            <el-button type="text" size="small" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="handleSave(scope.row)">保存</el-button>
            <el-button type="text" size="small" @click="handleDelete(scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[5, 10, 20]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total"></el-pagination>
    </el-card>
    <el-dialog title="添加部门" v-model ="showAddDialog">
      <el-form :model="addForm">
        <el-form-item label="部门号" label-width="100px">
          <el-input v-model="addForm.departmentId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="部门名称" label-width="100px">
          <el-input v-model="addForm.departmentName" autocomplete="off" />
        </el-form-item>
        <el-form-item label="所属支行号" label-width="100px">
          <el-input v-model="addForm.branchId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="部门管理者" label-width="100px">
          <el-input v-model="addForm.manager" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd()">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog title="搜索部门" v-model="showSearchDialog">
      <el-form :model="searchForm">
        <el-form-item label="支行号" label-width="100px">
          <el-input v-model="searchForm.branchId" autocomplete="off" /> 
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSearchDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSearch()">确定</el-button>
      </template>
    </el-dialog>
</template>
  
<script>
import { reactive, ref } from 'vue';
import { ElMessage ,ElMessageBox} from 'element-plus';
import  request  from '../utils/api';
import { onMounted } from 'vue';
export default {
  setup() {
    const tableData = ref([]); // 部门数据
    const showAddDialog = ref(false); // 控制添加部门对话框的显示
    const showSearchDialog = ref(false); // 控制搜索部门对话框的显示
    const currentPage = ref(1); // 当前页码
    const pageSize = ref(10); // 每页显示的条数
    const total = ref(0); // 总条数
    const addForm = reactive({
            departmentId: "",
            departmentName: "",
            branchId: "",
            manager: ""
        });
    const searchForm = reactive({
            branchId: "",
        });

    const loadData = async () => { 
      try {
        const response = await request.post('/api/departments/get/', searchForm, {
          params: { 
            page: currentPage.value,
            size: pageSize.value,
          },
        });
        if (response.data.code === 200) {
          tableData.value = response.data.data.data;
          total.value = response.data.data.count;
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
      row.editing = true; 
      // 编辑客户的逻辑
    };

    const handleSave = async (row) => {
      row.editing = false;
      try {
        const response = await request.put('/api/departments/edit/', row);
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
    const response = await request.delete('/api/departments/delete', {data: row});
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
        const response = await request.post('/api/departments/add/', addForm);
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