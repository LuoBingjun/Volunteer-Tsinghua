<template>
    <div style="margin:40px;">
        <h2>
            <i class="el-icon-user">
            </i> {{form.name}}的团体信息
        </h2>
        <userform :user="form" ref="userform" @modifyuser="modifyuser"/>
    </div>
</template>
<script>
import {getUserInfo,modifyUserInfo} from '@/api/user'
import { Message, MessageBox } from 'element-ui'
import userform from '../superuser/userform'

export default {
    name: "user",
    components:{userform},
    data(){
        return{
            form:{
                name:undefined,
                description:undefined,
                manager:undefined,
                email:undefined,
                phone:undefined,
                avatar:undefined,
                id:undefined
            },
        }
    },
    methods:{
        modifyuser(form)
        {
            console.log("form->",form)
            var that=this
            var formdata=new FormData()
            formdata.append('name',form.name)
            formdata.append('description',form.description)
            formdata.append('manager',form.manager)
            formdata.append('email',form.email)
            formdata.append('phone',form.phone)
            if(form.avatar)formdata.append('avatar',form.avatar)

            modifyUserInfo(formdata).then(res=>{
                Message({
                    message:"成功修改",
                    type:"success",
                    duration:1500
                })
                that.$router.push('/dashboard')
            }).catch(err=>{
                Message({
                    message:"error: "+err,
                    type:'error',
                    duration:5000
                })
            })
        }
    },
    created(){
        var that=this
        getUserInfo().then(res=>{
            var form=res.data
            form.nodelete=true
            that.form=form
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