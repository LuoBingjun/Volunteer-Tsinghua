import request from '@/utils/request'
import Cookies from 'js-cookie'

const key_isSuperUser='isSuperUser'

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

export function modifyUserInfo(options,id)
{
  if(id!==undefined)
  {
    return request({
      url:`/auth/webuser?id=${id}`,
      method:'put',
      data:options
    })
  }
  else
  {
    console.log(options)
    return request({
      url:`/auth/webuser`,
      method:'put',
      data:options
    })
  }
}

export function getUserList()
{
  return request({
    url:'/auth/listwebuser',
    method:'get',
  })
}

export function deleteUser(id)
{
  return request({
    url:`/auth/webuser?id=${id}`,
    method:'delete',
  })
}

export function addUser(options)
{
  return request({
    url:"/auth/webuser",
    method:"post",
    data:options
  })
}



export function setSuperUser(value)
{
  Cookies.set(key_isSuperUser,value)
}

export function isSuperUser()
{
  return Cookies.get(key_isSuperUser)=='false'?false:true
}


