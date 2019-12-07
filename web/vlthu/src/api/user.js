import request from '@/utils/request'

export function login(data) {
  console.log(data)
  return request({
    url: '/auth/weblogin',
    method: 'post',
    data
  })
}

export function getUserInfo(id)
{
  if(id!==undefined)
  {
    return request({
      url:`/auth/webuser?id=${id}`,
      method:"get"
    })
  }
  else{
    return request({
      url:`/auth/webuser`,
      method:"get"
    })
  }
}

export function modifyUserInfo(id,options)
{
  return request({
    url:`/auth/webuser?id=${id}`,
    method:'put',
    data:options
  })
}
