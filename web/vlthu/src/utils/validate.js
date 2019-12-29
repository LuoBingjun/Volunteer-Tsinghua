/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  const valid_map = ['admin', 'editor']
  return valid_map.indexOf(str.trim()) >= 0
}

export function checkPhone(rule,value,callback){
  var pattern=/^[0-9]{11}$/;
  if(pattern.test(value))
  {
    callback();
  }
  else
  {
    callback(new Error('请输入正确的11位电话号码'))
  }
}

export function checkEmail(rule,value,callback){
  var pattern=/^[a-z0-9]+([._\\-]*[a-z0-9])*@([a-z0-9]+[-a-z0-9]*[a-z0-9]+.){1,63}[a-z0-9]+$/
  if(pattern.test(value))
  {
    callback();
  }
  else
  {
    callback(new Error('请输入正确格式的电子邮箱'))
  }
}
