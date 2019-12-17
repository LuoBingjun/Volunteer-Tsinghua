<template>
    <div>
        <h2 style="margin:15px">
            <i class="el-icon-setting"></i> 管理所有用户
        </h2>
        <el-table :data="users" style="width: 100%">
            <el-table-column type="expand" label-width="auto">
                <template slot-scope="scope">
                    <userform :user="scope.row" @modifyuser='modifyUser' @deleteuser='deleteUser'></userform>
                </template>
            </el-table-column>
            <el-table-column
                label="团体名称"
                prop="name">
            </el-table-column>
            <el-table-column
                label="负责人"
                prop="manager">
            </el-table-column>
            <el-table-column
                label="联系电话"
                prop="phone">
            </el-table-column>
        </el-table>
        <el-card>
            <p><i class='el-icon-plus'> 添加新用户</i></p>
            <userform :user="newuser" @modifyuser='addUser'></userform>
        </el-card>
    </div>
</template>
<script>
import { getUserList,modifyUserInfo,deleteUser,addUser } from '@/api/user'
import { Message } from 'element-ui'
import userform from './userform'

export default {
    name: "user",
    data(){
        return{
            users:[],
            newuser:{
                isnew:true
            }
        }
    },
    components:{
        userform
    },
    methods:{
        getIndex(id)
        {
            for(var i in this.users)
            {
                if(this.users[i].id==id)
                    return i
            }
            return -1
        },
        modifyUser(form)
        {
            var formdata=new FormData()
            formdata.append('username',form.username)
            formdata.append('password',form.password)
            formdata.append('name',form.name)
            formdata.append('description',form.description)
            formdata.append('manager',form.manager)
            formdata.append('email',form.email)
            formdata.append('phone',form.phone)
            if(form.avatar)formdata.append('avatar',form.avatar)
            console.log("here!",formdata)
            modifyUserInfo(formdata,form.id).then(res=>{                
                Message({
                    message: '成功修改',
                    type: 'success',
                    duration: 5 * 1000
                })
                console.log(form,index)
                var index=this.getIndex(form.id)
                this.users[index].name=form.name
                this.users[index].manager=form.manager
                this.users[index].phone=form.phone
                this.users[index].email=form.email
                this.users[index].description=form.description                            
            }).catch(err=>{
                console.log(err)
            })
        },
        deleteUser(id)
        { 
            var that=this
            this.$confirm("该操作不可逆，是否继续","提示",{
                confirmButtonText: '确定',
                cancelButtonText:'取消',
                type:'warning'
            }).then(()=>{
                var index=that.getIndex(id)
                console.log(id,index)
                deleteUser(id).then(res=>{
                    Message({
                        message: '成功删除',
                        type: 'success',
                        duration: 5 * 1000
                    })
                    that.users[index].deleted=true
                }).catch(err=>{
                    Message({
                        message: 'error: '+err,
                        type: 'error',
                        duration: 5 * 1000
                    })
                })
            }).catch(()=>{
                Message({
                    message: '取消修改',
                    type: 'info',
                    duration: 5 * 1000
                })
            })
        },
        addUser(form){
            console.log("here")
            var formdata=new FormData()
            formdata.append('username',form.username)
            formdata.append('password',form.password)
            formdata.append('name',form.name)
            formdata.append('description',form.description)
            formdata.append('manager',form.manager)
            formdata.append('email',form.email)
            formdata.append('phone',form.phone)
            if(form.avatar)formdata.append('avatar',form.avatar)
            addUser(formdata).then(res=>{
                Message({
                    message: '成功添加',
                    type: 'success',
                    duration: 5 * 1000
                })
                this.users.push(form)
            }).catch(err=>{
                Message({
                    message: 'error: '+err,
                    type: 'error',
                    duration: 5 * 1000
                })
            })
        },
    },

    created(){
        getUserList().then(res=>{
            console.log(res)
            this.users=res.data
        }).catch(err=>{
            Message({
                message: 'Error: '+err,
                type: 'error',
                duration: 5 * 1000
            })
        })
    }
}
</script>
<style>
.short{
    width:60%
}
</style>