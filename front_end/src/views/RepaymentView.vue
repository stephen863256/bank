<template>
    <el-card class="box-card">
      <template v-slot:header>
        <div class="clearfix">
          <span>还款情况</span>
          <el-button style="float: right; padding: 3px 0" type="primary" @click="showSearchDialog = true">搜索</el-button>
        </div>
      </template>
      <el-table :data="tableData" style="width: 100%">
        <el-table-column prop="repaymentId" label="还款标识号">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.repaymentId" />
                <span v-else>{{scope.row.repaymentId}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="repaymentAmount" label="还款金额">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.repaymentAmount" />
                <span v-else>{{scope.row.repaymentAmount}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="repaymentDate" label="还款日期">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.repaymentDate" />
                <span v-else>{{scope.row.repaymentDate}}</span>
            </template>
        </el-table-column>
        <el-table-column prop="loanId" label="贷款号">
            <template v-slot:default="scope">
                <el-input v-if="scope.row.editing" v-model="scope.row.loanId" />
                <span v-else>{{scope.row.loanId}}</span>
            </template>
        </el-table-column>
        <el-table-column label="操作">
          <template v-slot:default="scope">
            <el-button type="text" size="small" @click="handleEdit(scope.$index, scope.row)">编辑</el-button>
            <el-button type="text" size="small" @click="handleSave(scope.$index, scope.row)">保存</el-button>
            <el-button type="text" size="small" @click="handleDelete(scope.$index, scope.row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination @size-change="handleSizeChange" @current-change="handleCurrentChange" :current-page="currentPage" :page-sizes="[5, 10, 20]" :page-size="pageSize" layout="total, sizes, prev, pager, next, jumper" :total="total"></el-pagination>
    </el-card>
    <el-dialog title="搜索还款记录" v-model="showSearchDialog">
        <el-form :model="searchForm">
            <el-form-item label="贷款号" label-width="100px">
                <el-input v-model="searchForm.loanId" autocomplete="off" />
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
import request from '../utils/api';
import { ElMessage } from 'element-plus';
import { onMounted } from 'vue';

export default {
  setup() {
    const tableData = ref([]); 
    const showAddDialog = ref(false); 
    const showSearchDialog = ref(false); 
    const currentPage = ref(1); 
    const pageSize = ref(10);
    const total = ref(0); 
    const addForm = reactive({
        repaymentId: "",
        repaymentAmount: "",
        repaymentDate: "",
        loanId: ""
        });
    const searchForm = reactive({
            idNumber: "",
        });

      const loadData = async () => {
      try {
        const response = await request.post('/api/repayments/get/', searchForm, {
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
      loadData();
    });

    const handleSizeChange = (val) => {
      pageSize.value = val;
      // 更新每页显示的条数
    };

    const handleCurrentChange = (val) => {
      currentPage.value = val;
      // 更新当前页码
    };

    const handleSearch = () => {
      showSearchDialog.value = false
      loadData();
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
      handleSizeChange,
      handleCurrentChange,
      handleSearch
    };
  }
};
</script>