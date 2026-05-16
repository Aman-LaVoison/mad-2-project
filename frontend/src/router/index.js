import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

// Auth components
import LoginView from '../views/auth/LoginView.vue'
import RegisterView from '../views/auth/RegisterView.vue'

// User components
import UserDashboard from '../views/user/DashboardView.vue'
import UserTreks from '../views/user/TreksView.vue'
import UserBookings from '../views/user/BookingsView.vue'
import UserProfile from '../views/user/ProfileView.vue'

// Admin components
import AdminDashboard from '../views/admin/DashboardView.vue'
import AdminTreks from '../views/admin/TreksView.vue'
import AdminStaff from '../views/admin/StaffView.vue'
import AdminUsers from '../views/admin/UsersView.vue'

// Staff components
import StaffDashboard from '../views/staff/DashboardView.vue'
import StaffTreks from '../views/staff/TreksView.vue'
import StaffParticipants from '../views/staff/ParticipantsView.vue'

// Landing page
import HomeView from '../views/HomeView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView
  },
  {
    path: '/auth/login',
    name: 'Login',
    component: LoginView,
    meta: { requiresAuth: false }
  },
  {
    path: '/auth/register',
    name: 'Register',
    component: RegisterView,
    meta: { requiresAuth: false }
  },
  {
    path: '/user',
    redirect: '/user/dashboard'
  },
  {
    path: '/user/dashboard',
    name: 'UserDashboard',
    component: UserDashboard,
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/treks',
    name: 'UserTreks',
    component: UserTreks,
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/bookings',
    name: 'UserBookings',
    component: UserBookings,
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/user/profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true, role: 'user' }
  },
  {
    path: '/admin',
    redirect: '/admin/dashboard'
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/treks',
    name: 'AdminTreks',
    component: AdminTreks,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/staff',
    name: 'AdminStaff',
    component: AdminStaff,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: AdminUsers,
    meta: { requiresAuth: true, role: 'admin' }
  },
  {
    path: '/staff',
    redirect: '/staff/dashboard'
  },
  {
    path: '/staff/dashboard',
    name: 'StaffDashboard',
    component: StaffDashboard,
    meta: { requiresAuth: true, role: 'staff' }
  },
  {
    path: '/staff/treks',
    name: 'StaffTreks',
    component: StaffTreks,
    meta: { requiresAuth: true, role: 'staff' }
  },
  {
    path: '/staff/treks/:trekId/participants',
    name: 'StaffParticipants',
    component: StaffParticipants,
    meta: { requiresAuth: true, role: 'staff' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const isAuthenticated = authStore.isLoggedIn
  const userType = authStore.userType

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/auth/login')
  } else if (to.meta.role && userType !== to.meta.role) {
    next('/')
  } else if ((to.path === '/auth/login' || to.path === '/auth/register') && isAuthenticated) {
    next(`/${userType}/dashboard`)
  } else {
    next()
  }
})

export default router
