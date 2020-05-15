/**
 * 所有的api集合
 * 一、定义唯一name
 * name = 所属顶级模块前缀 + 方法名（请确保自己所属模块的方法名唯一）
 */
import blog from './api_modules/blog'

// 引入模块
const HTTP_GET = 'get'
const HTTP_POST = 'post'
const HTTP_DELETE = 'delete'
const HTTP_PUT = 'put'
const HTTP_PATCH = 'patch'
const APIS = {
  ...blog,
}
export default APIS
