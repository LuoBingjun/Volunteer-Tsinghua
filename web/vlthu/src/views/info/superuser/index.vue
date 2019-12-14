<template>
    <div>
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
            console.log("INDEX! ")
            for(var i in this.users)
            {
                if(this.users[i].id==id)
                    return i
            }
            return -1
        },
        modifyUser(form)
        {
            modifyUserInfo(form,form.id).then(res=>{
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
            var index=this.getIndex(id)
            console.log(id,index)
            deleteUser(id).then(res=>{
                Message({
                    message: '成功删除',
                    type: 'success',
                    duration: 5 * 1000
                })
                this.users[index].deleted=true
            }).catch(err=>{
                Message({
                    message: 'error: '+err,
                    type: 'error',
                    duration: 5 * 1000
                })
            })
        },
        addUser(form){
            console.log("here")
            addUser({
                username:form.name,
                password:form.password,
                name:form.name,
                description:form.description,
                manager:form.manager,
                email:form.email,
                phone:form.phone
            }).then(res=>{
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