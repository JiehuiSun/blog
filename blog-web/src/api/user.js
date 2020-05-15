import request from '@/utils/request'
import { formatUrl } from '@/utils/util'

export function login(data) {
  return request({
    url: '/users/v1/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    // url: formatUrl('/users/v1/user/', token),
    url: '/users/v1/user/' + token,
    method: 'get',
    // params: { token }
  })
}

export function logout() {
  return request({
    url: '/users/v1/logout/',
    method: 'post'
  })
}
