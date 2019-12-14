<template>
    <div>
        <p>superuser</p>
        <el-table :data="users" style="width: 100%" @expand-change="expandSelect">
            <el-table-column type="expand" label-width="auto">
                <template>
                    <el-form :model="form">
                        <el-form-item label="团体名称">
                            <el-input v-model="form.name" class="short" @input="test"></el-input>
                        </el-form-item>
                        <el-form-item label="负责人名">
                            <el-input v-model="form.manager" class="short"></el-input>
                        </el-form-item>
                        <el-form-item label="联系方式">
                            <el-input v-model="form.phone" class="short"></el-input>
                        </el-form-item>
                        <el-form-item label="电子邮箱">
                            <el-input v-model="form.email" class="short"></el-input>
                        </el-form-item>
                        <el-form-item label="团体描述">
                            <el-input v-model="form.description" type="textarea" :rows="6"></el-input>
                        </el-form-item>
                    </el-form>
                    <el-button type="primary">
                        <i class="el-icon-check" @click="modifyUser"> 确认修改</i>
                    </el-button>
                    <el-button type="danger" plain>
                        <i class="el-icon-close" @click="resetForm(form.index)"> 放弃修改</i>
                    </el-button>
                    <el-button type="danger">
                        <i class="el-icon-delete" @click="deleteUser"> 删除账号</i>
                    </el-button>
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
    </div>
</template>
<script>
import { getUserList,modifyUserInfo,deleteUser } from '@/api/user'
import { Message } from 'element-ui'

export default {
    name: "user",
    data(){
        return{
            users:[],
            form:{
                name:undefined,
                manager:undefined,
                id:undefined,
                index:undefined,
                email:undefined,
                phone:undefined,
                description:undefined
            }
        }
    },
    methods:{
        test(){
            console.log(this.users,this.form)
        },
        resetForm(item){
            /*this.form={
                name:this.users[item].name,
                manager:this.users[item].manager,
                id:item,
                phone:this.users[item].phone,
                email:this.users[item].email,
                index:this.users[item].index,
            }
            this.form.name=this.users[item].name
            this.form.manager=this.users[item].manager
            this.form.id=item
            this.form.phone=this.users[item].phone
            this.form.email=this.users[item].email
            this.form.index=this.users[item].index*/
            this.form=this.users[item]
        },
        expandSelect(row, expandedRows) {
            var that = this
            if (expandedRows.length) {
                that.expands = []
                if (row) {
                    that.expands.push(row.id)// 每次push进去的是每行的ID
                    that.resetForm(row.index)
                }
            } else {
                that.expands = []// 默认不展开
            }
        },
        modifyUser()
        {
            modifyUserInfo(this.form,this.form.id).then(res=>{
                Message({
                    message: '成功修改',
                    type: 'success',
                    duration: 5 * 1000
                })
                this.users[this.form.index]=this.form
            }).catch(err=>{
                console.log(err)
            })
        },
        resetUser()
        {
            resetForm(this.form.index)
        },
        deleteUser()
        {
            deleteUser(this.form.id).then(res=>{
                Message({
                    message: '成功删除',
                    type: 'success',
                    duration: 5 * 1000
                })
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
            for(var item in this.users)
            {
                this.users[item].index=item
            }
            this.resetForm(0)
            /*
            var users=res.data
            console.log(users)
            for(var item in users)
            {
                users[item].form={
                    name:users[item].name,
                    manager:users[item].manager,
                    phone:users[item].phone,
                    email:users[item].email,
                    id:users[item].id,
                    description:users[item].description,
                }
                users[item].index=item
            }
            this.users=users
            
            */
           console.log(this.users)
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