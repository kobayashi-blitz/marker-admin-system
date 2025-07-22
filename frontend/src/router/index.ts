import type { RouteRecordRaw } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import MarkersView from '../views/MarkersView.vue'
import NotificationsView from '../views/NotificationsView.vue'
import UsersView from '../views/UsersView.vue'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/markers'
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginView
  },
  {
    path: '/markers',
    name: 'Markers',
    component: MarkersView,
    meta: { requiresAuth: true }
  },
  {
    path: '/notifications',
    name: 'Notifications',
    component: NotificationsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/users',
    name: 'Users',
    component: UsersView,
    meta: { requiresAuth: true }
  }
]
