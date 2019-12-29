<template>
    <div>
        <el-table :data="signlist">
            <el-table-column label="签到标题" prop="title"></el-table-column>
            <el-table-column label="签到位置" prop="position"></el-table-column>
            <el-table-column label="开始时间" prop="b_time"></el-table-column>
            <el-table-column label="结束时间" prop="e_time"></el-table-column>
        </el-table>
    </div>
</template>
<script>
export default {
    name:"signlist",
    props:['signlist'],
    data(){
        return{

        }
    },
    created(){
        console.log("签到列表：",this.signlist)
        for(var item in this.signlist)
        {
            this.signlist[item].b_time=new Date(this.signlist[item].begin_time).toLocaleString()
            this.signlist[item].e_time=new Date(this.signlist[item].end_time).toLocaleString()

        }
    },
    methods:{

    }

}
</script>