<template>
  <div>
    <h1>Project# {{projectID}}: {{title}}</h1>
    <div> 
      <p> 项目详情：{{content}} </p>
      <p> 需求：</p>
      <ol>
        <li v-for='item in requirements' :key='item'> 
          <p>
            {{item}}
          </p><br >
        </li>
      </ol>
    </div>
    <button @click="changeRouter">点击返回</button>
    <label></label>
  </div>
</template>

<script>
import {getProjectDetails} from '@/api/project'
import {Message} from 'element-ui'
export default {
  name: 'Project',
  data () {
    return {
      msg: 'Welcome to Your Vue.js App',
      projectID: undefined,
      title: undefined,
      content:undefined,
      cover: undefined,
      require_num:undefined,
      status:undefined,
      requirements:undefined,
      form:undefined,
      time:undefined,
      deadline:undefined,
    }
  },
  methods:{
    changeRouter(){
      console.log('点击了按钮')
      this.$router.pop()
    }
  },
  created(){
    console.log('project页面加载完毕,route为',this.$route)
    this.$data.projectID=this.$route.query.projectID
    /*
    以下获取数据，由于后端没写好，所以直接获取
    getProjectDetails(this.projectID).then(res =>{
      console.log('项目详情',res)
    }).catch(err =>{
      Message({
        message: 'Error request'+err,
        type: 'error',
        duration: 5 * 1000
      })
    })*/

    var res={
        "id": 1,
        "cover": "封面图片url",
        "title": "标题",
        "content": "内容",
        "require_num": 5, // "需求人数"
        "requirements": "[\"first\",\"second\"]" ,
        "status": "", // F-已结束 W-已报名待审核 P-报名通过正在进行 N-无法报名 A-可报名
        "form": "表单",
        "time": "发起时间",
        "deadline": "截止时间"
    }
    this.title=res.title
    this.content=res.content
    this.cover=res.cover
    this.require_num=res.require_num
    this.status=res.status
    this.requirements=JSON.parse(res.requirements)
    this.form=res.form
    this.time=res.time
    this.deadline=res.deadline
    console.log("得到的需求们：",this.requirements)
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1, h2 {
  font-weight: normal;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
