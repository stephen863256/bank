<template>
    <el-card class="box-card">
      <template v-slot:header>
        <div class="clearfix">
          <span>储蓄账户交易情况</span>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showSearchDialog = true">搜索</el-button>
        </div>
      </template>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="transactionId" label="交易号">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.transactionId" />
                <span v-else>{{scope.row.transactionId}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="transactionType" label="交易类型">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.transactionType" />
                <span v-else>{{scope.row.transactionType}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.amount" />
                <span v-else>{{scope.row.amount}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="transactionDate" label="交易日期">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.transactionDate" />
                <span v-else>{{scope.row.transactionDate}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="savingsAccount" label="账户号">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.savingsAccount" />
                <span v-else>{{scope.row.savingsAccount}}</span>
            </template>
        </el-table-column>
      </el-table>
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[5, 10, 20]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total"></el-pagination>
    </el-card>
    <el-dialog title="搜索还款记录" v-model="showSearchDialog">
        <el-form :model="searchForm">
            <el-form-item label="账户号" label-width="100px">
                <el-input v-model="searchForm.savingsAccount" autocomplete="off" />
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="showSearchDialog = false">取消</el-button>
            <el-button type="primary" @click="handleSearch()">搜索</el-button>
        </template>
    </el-dialog>
</template>

<script>
import { reactive,ref } from 'vue';
import  request  from '../utils/api.ts';
import { ElMessage } from 'element-plus';
import { onMounted } from 'vue';
export default {
  setup() {
    const tableData = ref([]); // 用户数据
    const showSearchDialog = ref(false); // 控制搜索用户对话框的显示
    const currentPage = ref(1); // 当前页码
    const pageSize = ref(10); // 每页显示的条数
    const total = ref(0); // 总条数
    const searchForm = reactive({
            savingsAccount: "",
        });
    const loadData = async () => {
      try {
        const response = await request.post('/api/transactions/get/', searchForm, {
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
      showSearchDialog,
      currentPage,
      pageSize,
      total,
      searchForm,
      loadData,
      onMounted,
      handleSizeChange,
      handleCurrentChange,
      handleSearch
    };
  }
};
  </script>