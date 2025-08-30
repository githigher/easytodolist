// frontend/src/router/index.js

import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import LoginView from '../views/LoginView.vue'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
  ],
})

// 导航守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.meta.requiresAuth;

  if (requiresAuth && !authStore.isAuthenticated) {
    // 如果页面需要认证但用户未登录，跳转到登录页
    next('/login');
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    // 如果用户已登录，但试图访问登录页，则跳转到主页
    next('/');
  } else {
    // 其他情况，正常放行
    next();
  }
});

export default router