<template>
    <el-card>
        <h1>
            <i class="el-icon-user">
            </i> {{form.name}} 的团体信息
        </h1>
        <userform :user="form" ref="userform" @modifyuser="modifyuser"/>
    </el-card>
</template>
<script>
import {getUserInfo,modifyUserInfo} from '@/api/user'
import { Message } from 'element-ui'
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
                phone:undefined
            },
        }
    },
    methods:{
        modifyuser(form)
        {
            this.form=form
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