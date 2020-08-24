<template>
  <div class="register-page">
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
    <div class="register-page-center">
      <div class="register-page-content">
        <div class="register-page-title">注册账号</div>
<!--        <div id="Register" style="text-align:center">-->
<!--    <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12" style="margin: 8% 24%">-->
          <div :xs="24" :sm="24" :md="12" :lg="12" :xl="12" style="margin:5% 20%; padding-bottom: 16px">
      <el-form :model="FormData" status-icon ref="FormData" :rules="rules">
        <el-form-item label="用户名" prop="username">
          <el-input type="text" v-model="FormData.username" placeholder="请输入用户名"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" v-model="FormData.password" placeholder="请输入密码"></el-input>
        </el-form-item>
        <el-form-item label="再次输入密码" prop="repassword">
          <el-input type="password" v-model="FormData.repassword" placeholder="请再次输入密码"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="FormData.email" placeholder="请输入邮箱"></el-input>
        </el-form-item>
        <el-form-item style="text-align:center">
          <el-button type="primary" @click="submitd('FormData')"><font size="4px">提交</font></el-button>
          <el-button @click="resetForm('FormData')"><font size="4px">重置</font></el-button>
        </el-form-item>
      </el-form>
<!--          </div>-->
<!--    </el-col>-->
  </div>
      </div>
    </div>
  </div>
</template>

<script>
  export default {
    name: 'Register',
    data() {
      // 检测第二次输入的密码
      var checkPassword = (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请再次输入密码'))
        } else if (value !== this.FormData.password) {
          callback(new Error('两次输入的密码不一致.'))
        } else {
          callback()
        }
      }
      // 检测用户名是否已经被注册
      var dulaUsername = (rule, value, callback) => {
        // 验证用户名是否存在.  一会再写
        if (value.length < 3) {
          callback(new Error('你的用户名太短了！'))
        } else if (value.length > 18) {
          callback(new Error('你的用户名太长了！'))
        } else {
          this.$axios.post('/apis/user/register?select=1', {
            select_username: value
          })
            .then(response => {
              if (response.data.is_indb === 1) {
                callback(new Error('该用户名已经被注册'))
              } else {
                callback();
              }
            })
        }
      }

      // 检测密码的长度
      var checkLen = (rule, value, callback) => {
        if (value.length < 6) {
          callback(new Error('密码长度不能小于6位'))
        } else if (value.length > 18) {
          callback(new Error('密码长度不能超过18位'))
        } else {
          callback()
        }
      }

      return {
        FormData: {
          username: "",
          password: "",
          repassword: "",
          email: ""
        },
        rules: {
          username: [{required: true, message: '这是必填项', trigger: 'blur'}, {validator: dulaUsername, trigger: 'blur'}],
          password: [{required: true, message: "这是必填项", trigger: 'blur'}, {validator: checkLen, trigger: 'blur'}],
          repassword: [{required: true, message: '这是必填项', trigger: 'blur'}, {validator: checkPassword, trigger: 'blur'}],
          email: [{required: true, message: "请输入邮箱地址", trigger: 'blur'}, {type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change']}]
        }
      }
    },
    methods: {
      submitd: function (formdata) {
        this.$refs[formdata].validate((valid) => {
          if (valid) {
            // 成功.
            this.$axios.post('/apis/user/register', {
              username: this.FormData.username,
              password: this.FormData.password,
              email: this.FormData.email
            })
              .then(response => {
                if (response.data.status === 0) {
                  this.$router.push({path: '/'})
                  window.location.reload()
                } else {
                  return false
                }
              })

          } else {
            return false;
          }
        });
      },
      resetForm: function (formdata) {
        this.$refs[formdata].resetFields()
      }
    }
  }
</script>

<style scoped>
  .register-page {
    font-size: 16px;
    color: #fff;
    background: url(../../assets/background.jpg) no-repeat;
    min-height: 100%;
  }

  .register-page-center {
    width: 70%;
    height: 70%;
    position: absolute;
    left: 0;
    right: 0;
    top: 0;
    bottom: 0;
    margin: auto;
  }

  .register-page-title {
    font-size: 40px;
    padding-top: 10px;
    text-align: center;
    user-select: none;
  }

  .register-page-content {
    background-color: rgba(46, 46, 46, .61);
    border-radius: 10px;
    box-shadow: 0 0 20px 0 #f0f8ff;
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
