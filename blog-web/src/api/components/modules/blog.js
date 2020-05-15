var tagApi = {
    BlogHouse: {
      name: 'BlogHouse',
      label: '博客',
      children: [
        {
          name: 'getList',
          label: '查看',
          apis: ['ListTag',]  // api_modules/xxx.js
        },
        {
          name: 'delList',
          label: '删除',
          apis: ['DelTag',]
        },
        {
          name: 'addList',
          label: '添加',
          apis: ['AddTag',]
        },
      ]
    },
  }
  
  export default tagApi
  