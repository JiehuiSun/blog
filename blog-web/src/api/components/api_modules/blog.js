const HTTP_GET = 'get'
const HTTP_POST = 'post'
const HTTP_DELETE = 'delete'
const HTTP_PUT = 'put'
const HTTP_PATCH = 'patch'
const APIS = {
	ListTag: {
        name: "ListTag",
		method: HTTP_GET,
		uri: "/api/blog/v1/tags/",
		desc: "标签列表"
	},
	DelTag: {
        name: "DelTag",
		method: HTTP_DELETE,
		uri: "/api/blog/v1/tags/",
		desc: "删除标签"
	},
	AddTag: {
        name: "AddTag",
		method: HTTP_POST,
		uri: "/api/blog/v1/tags/",
		desc: "添加标签"
	},
}

export default APIS