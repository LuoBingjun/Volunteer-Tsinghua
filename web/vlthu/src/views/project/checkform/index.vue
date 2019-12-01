<template>
  <el-table
    :data="applyList"
    tooltip-effect="dark"
    style="width: 100%" @selection-change="handleSelectionChange">
    <el-table-column type="selection"
      width="55" >
    </el-table-column>
    <el-table-column
      label="姓名"
      width="180">
      <template slot-scope="scope">{{ scope.row.user.name }}</template>
    </el-table-column>
    <el-table-column
      label="岗位"
      width="120">
      <template slot-scope="scope">{{ scope.row.job.job_name }}</template>
    </el-table-column>
    <el-table-column
      width="150">
      <template slot="header">
        <el-button type="success" @click="handleAll(true)" :disabled="selected.length==0">
          通过选中项
        </el-button>
      </template>

      <template slot-scope="scope">
        <el-button type="success" @click="handleOne(true,scope.row.id)" :disabled="scope.row.status=='P'">
          <i class="el-icon-check"></i>
          通过{{scope.row.status}}
        </el-button>
      </template>
    </el-table-column>
    <el-table-column
      width="150">
      <template slot="header">
        <el-button type="danger" @click="handleAll(false)" :disabled="selected.length==0">
          拒绝选中项
        </el-button>
      </template>
      <template slot-scope="scope">
        <el-button type="danger" @click="handleOne(false,scope.row.id)" :disabled="scope.row.status=='N'">
          <i class="el-icon-close"></i>
          拒绝{{scope.row.status}}
        </el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
<script>
import {Message} from 'element-ui'
import {checkApplyRecord} from '@/api/project'
export default {
  name:'checkform',
  props:["applyList"],
  created(){
    console.log(this.applyList)
    this.isIndeterminate=false
    this.checkAll=false
    this.selected=[]
  },
  data(){
    return {
      isIndeterminate:undefined,
      checkAll:undefined,
      selected:undefined,
    }
  },
  methods:{
    handleOne(c,id,hidePrompt){
      console.log(c,id)
      for(var i in this.selected)
      {
        console.log(this.selected[i])
        if(this.selected[i].id==id)
        {
          console.log(this.selected[i].status,"状态")
          if((this.selected[i].status=='P' && c==true) ||
             (this.selected[i].status=='N' && c==false) )
             {
               if(!hidePrompt)
               {
                  Message({
                    message: c?"已审核通过":"已拒绝请求",
                    type: 'success',
                    duration: 5 * 1000
                  })
               }
               return
             }
          else break
        }
      }
      checkApplyRecord(id,c).then(res=>{
        if(!hidePrompt){
          Message({
            message: c?"已审核通过":"已拒绝请求",
            type: 'success',
            duration: 5 * 1000
          })
        }
        for(var i in this.applyList)
        {
          if(this.applyList[i].id==id)this.applyList[i].status=c?'P':'N'
        }
      }).catch(err=>{
        if(!hidePrompt){
          Message({
            message: err,
            type: 'error',
            duration: 5 * 1000
          })
        }
      })
    },
    handleSelectionChange(val){
      console.log(val)
      this.selected=val
    },
    handleAll(c){
      var that=this
      var hideMsg=false
      for(var k in this.selected)
      {
        var id=this.selected[k].id
        this.handleOne(c,id,hideMsg)  // show the first request only
        hideMsg=true
      }
    }
  },


}
</script>

