<template>
  <div class="SocialSecurity">
    <div class="block">
    </div>
    <div class="wrap-banner">
      <el-row :gutter="10">
        <el-col :xs="24" :xl="12" :lg="12" :sm="24" :md="12">
          <el-card style="min-height: 100%; max-height: 800px; ">
            <div slot="header">
              <span>近半年公积金及社保额度变化</span>
            </div>
            <panel-group @handleSetLineChartData="handleSetLineChartData"/>

            <el-row v-loading="listLoading" style="background:#fff;padding:16px 16px 0;margin-bottom:32px;">
              <line-chart :chart-data="lineChartData"/>
            </el-row>
          </el-card>
        </el-col>

        <el-col :xl="12" :lg="12" :sm="24" :md="12" class="hidden-sm-and-down">
          <Status></Status>
          <el-card style="min-height: 200px; max-height: 300px; ">
            <div slot="header">
              <span>查询个人公积金月缴额及社保缴费基数</span>
            </div>
            <el-row>
              <div class="block">
                <span class="demonstration">请选择您要查询的月份</span>
                <el-date-picker
                  v-model="choose_month"
                  type="month"
                  placeholder="选择年月"
                  format="yyyy 年 MM 月"
                  value-format="yyyyMM">>
                </el-date-picker>
                <el-button type="primary" size="medium" @click="inquiry()">确定</el-button>
                <el-row>
                  <el-card style="margin-top:20px; margin-bottom: 20px">
                    <span v-show="!show_wage"><i class="el-icon-warning-outline"></i> 未查询到相关数据</span>
                    <span v-show="show_wage">您该月公积金月缴额为 {{this.wageItem}}，</span>
                    <span v-show="show_wage">应缴社保缴费基数为 {{this.taxItem}}</span>
                  </el-card>
                </el-row>
              </div>
            </el-row>
          </el-card>
        </el-col>
      </el-row>
    </div>

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

    <el-dialog
      title="提示"
      :visible.sync="dialogVisible"
      close-on-click-modal="false"
      show-close="false"
      width="30%">
      <span>您还未认证</span>
      <span slot="footer" class="dialog-footer">
    <el-button @click="goHome">取 消</el-button>
    <el-button type="primary" @click="goCertification">前往认证</el-button>
  </span>
    </el-dialog>

  </div>
</template>

<script>
  import Status from '@/components/Status'
  import LineChart from "./annex/LineChart"

  const lineChartData = {
    socialSecurityData: {
      xAxisData: [],
      wageData: [],
      taxData: []
    },
  }

  export default {
    name: 'SocialSecurity',
    components: {
      Status,
      LineChart
    },
    data() {
      return {
        listLoading: true,
        // 是否登录
        isLogin: false,
        // 是否认证
        dialogVisible: false,
        show_wage: false,
        userId: '',
        dataArr: [],
        wageArr: [],
        taxArr: [],
        wageItem: '',
        taxItem: '',
        lineChartData: lineChartData.socialSecurityData,
        choose_month: '',
      }
    },
    methods: {
      goHome() {
        this.$router.push({path: '/'})
      },
      goCertification() {
        this.$router.push({path: '/user/root'})
      },
      getData() {
        this.$axios.get('apis/get_info?wage=true&user_id=' + this.userId)
          .then(response => {
            if (response.data.status_code === 0) {
              this.listLoading = false
              this.dataArr = response.data.data
              let monthArr = new Array(6)
              let wageArr = new Array(6)
              let taxArr = new Array(6)
              for (let i = 0; i < this.dataArr.length; i++) {
                let Arr = this.dataArr[i]['date'].toString()
                monthArr[i] = Arr.substr(0, 4) + "年" + Arr.substr(4, 2) + "月"
                wageArr[i] = this.dataArr[i]['pf']
                taxArr[i] = this.dataArr[i]['ss']
              }
              lineChartData.socialSecurityData.xAxisData = [monthArr[5], monthArr[4], monthArr[3], monthArr[2], monthArr[1], monthArr[0]]
              lineChartData.socialSecurityData.wageData = [wageArr[5], wageArr[4], wageArr[3], wageArr[2], wageArr[1], wageArr[0]]
              lineChartData.socialSecurityData.taxData = [taxArr[5], taxArr[4], taxArr[3], taxArr[2], taxArr[1], taxArr[0]]
            } else {
              this.$message.error("未查询到您的信息！")
            }
          })
        // setTimeout(() => {
        //   this.listLoading = false
        // }, 20 * 1000)
      },
      // 查询
      inquiry: function () {
        this.wageItem = ''
        this.show_wage = false
        if (this.choose_month === '') {
          this.$message.error("请选择您要查询的月份！")
        } else {
          this.$axios.get('apis/get_info?wage=true&user_id=' + this.userId + '&date=' + this.choose_month)
            .then(response => {
              if (response.data.status_code === 0) {
                if (response.data.data !== null) {
                  this.wageItem = response.data.data[0]['pf']
                  this.taxItem = response.data.data[0]["ss"]
                  this.show_wage = true
                } else {
                  this.$message.error("未查询到该月您的社保信息！")
                }
              } else {
                this.$message.error("未查询到该月您的社保信息！")
              }
            })
        }
      },
      play: function (url, name) {
        console.log(name, url)
        this.audio = url
        this.name = name
        this.playm = true
      },
      handleSetLineChartData(type) {
        this.lineChartData = lineChartData[type]
      }
    },
    created() {
      // this.$http.get('apis/get_info?mp3=yep')
      //   .then(response => {
      //     this.mp3 = response.data
      //   }, error => {
      //     console.log('mp3 error')
      //   })
      this.$axios.get('apis/user/getstatus?aa=60&kk=6')
        .then(response => {
          if (response.data.status === 1) {
            this.$router.push({path: '/user/login'})
          } else {
            if (response.data.status === 2) {
              this.dialogVisible = true
            }
            this.isLogin = true
            this.userId = response.data.id
            this.getData()
          }
        })
    },
  }
</script>

<style scoped>
  .grid_content {
    background: #0b2e13;
    height: auto;
    width: auto;
  }

  .wrap-banner {
    position: absolute;
    left: 0;
    right: 0;
  }
</style>
