<template>
    <div>
        <superuser v-if="isSuperUser"/>
        <user v-else/>
    </div>
</template>
<script>
import user from './user'
import superuser from './superuser'
export default {
    name:"info",
    components:{user,superuser},
    data(){
        return {
            isSuperUser:true
        }
    },
    methods:{

    },
    created(){
        this.isSuperUser=this.$store.getters.isSuperUser
        console.log(this.isSuperUser)
    }
}
</script>