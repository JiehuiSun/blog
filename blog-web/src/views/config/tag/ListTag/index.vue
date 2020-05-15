
<template>
    <div class="management-tag">
    <div class="filter-container" style="margin-bottom: 20px">
        <el-button class="filter-item" type="success" icon="el-icon-plus" @click="handleAdd">添加标签</el-button>
    </div>

    <el-table
        key="tableKey"
        v-loading="listLoading"
        :data="list"
        border
        fit
        style="width: 100%"
        class="table"
        >

    <el-table-column label="序号" type="index" align="center" width="50" fixed></el-table-column>
      <el-table-column label="类型" align="center" width="100px" prop="typ_id"></el-table-column>
    <!-- 表单做判断 -->
      <!-- <el-table-column prop="store_name" label="门店" align="center">
        <template slot-scope="scope">
          <span v-if="scope.row.is_current">-</span>
          <span v-else>{{ scope.row.store_name }}</span>
        </template>
      </el-table-column> -->
      <el-table-column prop="name" label="标签名" align="center"></el-table-column>
      <!-- <el-table-column label="类型" align="center"></el-table-column> -->
      <el-table-column label="操作"  align="center">
        <template  slot-scope="scope">
          <el-link @click="handleDelete(scope.row.id)" type="danger" class="color-danger">删除</el-link>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      :total="total"
      :page.sync="listQuery.page_num"
      :limit.sync="listQuery.page_size"
      @pagination="getList"
    />
</div>
</template>

<script>
import { fetchStoreList } from '@/api/TOOLS'
import { getBlog } from '@/api/blog/index'
import { customConfirm } from '@/utils'
import Pagination from "@/components/Pagination";
export default {
  name: "BlogList",
  components: {
    Pagination
  },
  data() {
    return {
      listQuery: {
        // store_id: [],
        page_num: 1,
        page_size: 10
      },
      storeList: [],
      list: [],
      total: 0,
      listLoading: false,
      store_id: null,
      detailDialogVisible: false,
      detailInfo: {}
    };
  },
  mounted() {
    this.getList()
  },
  methods: {
    getList() {
      this.listLoading = true
      getBlog(this.listQuery).then(res => {
        this.listLoading = false
        this.list = res.data_list
        this.total = res.total_size
      })
    },
    handleDelete() {
      const that = this
      customConfirm(that,'确定要删除该标签?',() => {
        delBlog().then(data => {
          this.getList()
        })
      })
    },
    handleAdd() {
        this.$router.push({
            name: "BlogHouse"
        })
    }
  }
};
</script>
<style lang="scss" scoped>
  .management-tag {
    padding: 20px;
  }
</style>