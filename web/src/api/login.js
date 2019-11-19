/* eslint-disable */
import request from '@/utils/request'
import serverUrl from '@/utils/serverUrl'
export function login(username,password) {
    console.log(`${serverUrl}/auth/weblogin`)
    return request({
        url: `/auth/weblogin`,
        method: 'post',
        head:{
            xhrFields:{
                withCredentials:true
            }
        },
        data: {
            username:username,
            password:password
        }
    });
  }