import APIS from './_apis'
import roleApi from './roleApi'
function _getIdsByName(name) {
  var result = []
  var i = 0

  result = result.concat(roleApi[name].apis instanceof Array ? roleApi[name].apis : [])
  if (roleApi[name].children instanceof Array) {
    i = roleApi[name].children.length
    while (i--) {
      result = result.concat(roleApi[name].children[i].apis instanceof Array ? roleApi[name].children[i]
        .apis : [])
    }
  }
  return result
}

function _getIdsByNameArr(nameArr) {
  var _ids = [] // 未去重的ids
  var ids = [] // 结果ids
  var i = nameArr.length
  // 合并多个apis
  while (i--) {
    _ids = _ids.concat(_getIdsByName(nameArr[i]))
  }
  // 去除重复的id
  i = _ids.length
  while (i--) {
    if (ids.indexOf(_ids[i]) === -1) {
      ids.push(_ids[i])
    }
  }
  return ids
}
function getApis(nameArr) {
  var idArr = _getIdsByNameArr(nameArr)
  var result = {}
  var i = idArr.length
  while (i--) {
    if (APIS[idArr[i]]) {
      result[idArr[i]] = APIS[idArr[i]]
    }
  }
  return result
}

export default getApis
