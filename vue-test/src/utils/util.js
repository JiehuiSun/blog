export function formatUrl(url, ...args) {
    // match example: '/api/mum/detail/{id}/{sign}/'
    var arr = url.split(/\{id\}/g)
    var i = 0
    var len = arr.length
    var resStr = ''
    if (len === 1) {
      // 没有匹配到
      console.error(url + ' 与{id}/格式不匹配！')
      return url
    }
    for (i = 0; i < len; i++) {
      resStr += arr[i] + (args[i] === void(0)? '': args[i])
    }
    return resStr
  }