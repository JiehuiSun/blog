import request from '@/utils/request'
import { formatUrl } from '@/utils/util'
import getApis from '@/api/components/index'
const APIS = getApis(['BlogHouse'])

export function getBlog(data) {
  const api = APIS['ListTag']
  const url = api.uri
  const method = api.method
  return request({ method, url, params: data })
}
export function delBlog(id) {
  const api = APIS['DelTag']
  const url = formatUrl(api.uri, id)
  const method = api.method
  return request({ method, url, params: data })
}