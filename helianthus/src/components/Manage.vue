<template>
  <div class="AddBlog" v-show="isLogin" v-loading="loading">

    <div style="height: 480px; width: 100%; background: white" v-show="loading" fade>
    </div>

    <el-form v-if="!issubmitd" :rules="rules" ref="blog" :model="blog" v-show="!loading" fade>
      <el-row :gutter="10">
        <el-col :span="12">
          <el-card style="min-height: 200px; max-height: 300px; ">
            <div slot="header">
              <span>更新密钥</span>
            </div>
            <el-row>
              <el-card style="margin-top:20px; margin-bottom: 20px">
                <el-row>
                  <el-button type="primary" @click="renewKey">点击更新</el-button>
                </el-row>
                <el-row>
                  <font size="2" color="red">建议定期更新！</font>
                </el-row>
              </el-card>
            </el-row>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card style="min-height: 200px; max-height: 300px; ">
            <div slot="header">
              <span> 联邦学习</span>
            </div>
            <el-row>
              <el-card style="margin-top:20px; margin-bottom: 20px">
                <el-row>
                  <el-col :span="18">
                    <el-upload
                      class="upload-demo"
                      action="https://jsonplaceholder.typicode.com/posts/"
                      :on-preview="handlePreview"
                      :on-remove="handleRemove"
                      :before-remove="beforeRemove"
                      multiple
                      :limit="3"
                      :on-exceed="handleExceed">
                      <el-button type="primary" icon="el-icon-upload" @click="trainUpload">上传数据</el-button>
                      <div slot="tip" class="el-upload__tip">只能上传Excel/CSV文件，且不超过2M</div>
                    </el-upload>
                  </el-col>
                  <el-button type="success" @click="startTrain" :disabled=isTrain_disable>开始训练</el-button>
                </el-row>
              </el-card>
            </el-row>
          </el-card>
        </el-col>
      </el-row>

      <el-card style="min-height: 200px; min-height: 400px; margin-top: 10px">
        <div slot="header">
          <span>更换风控模型</span>
        </div>
        <el-row>
          <el-card style="margin-top:20px; margin-bottom: 20px">
            <el-form-item label="额度计算公式" prop="title" required>
              <el-select v-model="blog.title" placeholder="请选择" style="width: 680px">
                <el-option label="2*ss^3 + 10*pf + 10000" value=1></el-option>
                <el-option label="20*ss + 5*pf + 3000" value=2></el-option>
                <el-option label="max(min(max(ss * 0.8，pf * 15) * 10，150000)，50000)" value=3></el-option>
              </el-select>
              <el-button type="text" @click="dialogFormVisible = true"><font size="2" color="blue">点击定制模型</font>
              </el-button>
            </el-form-item>

            <!--            训练结果弹窗-->
            <el-dialog title="联邦学习训练结果" :visible.sync="dialogResultVisible">
              <div v-loading="result_loading" element-loading-background="white">
                <img src="../assets/result.png" style="width: 70%; height: 60%">
                <div style="margin-right: 10px">
                  L = 1.02824158
