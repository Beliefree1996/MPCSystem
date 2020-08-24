<template>
  <div class="login-page">
    <vue-particles
      color="#ffffff"
      :particleOpacity="0.7"
      :particlesNumber="50"
      shapeType="circle"
      :particleSize="4"
      linesColor="#dedede"
      :linesWidth="1"
      :lineLinked="true"
      :lineOpacity="0.4"
      :linesDistance="150"
      :moveSpeed="2"
      :hoverEffect="true"
      hoverMode="grab"
      :clickEffect="true"
      clickMode="push"
    >
    </vue-particles>
    <div class="login-page-center">
      <div class="login-page-content">
        <div class="login-page-title">系统登录</div>
        <div :xs="24" :sm="24" :md="12" :lg="12" :xl="12" style="margin:5% 20%; padding-bottom: 16px">
          <el-form ref="FormDatas" :model="FormDatas" label-width="80px" :rules="rules">
            <el-form-item label="用户名" prop="username">
              <el-input type="text" v-model="FormDatas.username" autocomplete="off" placeholder="键入你的用户名"></el-input>
            </el-form-item>
            <el-form-item label="密码" prop="password">
              <el-input type="password" v-model="FormDatas.password" autocomplete="off" placeholder="键入你的密码"></el-input>
            </el-form-item>
            <el-form-item style="text-align:center">
              <el-button type="primary" @click="submitd('FormDatas')"><font size="4px">登录</font></el-button>
              &nbsp;&nbsp;没有帐号?
              <router-link to="/user/register" style="color: red">点我注册</router-link>
            </el-form-item>
          </el-form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Login',
    data() {
      return {
        FormDatas: {
          username: '',
          password: ''
        },
        rules: {
          username: [
            {required: true, message: '这是必填项!', trigger: 'blur'}
          ],
          password: [
            {required: true, message: '这是必填项!', trigger: 'blur'}
          ]
        }
      }
    },
    methods: {
      submitd: function (Dataset) {
        this.$refs[Dataset].validate((valid) => {
          if (valid) {
            // 成功
            this.$axios.post('/apis/user/login', {
              username: this.FormDatas.username,
              password: this.FormDatas.password,
            })
              .then(response => {
                if (response.data.status === 0) {
                  this.$router.push({path: "/"});
                  window.location.reload();
                } else {
                  this.$notify({
                    title: '登录失败',
                    message: response.data.message,
                    type: 'error'
                  })
                }

              })
          } else {
            return false;
          }
        })
      }
    }
  }
</script>

<style>
  .login-page {
    font-size: 16px;
    color: #fff;
    background: url(../../assets/sky.jpg) no-repeat;
    min-height: 100%;
  }

  .login-page-center {
    width: 70%;
    height: 50%;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
  }

  .login-page-title {
    font-size: 42px;
    padding-top: 10px;
    text-align: center;
    user-select: none;
  }

  .login-page-content {
    background-color: rgba(46, 46, 46, .61);
    border-radius: 10px;
    box-shadow: 0 0 20px 0 #f0f8ff;
  }

  .el-form-item__label {
    color: white;
    font-size: 16px;
  }

  @-webkit-keyframes pulsate-bck {
    0%, to {
      -webkit-transform: scale(1);
      transform: scale(1)
    }
    50% {
      -webkit-transform: scale(.9);
      transform: scale(.9)
    }
  }

  @keyframes pulsate-bck {
    0%, to {
      -webkit-transform: scale(1);
      transform: scale(1)
    }
    50% {
      -webkit-transform: scale(.9);
      transform: scale(.9)
    }
  }
</style>
