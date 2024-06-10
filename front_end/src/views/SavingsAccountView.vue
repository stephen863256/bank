<template>
    <el-card class="box-card">
      <template v-slot:header>
        <div class="clearfix">
          <span>储蓄账户列表</span>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showAddDialog = true">增加</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showSearchDialog = true">搜索</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showDepositDialog = true">存款</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showWithdrawDialog = true">取款</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showUseDialog = true">转账</el-button>
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
          <el-table-column prop="balance" label="余额">
            <template v-slot:default="scope">
              <span>{{scope.row.balance}}</span>
            </template>
          </el-table-column>
          <el-table-column prop="interestRate" label="利率">
            <template v-slot:default="scope">
              <span>{{scope.row.interestRate}}</span>
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
    <el-dialog title="添加储蓄账户" v-model="showAddDialog">
    <el-form :model="addForm">
      <el-form-item label="支行代码" label-width="100px">
        <el-input v-model="addForm.branchCode" autocomplete="off" />
      </el-form-item>
      <el-form-item label="客户身份证号" label-width="100px">
        <el-input v-model="addForm.idNumber" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" label-width="100px">
        <el-input v-model="addForm.password" autocomplete="off" type="password" />
        </el-form-item>
      <el-form-item label="余额" label-width="100px">
        <el-input v-model="addForm.balance" autocomplete="off" />
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

    <el-dialog title="搜索储蓄账户" v-model="showSearchDialog">
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
    <!-- Deposit Dialog -->
    <el-dialog title="存款" v-model="showDepositDialog">
      <el-form :model="depositForm">
        <el-form-item label="账户号" label-width="100px">
          <el-input v-model="depositForm.accountId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="金额" label-width="100px">
          <el-input v-model="depositForm.amount" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showDepositDialog = false">取消</el-button>
        <el-button type="primary" @click="handleDeposit()">确定</el-button>
      </template>
    </el-dialog>

    <!-- Withdraw Dialog -->
    <el-dialog title="取款" v-model="showWithdrawDialog">
      <el-form :model="withdrawForm">
        <el-form-item label="账户号" label-width="100px">
          <el-input v-model="withdrawForm.accountId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="金额" label-width="100px">
          <el-input v-model="withdrawForm.amount" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showWithdrawDialog = false">取消</el-button>
        <el-button type="primary" @click="handleWithdraw()">确定</el-button>
      </template>
    </el-dialog>

    <!-- Use Dialog -->
    <el-dialog title="转账" v-model="showUseDialog">
      <el-form :model="transferForm">
        <el-form-item label="账户号" label-width="100px">
          <el-input v-model="transferForm.accountId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="目标账户号" label-width='100px'>
          <el-input v-model="transferForm.targetAccountId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="金额" label-width="100px">
          <el-input v-model="transferForm.amount" autocomplete="off" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showUseDialog = false">取消</el-button>
        <el-button type="primary" @click="handleTransfer()">确定</el-button>
      </template>
    </el-dialog>
</template>

<script>
//import { id } from 'element-plus/es/locale';
import { reactive, ref } from 'vue';
import request from '../utils/api';
import { ElMessage,ElMessageBox } from 'element-plus';
import { onMounted } from 'vue';
//import { ta } from 'element-plus/es/locale';
//import { da, tr } from 'element-plus/es/locale';

export default {
  setup() {
    const tableData = ref([]); // 信用账户数据
    const showAddDialog = ref(false); // 控制添加信用账户对话框的显示
    const showSearchDialog = ref(false); // 控制搜索信用账户对话框的显示
    const showDepositDialog = ref(false); // 控制存款对话框的显示
    const showWithdrawDialog = ref(false); // 控制取款对话框的显示
    const showUseDialog = ref(false); // 控制使用对话框的显示
    const currentPage = ref(1); // 当前页码
    const pageSize = ref(10); // 每页显示的条数
    const total = ref(0); // 总条数
    const addForm = reactive({
        branchCode: "",
        idNumber: "",
        accountId: "",
        remaining: "", 
        password: "",
        openingDate: "",
        interestRate: "" 
    });

    const searchForm = reactive({
            accountId: "",
        });
    const depositForm = reactive({
            accountId: "",
            amount: "",
            transactionDate: ""
        });
    const withdrawForm = reactive({
            accountId: "",
            amount: "",
            transactionDate: ""
        });
    const transferForm = reactive({
            accountId: "",
            amount: "",
            transactionDate: "" ,
            targetAccountId: ""
        });
    const loadData = async () => {
      try {
        const response = await request.post('/api/savingsaccounts/get/', searchForm, {
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
      row.editing = true;
      // 编辑客户的逻辑
    };

    const handleSave = async (row) => {
      row.editing = false;
      try {
        const response = await request.put('/api/savingsaccounts/edit/', row);
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
    const response = await request.delete('/api/savingsaccounts/delete', {data: row});
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
        const response = await request.post('/api/savingsaccounts/add/', addForm);
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
    const handleDeposit = async () => {
      // 存款的逻辑
      try {
        const response = await request.put('/api/savingsaccounts/deposit/', depositForm);
        if (response.data.code === 200) {
          // 存款成功
          console.log('Deposit successful');
          // 关闭存款对话框
          showDepositDialog.value = false;
          // 重新加载数据
          loadData();
        } else {
          // 存款失败
          ElMessage.error(response.data.code + ":" + response.data.message);
          console.log('Deposit failed');
        }
      } catch (error) {
        // 处理错误
        ElMessage.error(error);
        console.log('Error:', error);
      }
    };

    const handleWithdraw = async () => {
      // 取款的逻辑
      try {
        const response = await request.put('/api/savingsaccounts/withdraw/', withdrawForm);
        if (response.data.code === 200) {
          // 取款成功
          console.log('Withdraw successful');
          // 关闭取款对话框
          showWithdrawDialog.value = false;
          // 重新加载数据
          loadData();
        } else {
          // 取款失败
          ElMessage.error(response.data.code + ":" + response.data.message);
          console.log('Withdraw failed');
        }
      } catch (error) {
        // 处理错误
        ElMessage.error(error);
        console.log('Error:', error);
      }
    };

    const handleTransfer = async () => {
      // 使用的逻辑
      try {
        const response = await request.put('/api/savingsaccounts/transfer/', transferForm);
        if (response.data.code === 200) {
          // 使用成功
          console.log('Transfer successful');
          // 关闭使用对话框
          showUseDialog.value = false;
          // 重新加载数据
          loadData();
        } else {
          // 使用失败
          ElMessage.error(response.data.code + ":" + response.data.message);
          console.log('Transfer failed');
        }
      } catch (error) {
        // 处理错误
        ElMessage.error(error);
        console.log('Error:', error);
      }
    };

    return {
      tableData,
      showAddDialog,
      showSearchDialog,
      showDepositDialog,
      showWithdrawDialog,
      showUseDialog,
      currentPage,
      pageSize,
      total,
      addForm,
      searchForm,
      depositForm,
      withdrawForm,
      transferForm,
      loadData,
      onMounted,
      handleEdit,
      handleSave,
      handleDelete,
      handleSizeChange,
      handleCurrentChange,
      handleAdd,
      handleSearch,
      handleDeposit,
      handleWithdraw,
      handleTransfer
    };
  }
};
</script>