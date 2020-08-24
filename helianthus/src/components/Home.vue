<template>
  <div class="Home">
    <div style="height: 100%; width: 100%">
      <span class="demonstration"></span>
      <el-carousel height="386px">
        <el-carousel-item v-for="item in news" :key="item.id">
          <!--        <h3 class="small">{{ item.tittle }}</h3>-->
<!--          <div style="height: 100%; width: auto">-->
            <img :src="item.img_src">
<!--          </div>-->
        </el-carousel-item>
      </el-carousel>
      <br>
      <br>
    </div>
    <el-row :gutter="10">
      <el-col :xs="24" :xl="12" :lg="12" :sm="24" :md="12">
        <el-card style="min-height: 150px; max-height: 238px">
          <div slot="header">
            <span>最新公告</span>
            <div style="cursor:pointer; display: inline-block; float: right">
              <i class="el-icon-more" onclick="window.location.href='/bloglist'"></i>
            </div>
          </div>
          <div style="overflow: auto; height: 180px; width: 100%;">
            <li style="font-size: 90%; margin-top: 5px" v-for="dat in blogList">
              <span>{{dat.title}}</span>
              <span style="float: right">{{dat.time}}</span>
            </li>
          </div>

        </el-card>
      </el-col>

      <el-col :xl="12" :lg="12" :sm="24" :md="12" class="hidden-sm-and-down">
        <div v-if="isStaff === false">
        <el-card style="min-height: 200px; max-height: 300px; ">
          <div slot="header">
            <span>当前授权额度</span>
          </div>
          <el-row>
            <el-card style="margin-top:20px; margin-bottom: 20px">
              <el-tag
                v-loading="listLoading"
                style="margin-left:45%"
                :key="quota"
                type="success"
                effect="dark">
                {{ quota }}元
              </el-tag>
            </el-card>
          </el-row>
        </el-card>
          </div>
        <div v-else>
          <Status></Status>
        </div>
      </el-col>
    </el-row>

  </div>
</template>

<script>
  import Status from '@/components/Status'

  export default {
    name: 'Home',
    components: {
      Status
    },
    data() {
      return {
        userId: 1,
        isStaff: true,
        listLoading: true,
        playm: false,
        blogList: null,
        mp3: '',
        audio: '',
        name: '',
        quota: '78000',
        news: [
          {id: 1, tittle: '新闻1', img_src: '/apis/static/image/1.jpg'},
          {id: 2, tittle: '新闻2', img_src: '/apis/static/image/2.jpg'},
          {id: 3, tittle: '新闻3', img_src: '/apis/static/image/3.jpg'}
        ],
      }
    },
    methods: {
      play: function (url, name) {
        console.log(name, url)
        this.audio = url
        this.name = name
        this.playm = true
      },
      getUserInfo: function() {
        this.$axios.get('apis/user/getstatus?aa=60&kk=6')
        .then(response => {
          if (response.data.status === 0){
            this.userId = response.data.id
            this.isStaff = response.data.is_staff
            this.getQuota()
          }
          else if (response.data.status === 1) {
            this.$router.push({path: '/user/login'})
          }
        })
      },
      getQuota: function () {
        // this.$axios.get('apis/getQuota?userId' + this.userId)
        //   .then(response => {
        //     if (response.data.status_code === 0) {
        //       this.listLoading = false
        //       this.quota = response.data.data
        //     } else if(response.data.status_code === 1){
        //       this.quota = "您未认证！"
        //     }
        //     else {
        //       this.$message.error("未查询到您的额度！")
        //     }
        //   })
        this.$axios.get('apis/getQuota?userId=' + this.userId)
          .then(response => {
            if (response.data.status_code === 0) {
              this.listLoading = false
              this.quota = response.data.data
            } else if(response.data.status_code === 1){
              this.quota = "您未认证！"
            }
            else {
              this.$message.error("未查询到您的额度！")
            }
          })
      }
    },
    created() {
      // this.$http.get('apis/get_info?mp3=yep')
      //   .then(response => {
      //     this.mp3 = response.data
      //   }, error => {
      //     console.log('mp3 error')
      //   })
      this.$http.get("apis/get_info?blog_list=true&aa=60&kk=6")
        // this.$http.get("apis/get_info?wage=true&aa=60&kk=6")
        .then(response => {
          this.blogList = response.data.data
          this.loading = false
        }, error => {
          console.log("获取bloglist出错了.");
        });
      fetch("apis/get_info?mp3=yep", {
        method: "get",
      })
        .then(response => {
          return response.json()
        })
        .then(data => {
          this.mp3 = data
        })
      // this.getQuota()
      this.getUserInfo()

    }
  }
</script>

<style scoped>
  .grid_content {
    background: #0b2e13;
    height: auto;
    width: auto;
  }
</style>
