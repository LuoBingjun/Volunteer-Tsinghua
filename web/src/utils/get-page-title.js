import defaultSettings from '@/settings'

const title = defaultSettings.title || '志愿清华管理端'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    if(pageTitle=='退出登陆')return `登陆 - ${title}`
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
