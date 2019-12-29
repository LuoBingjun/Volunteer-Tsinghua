<template>
    <div>
        <superuser v-if="superUser"/>
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
            superUser:undefined
        }
    },
    methods:{

    },
    created(){
        this.superUser=isSuperUser()
    }
}
</script>