<template>
  <div>
    <el-dialog :visible.sync="dialogVis" :with-header="true" :title="applyList[selectedForm].user.name+'的报名表单'" width="60%"> 
      <div style="margin:10px 60px">
        <el-form label-width="auto" >
          <el-form-item label="申请岗位">
            <el-input :value="applyList[selectedForm].job.job_name" :disabled="true" class="short"/>
          </el-form-item>
          <el-form-item v-for="(item,index) in form" :key="index" :label="item.text">
              <el-input :value="applyList[selectedForm].form[index]" v-if="item.type=='text'" :disabled="true"  class="short"/>
              <el-radio-group :value="parseInt(applyList[selectedForm].form[index])" v-else-if="item.type=='radioBox'" :disabled="true">
                <el-radio v-for="(item1,index1) in form[index].options" :key="index1" :label="index1">
                  {{item1.name}}
                </el-radio>
              </el-radio-group>
              <el-checkbox-group :value="applyList[selectedForm].form[index]" v-else :disabled="true">
                <el-checkbox v-for="(item1,index1) in form[index].options" :key="index1" :label="''+index1">
                  {{item1.name}}
                </el-checkbox>
              </el-checkbox-group>
            </el-form-item>
        </el-form>
      </div>
    </el-dialog>
    <el-table
      :data="applyList"
      tooltip-effect="dark"
      style="width: 100%" @selection-change="handleSelectionChange">
      <el-table-column type="selection"
        width="55" >
      </el-table-column>
      <el-table-column
        label="姓名"
        width="100">
        <template slot-scope="scope">{{ scope.row.user.name }}</template>
      </el-table-column>
      <el-table-column
        label="岗位"
        width="120">
        <template slot-scope="scope">{{ scope.row.job.job_name }}</template>
      </el-table-column>
      <el-table-column width="180" label="操作">
        <template slot-scope="scope">
          <el-button @click="showForm(scope.row)" plain>
            查看报名表单
          </el-button>
        </template>
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
            <i class="el-icon-check">  通过  </i>
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
            <i class="el-icon-close">  拒绝  </i>
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>
<script>
import {Message} from 'element-ui'
import {checkApplyRecord} from '@/api/project'
export default {
  name:'checkform',
  props:["form","applyList"],
  created(){
    console.log(this.applyList,this.form)
    this.isIndeterminate=false
    this.checkAll=false
    this.selected=[]
    for(var item in this.applyList)
    {
      this.applyList[item].form=JSON.parse(this.applyList[item].form)
    }

  },
  data(){
    return {
      isIndeterminate:undefined,
      checkAll:undefined,
      selected:undefined,
      dialogVis:false,
      selectedForm:0
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
    },
    showForm(id)
    {
      var index=this.applyList.indexOf(id)
      console.log(index)
      /*this.$alert(this.applyList[index].form,{
        dangerouslyUseHTMLString:true
      })*/
      this.selectedForm=index
      this.dialogVis=true
    },
    getNChoice(selectedForm,index)
    {
      var ans = JSON.parse(this.applyList[selectedForm].form)[index]
      return 666
    },
    get1Choice(selectedForm,index)
    {
      var ans = JSON.parse(this.applyList[selectedForm].form)[index]
      return this.form[index].options[ans]
    },
  },


}
</script>
<style>
.short{
  width:60%
}
</style>