w1 = -6.40531007
w2 = 634.590094
w3 = 5.69205746
x01 = 0.481440154
x02 = 0.0126577103
x03 = 0.377919248
b = 0.0550714959
                </div>
              </div>
              <span slot="footer" class="dialog-footer">
    <el-button type="primary" @click="dialogResultVisible = false">确 定</el-button>
  </span>
            </el-dialog>

            <!--            自定义公式-->
            <el-dialog title="自定义风控模型函数" :visible.sync="dialogFormVisible">
              <el-tabs type="border-card" stretch=true>
                <el-tab-pane label="单次函数">
                  <el-form :model="simpleFormula">
                    <h3>ss为个人社保缴费基数，pf为个人公积金月缴额</h3>
                    <br>
                    <el-form-item label="风控模型函数">
                      <el-input v-model="simpleFormula.a1" size="mini" placeholder="系数" style="width: 56px"></el-input>
                      ss +
                      <el-input v-model="simpleFormula.a2" size="mini" placeholder="系数" style="width: 56px"></el-input>
                      pf +
                      <el-input v-model="simpleFormula.c" size="mini" placeholder="常数" style="width: 56px"></el-input>
                    </el-form-item>
                    <el-form-item label="分母">
                      <el-input v-model="LDivisor" size="mini" placeholder="分母" style="width: 56px"></el-input>
                    </el-form-item>
                  </el-form>
                  <br>
                  <div class="dialog-footer" style="float:right">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="warning" @click="Mclear">清 空</el-button>
                    <el-button type="primary" @click="simpleSubmit">提 交</el-button>
                  </div>
                </el-tab-pane>
                <el-tab-pane label="多次函数">
                  <el-form :model="formula">
                    <h3>当前风de控模型函数：{{ModelFunction}}</h3>
                    <br>
                    <el-form-item label="多项式项">
                      <el-input v-model="formula.a" size="mini" placeholder="系数" style="width: 56px"></el-input>
                      ss^
                      <el-input v-model="formula.n1" size="mini" placeholder="次数" style="width: 56px"></el-input>
                      *pf^
                      <el-input v-model="formula.n2" size="mini" placeholder="次数" style="width: 56px"></el-input>
                      <el-button size="mini" type="success" round style="margin-left: 10px" @click="additem">添加
                      </el-button>
                    </el-form-item>
                    <el-form-item label="常数项">
                      <el-input v-model="lastC" size="mini" placeholder="常数" style="width: 66px"></el-input>
                      <el-button size="mini" type="success" round style="margin-left: 10px" @click="addC">确认</el-button>
                    </el-form-item>
                    <el-form-item label="分母">
                      <el-input v-model="MDivisor" size="mini" placeholder="分母" style="width: 66px"></el-input>
                      <el-button size="mini" type="success" round style="margin-left: 10px" @click="addMDivisor">确认
                      </el-button>
                    </el-form-item>
                  </el-form>
                  <br>
                  <div class="dialog-footer" style="float:right">
                    <el-button @click="dialogFormVisible = false">取 消</el-button>
                    <el-button type="warning" @click="Mclear">清 空</el-button>
                    <el-button type="primary" @click="repeatedlySubmit">提 交</el-button>
                  </div>
                </el-tab-pane>
              </el-tabs>
            </el-dialog>

            <div class="form-group">
              <!--        row分栏-->
              <el-row>
                <el-col :span="8">
                  <el-form-item label="数据加密算法" required>
                    <el-select v-model="blog.cateory_normal" placeholder="请选择">
                      <el-option label="Paillier" value="1"></el-option>
                      <el-option label="BLP" value="2"></el-option>
                      <el-option label="BLP_other" value="3"></el-option>
                      <el-option label="BFV" value="4"></el-option>
                      <el-option label="CKKS" value="5"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="同态运算算法" prop="cateory_normal">
                    <el-select v-model="blog.cateory_operation" placeholder="请选择">
                      <el-option :disabled='isAdd' label="Paillier" value="1"></el-option>
                      <el-option :disabled='isAdd' label="BLP" value="2"></el-option>
                      <el-option :disabled='isAdd' label="BLP_other" value="3"></el-option>
                      <el-option label="BFV" value="4"></el-option>
                      <el-option label="CKKS" value="5"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <!--                <el-col :span="8">-->
                <!--                  <el-form-item label="乘法加密算法" prop="cateory_normal">-->
                <!--                    <el-select v-model="blog.cateory_multiply" placeholder="请选择">-->
                <!--                      <el-option label="BFV" value=1></el-option>-->
                <!--                      <el-option label="CKKS" value=2></el-option>-->
                <!--                    </el-select>-->
                <!--                  </el-form-item>-->
                <!--                </el-col>-->
                <!--                <el-row>-->
                <el-col :span="12">
                  <el-form-item label="设定者" prop="author" required>
                    <el-select v-model="blog.author" placeholder="请选择">
                      <el-option :value="users"></el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <!--                </el-row>-->

              </el-row>
            </div>

            <div class="form-group">
              <el-popover
                placement="top"
                width="160"
                v-model="visible">
                <p>确定提交么?</p>
                <div style="text-align: right; margin: 0">
                  <el-button size="mini" type="text" @click="visible = false">取消</el-button>
                  <el-button type="primary" size="mini" @click="submitform('blog')">确定</el-button>
                </div>
                <el-button slot="reference" type="primary">提交</el-button>
              </el-popover>
              <el-button type="primary" v-on:click="resetform" plain>重置</el-button>
            </div>
          </el-card>
        </el-row>
      </el-card>
    </el-form>

    <div v-else>
      <el-alert
        title="发布成功"
        type="success"
        show-icon>
      </el-alert>
      <h1>大成功～</h1>
      <h3>感谢你从本站付出的时间</h3>
      <router-link to="/bloglist"><i class="el-icon-s-promotion"></i>返回</router-link>
    </div>

  </div>
