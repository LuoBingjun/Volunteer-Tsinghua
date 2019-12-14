<template>
    <el-card>
        <h1>
            <i class="el-icon-user">
            </i> {{oldname}}的团体信息
        </h1>
        <el-form :model="form" :rules="rules" label-width="auto" ref="form">
            <el-form-item label="团体名称" prop="name">
                <el-input class="short" v-model="form.name"/>
            </el-form-item>
            <el-form-item label="团体描述" prop="description">
                <el-input class="short" v-model="form.description"/>
            </el-form-item>
            <el-form-item label="电子邮箱" prop="email">
                <el-input class="short" v-model="form.email"/>
            </el-form-item>
            <el-form-item label="电话号码" prop="phone">
                <el-input class="short" v-model="form.phone"/>
            </el-form-item>
            <el-button type="primary" @click="updateInfo"> <i class="el-icon-upload"> 更新</i></el-button>
            <el-button type="danger" @click="resetInfo" plain> <i class="el-icon-close"> 重置</i></el-button>
        </el-form>
    </el-card>
</template>
<script>
import {getUserInfo,modifyUserInfo} from '@/api/user'
import { Message } from 'element-ui'
export default {
    name: "user",
    data(){
        var emailValidator=(rule,value,callback)=>{
            callback()
        }
        var phoneValidator=(rule,value,callback)=>{
            callback()
        }
        return{
            oldname:undefined,
            form:{
                name:undefined,
                description:undefined,
                manager:undefined,
                email:undefined,
                phone:undefined
            },
            rules:{
                email:[
                    {validator:emailValidator,message:"邮箱不符合格式",trigger:"blur"}
                ],
                phone:[
                    {validator:phoneValidator,message:"手机号不符合格式",trigger:"blur"}
                ]
            }
        }
    },
    methods:{
        updateInfo(){
            var that=this
            this.$refs.form.validate().then((valid)=>{
                if(valid)
                {
                    modifyUserInfo(that.form).then(()=>{
                        that.oldname=that.form.name
                        Message({
                            message: '成功修改',
                            type: 'success',
                            duration: 5 * 1000
                        })
                        that.$router.push({path:'/dashboard'})
                    })
                }
            }).catch(err=>{
                Message({
                    message: 'Error: '+err,
                    type: 'error',
                    duration: 5 * 1000
                })
            })
        },
        resetInfo(){
            getUserInfo().then(res=>{
                this.form=res.data
                this.oldname=res.data.name
            }).catch(err=>{
                Message({
                    message: 'Error: '+err,
                    type: 'error',
                    duration: 5 * 1000
                })
            })
        }
    },
    created(){
        getUserInfo().then(res=>{
            this.form=res.data
            console.log(this.form)
            this.oldname=res.data.name
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