<template>
    <div>
        <superuser v-if="isSuperUser"/>
        <user v-else/>
    </div>
</template>
<script>
import user from './user'
import superuser from './superuser'
import { isSuperUser } from '@/api/user'
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
        this.isSuperUser=isSuperUser()
        console.log(this.isSuperUser)
    }
}
</script>