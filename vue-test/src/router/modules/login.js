import Layout from '@/layout'
export default {
  name: 'login',
  path: '/login',
  component: () =>
    import('@/views/login/index'),
  hidden: true
}
