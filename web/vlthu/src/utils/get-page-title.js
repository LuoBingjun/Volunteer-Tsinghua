import defaultSettings from '@/settings'

const title = defaultSettings.title || 'Vlthu'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
