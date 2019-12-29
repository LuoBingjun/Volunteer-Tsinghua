<template>
    <div>
        <el-form :model="form" :rules="rules" ref="form">           
            <el-form-item label="登陆名称" prop="username" v-if="isnew">
                <el-input v-model="form.username" class="short"></el-input>
            </el-form-item>
            <el-form-item label="登陆密码" v-if="isnew" prop="password">
                <el-input v-model="form.password" class="short" type="password"></el-input>
            </el-form-item>
            <el-divider v-if="isnew"></el-divider>
            <el-form-item label="团体名称" prop="name">
                <el-input v-model="form.name" class="short"></el-input>
            </el-form-item>
            <el-form-item label="负责人名" prop="manager"> 
                <el-input v-model="form.manager" class="short"></el-input>
            </el-form-item>
            <el-form-item label="联系方式" prop="phone">
                <el-input v-model="form.phone" class="short"></el-input>
            </el-form-item>
            <el-form-item label="电子邮箱" prop="email">
                <el-input v-model="form.email" class="short"></el-input>
            </el-form-item>
            <el-form-item label="团体描述" prop="description">
                <el-input v-model="form.description" type="textarea" :rows="6"></el-input>
            </el-form-item>
            <el-form-item label="上传头像">
                <img v-if="avatar_url" :alt="avatar_url" :src="avatar_url" style="height:120px;width:120px;float:right" />
                <el-upload
                    action="#"
                    list-type="picture-card"
                    :auto-upload="true"
                    :multiple="false"
                    :limit="1"
                    name="avatar"
                    :http-request="getavatar"
                    ref="uploader"
                    :on-remove="removeavatar"
                    accept="image/*"
                >
                    <i slot="default" :class="form.avatar?'el-icon-close':'el-icon-plus'"></i>
                </el-upload>
            </el-form-item>
        </el-form>
        <el-button type="primary" @click="modifyUser" v-if="isnew">
            <i class="el-icon-plus"> 新建用户</i>
        </el-button>
        <el-button type="primary" @click="modifyUser" v-if="!isnew">
            <i class="el-icon-check"> 确认修改</i>
        </el-button>
        <el-button type="danger" @click="resetForm" v-if="!isnew" plain>
            <i class="el-icon-close"> 放弃修改</i>
        </el-button>
        <el-button type="danger" @click="deleteUser" v-if="!isnew && !nodelete">
            <i class="el-icon-delete"> 删除账号</i>
        </el-button>
    </div>
</template>
<script>
import {Message} from 'element-ui'
import {checkPhone, checkEmail} from '@/utils/validate'
export default {
    name:'userform',
    props:['user'],
    data(){
        return{
            form:{
                username:undefined,
                id:undefined,
                name:undefined,
                manager:undefined,
                phone:undefined,
                email:undefined,
                description:undefined,
                password:undefined,
                avatar:undefined
            },
            rules:{
                username:{required:true, message: "登陆名称不能为空", trigger: "blur"},
                name:{required: true, message: "团体名称不能为空", trigger: "blur"},
                manager:{required:true,message:"负责人不能为空",trigger:'blur'},
                phone:[{required:true,message:"电话号码不能为空",trigger:'blur'},{validator: checkPhone,trigger:'blur'}],
                email:[{required:true,message:"电子邮箱不能为空",trigger:'blur'},{validator: checkEmail,trigger:'blur'}],
                description:{required:true,message:"团体描述不能为空",trigger:'blur'},
                password:{required:true,message:"密码不能为空",trigger:'blur'}
            },
            isnew:undefined,
            nodelete:undefined
        }
    },
    watch:{
        user(){
            this.resetForm()
        }
    },
    methods:{
        modifyUser(){
            this.$refs.form.validate().then((valid)=>{
                if(valid){
                    this.$emit('modifyuser',this.form)
                }
            }).catch(err=>{})
        },
        resetForm(){
            this.form.name=this.user.name
            this.form.manager=this.user.manager
            this.form.phone=this.user.phone
            this.form.email=this.user.email
            this.form.description=this.user.description
            this.form.id=this.user.id
            this.avatar_url=this.user.avatar
            this.form.avatar=undefined
            if(this.$refs.uploader)this.$refs.uploader.clearFiles()
            else console.log("uploader: empty",)

            this.form.nodelete=this.user.nodelete
            this.isnew=this.user.isnew
            this.nodelete=this.user.nodelete
        },
        deleteUser(){
            this.$emit('deleteuser',this.form.id)
        },
        getavatar(file)
        {
            var that=this
            new Promise(function(resolve,reject){
                let _URL=window.URL||window.webkitURL
                let img=new Image()
                img.onload=function(){
                    let valid=(img.width==img.height)
                    valid?resolve():reject()
                }
                img.src=_URL.createObjectURL(file.file)
            }).then(()=>{
                that.form.avatar=file.file
            }).catch(()=>{
                Message({
                    message:"上传的图片不符合要求（要求宽高比1:1）",
                    type:'warning',
                    duration:5000
                })
                that.$refs.uploader.clearFiles()
            })
        },
        removeavatar()
        {
            this.form.avatar=undefined
        },
    },
    created(){
        console.log("user is",this.user)
        this.resetForm()
    }
}
</script>

<style>
.short{
    width:60%
}
</style>