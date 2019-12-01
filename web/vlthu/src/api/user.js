import request from '@/utils/request'

export function login(data) {
  console.log(data)
  return request({
    url: '/auth/weblogin',
    method: 'post',
    data
  })
}
