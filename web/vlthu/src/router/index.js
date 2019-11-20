import Vue from 'vue'
import Router from 'vue-router'
import Project from '@/components/Project'
import Info from '@/components/Info'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/project',
      name: 'Project',
      component: Project,
    },
    {
      path: '/info',
      name: 'Info',
      component: Info
    },{
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
