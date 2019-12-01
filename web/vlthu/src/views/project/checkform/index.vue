<template>
  <table>
    <!--<tr>
      <td>
        <el-checkbox :indeterminate="isIndeterminate" v-model="checkAll" @change="handleCheckAll">
          全选
        </el-checkbox>
      </td>
      <td>申请岗位</td>
    </tr>
    <tr v-for='item in applyList' :key='item.index'>
      <td>
        <el-checkbox>
          {{item.user.name}}
        </el-checkbox>
      </td>
      <td>{{item.job.job_name}}</td>
      <td>
        <el-button v-if="item.status!='P'" @click="handleRecord" :id="'Y'+item.id" type="success" icon="el-icon-check">通过</el-button>
        <el-button v-if="item.status=='P' " disabled='true' type="success" icon="el-icon-check">已通过</el-button>
      </td> 
      <td>
        <el-button v-if="item.status!='N'" @click="handleRecord" :id="'N'+item.id" type="danger" icon="el-icon-close">拒绝</el-button>
        <el-button v-if="item.status=='N'" disabled='true' type="danger" icon="el-icon-close">已拒绝</el-button>
      </td>
    </tr>-->
  </table>
</template>
<script>
import {Message} from 'element-ui'
export default {
  name:'checkform',
  props:["applyList"],
  created(){
    console.log(this.applyList)
  },
  data(){
    return {
      isIndeterminate:undefined,
      checkAll:undefined,

    }
  },
  methods:{
    
  }
}
</script>

