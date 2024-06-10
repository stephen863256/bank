<template>
    <el-card class="box-card">
      <template v-slot:header>
        <div class="clearfix">
          <span>信用账户列表</span>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showAddDialog = true">增加</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showSearchDialog = true">搜索</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showRepaymentDialog = true">还款</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showUseDialog = true">使用</el-button>
        </div>
      </template>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="accountId" label="账户号">
            <template v-slot:default="scope">
                <span>{{scope.row.accountId}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="branchCode" label="支行代码">
            <template v-slot:default="scope">
              <span>{{scope.row.branchCode}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="idNumber" label="客户身份证号">
            <template v-slot:default="scope">
                <span>{{scope.row.idNumber}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="password" label="密码">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.password" />
                <span v-else>{{scope.row.password}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="openDate" label="开户日期">
            <template v-slot:default="scope">
                <span>{{scope.row.openDate}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="creditBalance" label="额度余额">
            <template v-slot:default="scope">
                <span>{{scope.row.creditBalance}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="creditLimit" label="使用额度">
            <template v-slot:default="scope">
                <span>{{scope.row.creditLimit}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="lastRepaymentDate" label="最后还款日期">
            <template v-slot:default="scope">
                <span>{{scope.row.lastRepaymentDate}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="interestRate" label="利率">
            <template v-slot:default="scope">
                <span>{{scope.row.interestRate}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="interest" label="利息">
          <template v-slot:default="scope">
            <span>{{scope.row.interest}}</span>
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
    <el-dialog title="添加信用账户" v-model="showAddDialog">
    <el-form :model="addForm">
      <el-form-item label="支行代码" label-width="100px">
        <el-input v-model="addForm.branchCode" autocomplete="off" />
      </el-form-item>
      <el-form-item label="客户身份证号" label-width="100px">
        <el-input v-model="addForm.idNumber" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" label-width="100px">
        <el-input v-model="addForm.password" autocomplete="off" />
      </el-form-item>
      <el-form-item label="使用额度" label-width="100px">
        <el-input v-model="addForm.creditLimit" autocomplete="off" />
      </el-form-item>
      <el-form-item label="开户日期" label-width="100px">
        <el-date-picker v-model="addForm.openingDate" type="date" placeholder="选择日期" />
      </el-form-item>
      <el-form-item label="利率" label-width="100px">
        <el-input v-model="addForm.interestRate" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showAddDialog = false">取消</el-button>
      <el-button type="primary" @click="handleAdd()">确定</el-button>
    </template>
  </el-dialog>

    <el-dialog title="搜索信用账户" v-model="showSearchDialog">
      <el-form :model="searchForm">
        <el-form-item label="账户号" label-width="100px">
          <el-input v-model="searchForm.accountId" autocomplete="off" /> 
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSearchDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSearch()">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog title="还款" v-model="showRepaymentDialog">
      <el-form :model="repaymentForm">
        <el-form-item label="账户号" label-width="100px">
          <el-input v-model="repaymentForm.accountId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="还款日期" label-width="100px">
          <el-date-picker v-model="repaymentForm.repaymentDate" type="date" placeholder="选择日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="还款金额" label-width="100px">
          <el-input v-model="repaymentForm.amount" autocomplete="off" /> 
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRepaymentDialog = false">取消</el-button>
        <el-button type="primary" @click="handleRepayment()">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog title="使用" v-model="showUseDialog">
      <el-form :model="useForm">
        <el-form-item label="账户号" label-width="100px">
          <el-input v-model="useForm.accountId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="使用日期" label-width="100px">
          <el-date-picker v-model="useForm.useDate" type="date" placeholder="选择日期"></el-date-picker>
        </el-form-item>
        <el-form-item label="使用金额" label-width="100px">
          <el-input v-model="useForm.amount" autocomplete="off" /> 
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUseDialog = false">取消</el-button>
        <el-button type="primary" @click="handleUse()">确定</el-button>
      </template>
    </el-dialog>
</template>

<script>
import { reactive, ref } from 'vue';
import request from '../utils/api';
import { ElMessage,ElMessageBox } from 'element-plus';
import { onMounted } from 'vue';


export default {
  setup() {
    const tableData = ref([]); // 信用账户数据
    const showAddDialog = ref(false); // 控制添加信用账户对话框的显示
    const showSearchDialog = ref(false); // 控制搜索信用账户对话框的显示
    const showRepaymentDialog = ref(false); // 控制还款对话框的显示
    const showUseDialog = ref(false); // 控制使用对话框的显示
    const currentPage = ref(1); // 当前页码
    const pageSize = ref(10); // 每页显示的条数
    const total = ref(0); // 总条数
    const addForm = reactive({
      branchCode: "",
      idNumber: "",
      password: "",
      balance: "", // 额度余额
      creditLimit: "", // 使用额度
      openingDate: "", // 开户日期
      interestRate: "", // 利率
    });
    const searchForm = reactive({
            accountId: "",
        });
    const repaymentForm = reactive({
            repaymentDate: "",
            amount: "",
            accountId: ""
        });
    const useForm = reactive({
            useDate: "",
            amount: "",
            accountId: ""
        });
    const loadData = async () => {
      // 加载信用账户数据的逻辑
      try {
        const response = await request.post('/api/creditaccounts/get/', searchForm, {
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

    onMounted (() => {
      loadData();
    });
    const handleEdit = (row) => {
      row.editing = true;
      // 编辑信用账户的逻辑
    };

    const handleSave = async (row) => {
      row.editing = false;
      try {
        const response = await request.put('/api/creditaccounts/edit/', row);
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
    const response = await request.delete('/api/creditaccounts/delete', {data: row});
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
        const response = await request.post('/api/creditaccounts/add/', addForm);
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

    const handleRepayment = async () => {
      // 还款的逻辑
      try{
        const response = await request.put('/api/creditaccounts/repay/', repaymentForm);
        if(response.data.code === 200){
          console.log('Repayment successful');
          showRepaymentDialog.value = false;
          loadData();
        }else{
          ElMessage.error(response.data.code + ":" + response.data.message);
          console.log('Repayment failed');
        }
      }catch(error){
        ElMessage.error(error);
        console.error(error);
      }
    };

    const handleUse = async () => {
      // 使用的逻辑
      try{
        const response = await request.put('/api/creditaccounts/consume/', useForm);
        if(response.data.code === 200){
          console.log('Use successful');
          showUseDialog.value = false;
          loadData();
        }else{
          ElMessage.error(response.data.code + ":" + response.data.message);
          console.log('Use failed');
        }
      }catch(error){
        ElMessage.error(error);
        console.error(error);
      }
    };

    return {
      tableData,
      showAddDialog,
      showSearchDialog,
      showRepaymentDialog,
      showUseDialog,
      currentPage,
      pageSize,
      total,
      addForm,
      searchForm,
      repaymentForm,
      useForm,
      loadData,
      onMounted,
      handleEdit,
      handleSave,
      handleDelete,
      handleSizeChange,
      handleCurrentChange,
      handleAdd,
      handleSearch,
      handleRepayment,
      handleUse
    };
  }
};
</script>