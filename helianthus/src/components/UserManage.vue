<template>
  <div class="UserManage">
    <div class="wrap-banner">
    <el-row>
      <h3></h3>
      <el-input v-model="input" placeholder="请输入用户名" style="width: 160px"></el-input>
      <el-button type="primary" round style="margin-left: 20px" @click="inquiry()">搜索</el-button>
    </el-row>
    <el-card style="min-height: 100%; max-height: 800px; margin-top: 20px">
      <el-table
        :data="tableData"
        style="width: 100%">
        <el-table-column
          prop="username"
          label="用户名"
          width="100">
        </el-table-column>
        <el-table-column
          prop="email"
          label="邮箱"
          width="240">
        </el-table-column>
        <el-table-column
          prop="IC_num"
          label="身份证号"
        >
        </el-table-column>
        <el-table-column
          prop="date_joined"
          label="注册时间"
          width="250">
        </el-table-column>
        <el-table-column
          prop="last_login"
          label="最近登陆"
          width="250">
        </el-table-column>
        <el-table-column align="center" min-width="80" label="锁定">
          <template slot-scope="scope">
            <el-switch v-model="scope.row.is_active === false" active-color="#13ce66"
                       @change="changeActive(scope.row)">
            </el-switch>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!--页码条-->
    </div>
    <el-col :span="24" class="toolbar" style="position: absolute; right: 100px; bottom: 60px">
      <el-pagination style="float:right;"
                     background
                     layout="prev, pager, next"
                     @current-change="handleCurrentChange"
                     :page-size="pageSize"
                     :total="totalPage">
      </el-pagination>
    </el-col>
        <vue-particles
        color="#409EFF"
        :particleOpacity="0.7"
        :particlesNumber="80"
        shapeType="circle"
        :particleSize="4"
        linesColor="#409EFF"
        :linesWidth="1"
        :lineLinked="true"
        :lineOpacity="0.4"
        :linesDistance="150"
        :moveSpeed="3"
        :hoverEffect="true"
        hoverMode="grab"
        :clickEffect="true"
        clickMode="push"
      ></vue-particles>
  </div>
</template>

<style>
  .el-table .warning-row {
    background: oldlace;
  }

  .el-table .success-row {
    background: #f0f9eb;
  }
</style>

<script>
  export default {
    name: 'UserManage',
    data() {
      return {
        tableData: [],
        input: '',
        page: 1,
        totalPage: 100,
        pageSize: 5,
      }
    },
    created() {
      this.getData()
    },
    methods: {
      inquiry() {
        this.$axios.get('apis/get_info?user_detail=true&username=' + this.input)
          .then(response => {
            if (response.data.status_code === 0) {
              this.tableData = response.data.data
              for (let i = 0; i < this.tableData.length; i++) {
                if (!this.tableData[i]['IC_num']) {
                  this.tableData[i]['IC_num'] = "未绑定"
                }
              }
              console.log(this.tableData)
            } else {
              this.$message.error("网络错误！")
            }
          })
      },
      getData() {
        this.$axios.get('apis/get_info?user_detail=true&page=' + this.page)
          .then(response => {
            if (response.data.status_code === 0) {
              this.tableData = response.data.data
              this.totalPage = response.data.total
              for (let i = 0; i < this.tableData.length; i++) {
                if (!this.tableData[i]['IC_num']) {
                  this.tableData[i]['IC_num'] = "未绑定"
                }
              }
              console.log(this.tableData)
            } else {
              this.$message.error("网络错误！")
            }
          })
      },
      changeActive(data) {
        this.$axios.get('apis/change_data?change_active=true&user_id=' + data.id)
          .then(response => {
            if (response.data.status_code === 0) {
              this.getData()
              if(data.is_active === false){
                this.$message.success("解锁成功！")
              }else{
                this.$message.success("锁定成功！")
              }
            } else {
              this.$message.error("网络错误！")
            }
          })
      },
      // 点击页码
      handleCurrentChange(val) {
        this.page = val;
        this.getData();
      },
      // tableRowClassName({row, IC_num}) {
      //   if (IC_num === "未绑定") {
      //     return 'warning-row';
      //   } else if (IC_num === 3) {
      //     return 'success-row';
      //   }
      //   return '';
      // }
    },
  }
</script>

<style scoped>
    .wrap-banner {
    position: absolute;
      left: 30px;
      right: 30px;
    /*left: 50%;*/
    /*margin-left: -520px;*/
  }
</style>