</template>

<script>
  export default {
    name: 'AddBlog',
    data() {
      return {
        isAdd: false,
        isTrain_disable: true,
        result_loading: true,
        flag: 0,  // 判断是否是新增风控模型函数，0为常用下拉框选取，1为定制单次，2为定制多次
        dialogFormVisible: false,
        dialogResultVisible: false,
        ModelFunction: '0',
        coefficientArray: [], // 系数
        powerArray: [], // 幂
        formula: {
          a: 0, // 系数
          n1: 0,  // ss的幂
          n2: 0,  // pf的幂
        },
        lastC: 0,
        MDivisor: 1,  // 分母
        simpleFormula: {
          a1: 0,
          a2: 0,
          c: 0,
        },
        LDivisor: 1,  // 分母
        // blog需要提交的数据
        blog: {
          title: '1',
          // 初始化分类列表数据
          cateory_normal: '1',
          cateory_operation: '1',
          // cateory_plus: '1',
          // cateory_multiply: '1',
          author: null
        },
        // cateorys_plus: ['Paillier', 'BLP', 'BLP_other'],
        // cateorys_multiply: ['Paillier', 'BLP', 'BLP_other', 'BFV', 'CKKS'],
        // 初始化用户数据
        users: '',
        // 表单是否被提交
        issubmitd: false,
        visible: false,
        loading: true,
        // 是否登录
        isLogin: false,
        rules: {
          title: [{required: true, message: '这是必填的!', trigger: 'blur'}],
          cateory_normal: [{required: true, message: '这是必填的!', trigger: 'blur'}],
          cateory_plus: [{required: true, message: '这是必填的!', trigger: 'blur'}],
          cateory_multiply: [{required: true, message: '这是必填的!', trigger: 'blur'}],
          author: [{required: true, message: '这是必填的!', trigger: 'blur'}]
        }
      }
    },
    methods: {
      // 验证表单
      submitform: function (submitForm) {
        if (this.flag === 0) {  // 下拉框内模型
          var params = {
            flag: this.flag,
            cateory_normal: this.blog.cateory_normal,
            cateory_operation: this.blog.cateory_operation,
            functionId: this.blog.title
          }
        } else if (this.flag === 1) { // 自定义一次模型函数
          var params = {
            flag: this.flag,
            cateory_normal: this.blog.cateory_normal,
            cateory_operation: this.blog.cateory_operation,
            a1: this.simpleFormula.a1,
            a2: this.simpleFormula.a2,
            c: this.simpleFormula.c,
            LDivisor: this.LDivisor
          }
          // console.log(this.simpleFormula.a1)
          // console.log(this.simpleFormula.a2)
          // console.log(this.simpleFormula.c)
        } else if (this.flag === 2) { // 自定义多次模型函数
          var params = {
            flag: this.flag,
            cateory_normal: this.blog.cateory_normal,
            cateory_operation: this.blog.cateory_operation,
            coefficientArray: this.coefficientArray,
            powerArray: this.powerArray,
            lastC: this.lastC,
            MDivisor: this.MDivisor
          }
          // console.log(this.coefficientArray)
          // console.log(this.powerArray)
        }
        this.$refs[submitForm].validate((valid) => {
          if (valid) {
            this.visible = false
            // this.issubmitd = true
            // console.log(params)
            this.$http.post('opens/changeStrategy', params)
              .then(response => {
                console.log(response)
              }, error => {
                console.log(error)
              })
            this.$notify({
              title: '修改成功！',
              message: '已提交, 风控模型已成功更换！',
              type: 'success'
            })
          }
        })
      },
      renewKey: function () {
        this.$axios.get('opens/renew_publicKey')
          .then(response => {
            if (response.data.status_code == 0) {
              this.$message.success("更新成功！")
            } else {
              this.$message.error("网络错误，更新失败！")
            }
          })
      },
      resetform: function () {
        this.blog = {
          title: null,
          cateory: null,
          author: null
        }
      },
      additem: function () {
        if (this.formula.a !== 0) {
          this.coefficientArray.push(Number(this.formula.a))
          var arrayObj = new Array()
          arrayObj.push(Number(this.formula.n1), Number(this.formula.n2), 0)
          this.powerArray.push(arrayObj)
          if (this.ModelFunction === '0') {
            this.ModelFunction = this.formula.a + 'ss^' + this.formula.n1 + '*pf^' + this.formula.n2
          } else {
            this.ModelFunction = this.ModelFunction + ' + ' + this.formula.a + 'ss^' + this.formula.n1 + '*pf^' + this.formula.n2
          }
        }
      },
      addC: function () {
        if (this.ModelFunction === '0') {
          this.ModelFunction = this.lastC
        } else {
          this.ModelFunction = this.ModelFunction + ' + ' + this.lastC
        }
      },
      addMDivisor: function () {
        if (this.MDivisor === '0') {
          this.$message.error("分母不能为0！")
        } else {
          this.ModelFunction = '(' + this.ModelFunction + ') / ' + this.MDivisor
        }
      },
      Mclear: function () {
        this.ModelFunction = '0'
        this.coefficientArray = []
        this.powerArray = []
        this.formula.a = 0
        this.formula.n1 = 0
        this.formula.n2 = 0
        this.lastC = 0
      },
      Lclear: function () {
        this.simpleFormula.a1 = 0
        this.simpleFormula.a2 = 0
        this.simpleFormula.c = 0
        this.LDivisor = 1
      },
      simpleSubmit: function () {
        this.flag = 1
        this.blog.title = this.simpleFormula.a1 + 'ss + ' + this.simpleFormula.a2 + 'pf + ' + this.simpleFormula.c
        this.dialogFormVisible = false
      },
      repeatedlySubmit: function () {
        this.flag = 2
        this.blog.title = this.ModelFunction
        this.dialogFormVisible = false
        this.isAdd = true
        this.blog.cateory_operation = '4'
      },
      trainUpload: function () {
        this.isTrain_disable = false
      },
      startTrain: function () {
        this.dialogResultVisible = true
        this.result_loading = true
        // setTimeout(function () {
        //   this.result_loading = false;
        // },3000)
        setTimeout(() => {
          this.result_loading = false
        }, 8 * 1000)
      }
    },
    created() {
      // 检测是否登录
      this.$axios.get('apis/user/getstatus?aa=60&kk=6')
        .then(response => {
          if (response.data.status === 1) {
            this.$router.push({path: '/user/login'})
          } else {
            this.isLogin = true
            this.users = response.data.username
            // 获取分类列表数据
            this.$axios.get('apis/get_info?cateory=1ds2ppJu2I9dl1&aa=32&kk=34')
              .then(response => {
                // this.cateorys = response.data.data
                this.loading = false
              }, error => {
                console.log(error)
              })
          }
        })
    }
  }
</script>

<style scoped>
  [v-cloak] {
    display: none;
  }
</style>
