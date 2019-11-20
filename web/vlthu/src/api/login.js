import request from './request'
export function login(username,password) {
    return request({
        url:'/auth/weblogin',
        method:'post',
        data:{
            username:username,
            password:password
        }
    })
}