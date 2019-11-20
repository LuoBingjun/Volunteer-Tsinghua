import request from './request'
export function login(username,password) {
    console.log(username)
    return request({
        url:'/auth/weblogin',
        method:'post',
        data:{
            username:username,
            password:password
        }
    })
}