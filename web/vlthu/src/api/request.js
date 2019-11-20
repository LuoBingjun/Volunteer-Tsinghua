/* eslint-disable */
import axios from 'axios'
import { MessageBox, Message } from 'element-ui'
const service = axios.create({
    baseURL: '/api', // url = base url + request url
    withCredentials: true, // send cookies when cross-domain requests
    timeout: 5000 // request timeout
})

service.interceptors.request.use(
  config => {
    // console.log("request拦截成功",config)
    // do something before request is sent
    return config
  },
  error => {
    // do something with request error
    Message({
      message: 'Error request'+(response.message || response.status),
      type: 'error',
      duration: 5 * 1000
    })
    console.log(error) // for debug
    return Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  /**
   * If you want to get http information such as headers or status
   * Please return  response => response
  */

  /**
   * Determine the request status by custom code
   * Here is just an example
   * You can also judge the status by HTTP Status Code
   */
  response => {
    // console.log('response拦截成功',response)
    // if the custom code is not 20000, it is judged as an error.
    if (response.status !== 200) {
      Message({
        message: '中间件捕捉到Error '+(response.message || response.status),
        type: 'error',
        duration: 5 * 1000
      })
      console.log('错误详情：',response)
      return Promise.reject(new Error(response.data || 'Error'))
    } else {
      return response
    }
  },
  error => {
    // console.log('err' + error) // for debug
    Message({
      message: '中间件捕捉到Error '+error,
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service  