import { createRouter, createWebHistory} from 'vue-router'
import HomeView from '../views/HomeView.vue'

const Layoutmap = [
  {
    path: 'user', 
    name: 'User',
    component: () => import('@/views/UserView.vue'),
    meta: { roles: 'admin' },
    icon: 'el-icon-user'
  },
  {
    path: 'client',
    name: 'Client',
    component: () => import('@/views/ClientView.vue')
  },
  {
    path: 'branch',
    name: 'Branch',
    component: () => import('@/views/BranchView.vue'),
    meta: { roles: 'admin' }
  },
  {
    path: 'department',
    name: 'Department',
    component: () => import('@/views/DepartmentView.vue'),
    meta: { roles: 'admin' }
  },
  {
    path: 'employee',
    name: 'Employee',
    component: () => import('@/views/EmployeeView.vue'),
    meta: { roles: 'admin' }
  },
  {
    path: 'creditAccount',
    name: 'CreditAccount',
    component: () => import('@/views/CreditAccountView.vue')
  },
  {
    path: 'savingsAccount',
    name: 'SavingsAccount',
    component: () => import('@/views/SavingsAccountView.vue')
  },
  {
    path: 'loan',
    name: 'Loan',
    component: () => import('@/views/LoanView.vue')
  },
  {
    path: 'repayment',
    name: 'Repayment',
    component: () => import('@/views/RepaymentView.vue')
  },
  {
    path: 'transaction',
    name: 'Transaction',
    component: () => import('@/views/TransactionView.vue')
  },
  {
    path: 'creditTransaction',
    name: 'CreditTransaction',
    component: () => import('@/views/CreditTransactionView.vue')
  }
]

export { Layoutmap };

const routes= [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component:() => import( '../views/AboutView.vue')
  },
  {
    path: '/usercenter',
    name: 'UserCenter',
    component: () => import('@/views/UserCenterView.vue')
  },
  {
    path: '/login', 
    name: 'Login', 
    component: ()  => import('../views/LoginView.vue')
  },
  {
    path: '/layout', 
    name: 'Layout',
    component: () => import('../layout/Index.vue'),
    children: [...Layoutmap]
  },
]


const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

import NProgress from 'nprogress'   // 导入 nprogress
import 'nprogress/nprogress.css'   // 导入样式，否则看不到效果
import store from '../store/index'

NProgress.configure({ showSpinner: true })   // 显示右上角螺旋加载提示

router.beforeEach((to, from, next) => { 
    NProgress.start()   // 开启进度条
    if(store.getters.isLoggedIn) {
        if(to.name == 'Login') {
            next({name: 'Layout'})
        }
        else
        {
            let roles = store.getters.getRoles;
            let hasPermission = true;
            if(to.meta.roles) {
                hasPermission = roles.some(role => to.meta.roles.includes(role))
            }
            if(hasPermission) {
                next()
            }
            else {
                next({name: 'Layout'})
            }
        }
    }
    else{
        if(to.name == 'Login') {
            next()
        }
        else {
            next({name: 'Login'})
        }
    }
})

router.afterEach(() => {
  NProgress.done()   // 关闭进度条
})

