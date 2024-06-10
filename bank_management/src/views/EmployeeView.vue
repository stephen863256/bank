<template>
    <el-card class="box-card">
      <template v-slot:header>
        <div class="clearfix">
          <span>员工列表</span>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showAddDialog = true">增加</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showSearchDialog = true">搜索</el-button>
        </div>
      </template>
    <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="employeeId" label="员工号"></el-table-column>
        <el-table-column prop="idCard" label="身份证号">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.idCard" disabled />
            <span v-else>{{scope.row.idCard}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="name" label="姓名">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.name" />
            <span v-else>{{scope.row.name}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="gender" label="性别">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.gender" disabled />
            <span v-else>{{scope.row.gender}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="phoneNumber" label="手机号">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.phoneNumber" />
            <span v-else>{{scope.row.phoneNumber}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="address" label="住址">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.address" />
            <span v-else>{{scope.row.address}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="salary" label="工资">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.salary" />
            <span v-else>{{scope.row.salary}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="hireDate" label="入职时间">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.hireDate" disabled />
            <span v-else>{{scope.row.hireDate}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="position" label="职位">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.position" disabled/>
            <span v-else>{{scope.row.position}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="branchId" label="所属支行号">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.branchId" disabled/>
            <span v-else>{{scope.row.branchId}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="departmentId" label="所属部门号">
            <template v-slot:default="scope">
            <el-input v-if="scope.row.editing" v-model="scope.row.departmentId" />
            <span v-else>{{scope.row.departmentId}}</span>
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
    <el-dialog title="添加员工" v-model="showAddDialog">
  <el-form :model="addForm">
    <el-form-item label="身份证号" label-width="100px">
      <el-input v-model="addForm.idCard" autocomplete="off" />
    </el-form-item>
    <el-form-item label="姓名" label-width="100px">
      <el-input v-model="addForm.name" autocomplete="off" />
    </el-form-item>
    <el-form-item label="性别" label-width="100px">
      <el-input v-model="addForm.gender" autocomplete="off" />
    </el-form-item>
    <el-form-item label="手机号" label-width="100px">
      <el-input v-model="addForm.phoneNumber" autocomplete="off" />
    </el-form-item>
    <el-form-item label="地址" label-width="100px">
      <el-input v-model="addForm.address" autocomplete="off" />
    </el-form-item>
    <el-form-item label="工资" label-width="100px">
      <el-input v-model="addForm.salary" autocomplete="off" />
    </el-form-item>
    <el-form-item label="入职时间" label-width="100px">
      <el-date-picker
        v-model="addForm.hireDate"
        type="date"
        placeholder="选择日期"
      />
    </el-form-item>
    <el-form-item label="职位" label-width="100px">
      <el-input v-model="addForm.position" autocomplete="off" />
    </el-form-item>
    <el-form-item label="部门号" label-width="100px">
      <el-input v-model="addForm.departmentId" autocomplete="off" />
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="showAddDialog = false">取消</el-button>
    <el-button type="primary" @click="handleAdd()">确定</el-button>
  </template>
</el-dialog>
<el-dialog title="搜索部门" v-model="showSearchDialog">
      <el-form :model="searchForm">
        <el-form-item label="员工号" label-width="100px">
          <el-input v-model="searchForm.employeeId" autocomplete="off" /> 
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
import { ElMessage,ElMessageBox } from 'element-plus';
import  request  from '../utils/api';
import { onMounted } from 'vue';
export default {
  setup() {
    const tableData = ref([]); // 员工数据
    const showAddDialog = ref(false); // 控制添加员工对话框的显示
    const showSearchDialog = ref(false); // 控制搜索员工对话框的显示
    const currentPage = ref(1); // 当前页码
    const pageSize = ref(10); // 每页显示的条数
    const total = ref(0); // 总条数
    const addForm = reactive({
      employeeId: "",
      idCard: "",
      name: "",
      gender: "",
      phoneNumber: "",
      address: "",
      salary: "",
      hireDate: "",
      position: "",
      //branchId: "",
      departmentId: ""
    });

    const searchForm = reactive({
      employeeId: "",
    });
    const loadData = async () => { 
      try {
        const response = await request.post('/api/employees/get/', searchForm, {
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

    const handleAdd = async () => {
      try {
        const response = await request.post('/api/employees/add/', addForm);
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

    const handleEdit = (row) => {
      // 编辑员工的逻辑
      row.editing = true;
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
    const handleSave = async (row) => {
      row.editing = false;
      try {
        const response = await request.put('/api/employees/edit/', row);
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
    const response = await request.delete('/api/employees/delete', {data: row});
    if (response.data.code === 200) {
      // 删除成功
      console.log('Delete successful');
      // 重新加载数据
      loadData();
    } else {
      // 删除失败
      ElMessage.error(response.data.code + ":" + response.data.message);
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