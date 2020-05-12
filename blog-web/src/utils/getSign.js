import md5 from 'js-md5'
const APPID = 's3005'
// const APPID = 'm2004'

const APPKEY = '43ce266372b8b94415686532db1d99eb'

function getSign(config, usertoken = "") {
  var uri = /api/.test(config.url) ? config.url : '/api' + config.url
  var timestamp = +new Date()
  var s = 'appid=' + APPID + '&timestamp=' + timestamp + '&uri=' + uri
  if (usertoken) {
    s += '&usertoken=' + usertoken
  }
  var sign = md5(s + APPKEY)
  var signObj = {
    "X-AUTH-APPID": APPID,
    "X-AUTH-TIMESTAMP": timestamp,
    "X-AUTH-SIGN": sign,
    "X-AUTH-USERTOKEN": usertoken
  }
  return signObj
}

export default getSign
