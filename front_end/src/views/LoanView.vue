<template>
    <el-card class="box-card">
      <template v-slot:header>
        <div class="clearfix">
          <span>贷款列表</span>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showAddDialog = true">增加</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showSearchDialog = true">搜索</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showRepaymentDialog = true">还款</el-button>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showChangeStatusDialog = true">更改状态</el-button>
        </div>
      </template>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="loanId" label="贷款号">
          <template v-slot:default="scope">
            <span>{{scope.row.loanId}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="本金">
          <template v-slot:default="scope">
            <span>{{scope.row.amount}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="interestRate" label="利率">
          <template v-slot:default="scope">
            <span>{{scope.row.interestRate}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="loanDate" label="发放时间">
          <template v-slot:default="scope">
            <span>{{scope.row.loanDate}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="repaymentAmount" label="已还款">
          <template v-slot:default="scope">
            <span>{{scope.row.repaymentAmount}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="interest" label="利息">
          <template v-slot:default="scope">
            <span>{{scope.row.interest}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="loanStatus" label="贷款状态">
          <template v-slot:default="scope">
            <span>{{scope.row.loanStatus}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="loanDays" label="借贷天数">
          <template v-slot:default="scope">
            <span>{{scope.row.loanDays}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="branchIssued" label="发放支行">
          <template v-slot:default="scope">
            <span>{{scope.row.branchIssued}}</span>
          </template>
        </el-table-column>
        <el-table-column prop="clientId" label="客户身份证号">
          <template v-slot:default="scope">
            <span>{{scope.row.clientId}}</span>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[5, 10, 20]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total"></el-pagination>
    </el-card>
  
    <!-- Add Loan Dialog -->
    <el-dialog title="添加贷款" v-model="showAddDialog">
    <el-form :model="addLoanForm">
        <el-form-item label="本金" label-width="120px">
        <el-input v-model="addLoanForm.amount" autocomplete="off" />
        </el-form-item>
        <el-form-item label="利率" label-width="120px">
        <el-input v-model="addLoanForm.interestRate" autocomplete="off" />
        </el-form-item>
        <el-form-item label="借贷天数" label-width="120px">
          <el-input v-model="addLoanForm.loanDays" autocomplete="off" />
        </el-form-item>
        <el-form-item label="发放支行" label-width="120px">
        <el-input v-model="addLoanForm.branchIssued" autocomplete="off" />
        </el-form-item>
        <el-form-item label="身份证号" label-width="120px">
        <el-input v-model="addLoanForm.idNumber" autocomplete="off" />
        </el-form-item>
    </el-form>
    <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="handleAdd()">确定</el-button>
    </template>
    </el-dialog>

    <el-dialog title="搜索客户" v-model="showSearchDialog">
      <el-form :model="searchForm">
        <el-form-item label="身份证号" label-width="100px">
          <el-input v-model="searchForm.idNumber" autocomplete="off" /> 
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSearchDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSearch()">确定</el-button>
      </template>
    </el-dialog>

    <!-- Change Loan Status Dialog -->
    <el-dialog title="更改贷款状态" v-model="showChangeStatusDialog">
    <el-form :model="changeStatusForm">
        <el-form-item label="贷款号" label-width="120px">
        <el-input v-model="changeStatusForm.loanId" autocomplete="off" />
        </el-form-item>
        <el-form-item label="新状态" label-width="120px">
        <el-select v-model="changeStatusForm.newStatus" placeholder="请选择新状态">
            <el-option label="已发放" value="ISSUED"></el-option>
        </el-select>
        </el-form-item>
        <el-form-item label="审批日期" label-width="120px">
        <el-date-picker v-model="changeStatusForm.loanDate" type="date" placeholder="选择日期"></el-date-picker>
        </el-form-item>
    </el-form>
    <template #footer>
        <el-button @click="showChangeStatusDialog = false">取消</el-button>
        <el-button type="primary" @click="handleChangeStatus()">确定</el-button>
    </template>
    </el-dialog>

    <el-dialog title="还款" v-model="showRepaymentDialog">
      <el-form :model="repaymentForm">
        <el-form-item label="贷款号" label-width="100px">
          <el-input v-model="repaymentForm.loanId" autocomplete="off" />
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
  </template>

<script>
import { reactive,ref } from 'vue';
import request from '../utils/api';
import { ElMessage } from 'element-plus';
import { onMounted } from 'vue';

export default {
    setup() {
      const tableData = ref([]); // 支行数据
      const showAddDialog = ref(false); 
      const showSearchDialog = ref(false); 
      const showChangeStatusDialog = ref(false); 
      const showRepaymentDialog = ref(false);
      const currentPage = ref(1); // 当前页码
      const pageSize = ref(10); // 每页显示的条数
      const total = ref(0); // 总条数
      const addLoanForm = reactive({
            amount: '',
            interestRate: '',
            loanDays: '',
            loanStatus: '',
            branchIssued: '',
            idNumber: '',
          });
      const searchForm = reactive({
              idNumber: "",
          });
      const changeStatusForm = reactive({
              loanId: "",
              newStatus: "",
              loanDate: "",
      });
      const repaymentForm = reactive({
              loanId: "",
              repaymentDate: "",
              amount: "",
          });
      const loadData = async () => {
      try {
        const response = await request.post('/api/loans/get/', searchForm, {
          params: {
            page: currentPage.value,
            size: pageSize.value, 
          },
        });
        if (response.data.code === 200) {
          tableData.value = response.data.data.data;
          total.value = response.data.data.count;
         // console.log(response.data.data.data);
         // console.log(response.data.data.count);
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
        const response = await request.post('/api/loans/add/', addLoanForm);
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
      for(let key in addLoanForm){
        addLoanForm[key] = "";
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
      
      const handleChangeStatus = async () => {
        try {
          const response = await request.post('/api/loans/updatestatus/', changeStatusForm);
          if (response.data.code === 200) {
            // 更改状态成功
            console.log('Change status successful');
            // 关闭更改状态对话框
            showChangeStatusDialog.value = false;
            // 重新加载数据
            loadData();
          } else {
            // 更改状态失败
            ElMessage.error(response.data.code + ":" + response.data.message);
            console.log('Change status failed');
          }
        } catch (error) {
          // 处理错误
          ElMessage.error(error);
          console.log('Error:', error);
        }
      };
      
      const handleRepayment = async () => {
      // 还款的逻辑
        try{
          const response = await request.put('/api/loans/repay/', repaymentForm);
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

      return {
        tableData,
        showAddDialog,
        showSearchDialog,
        showChangeStatusDialog,
        showRepaymentDialog,
        currentPage,
        pageSize,
        total,
        addLoanForm,
        searchForm,
        changeStatusForm,
        repaymentForm,
        loadData,
        onMounted,
        handleSizeChange,
        handleCurrentChange,
        handleAdd,
        handleSearch,
        handleChangeStatus,
        handleRepayment,
      };
    }
  };
  </script>