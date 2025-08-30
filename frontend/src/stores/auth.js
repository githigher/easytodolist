// frontend/src/stores/auth.js

import { defineStore } from 'pinia';
import apiClient from '../services/api';
import router from '../router';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(credentials) {
      // --- 诊断日志第一步 ---
      // 打印从登录页面传递过来的 credentials 对象，看看它是否有值。
      console.log('1. [login action] 接收到的 credentials:', credentials);

      try {
        const formData = new URLSearchParams();
        
        // 检查 credentials 是否存在且有 username 属性
        if (credentials && credentials.username) {
          formData.append('username', credentials.username);
          formData.append('password', credentials.password);
        } else {
          console.error('错误：传递给 login action 的 credentials 对象为空或无效！');
          alert('登录信息为空，无法登录！');
          return; // 提前退出，不发送请求
        }

        // --- 诊断日志第二步 ---
        // 打印即将发送的 formData 内容。 .toString() 会把它转换成 "username=...&password=..." 的格式。
        console.log('2. [login action] 即将发送的 FormData:', formData.toString());

        const response = await apiClient.post('/token', formData);
        
        console.log('3. [login action] 登录成功，收到 token!');
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        apiClient.defaults.headers.common['Authorization'] = `Bearer ${this.token}`;
        router.push('/');

      } catch (error) {
        console.error('4. [login action] 登录失败! Error:', error.response?.data || error.message);
        alert('登录失败，请检查用户名和密码，并查看控制台错误信息。');
      }
    },
    async register(credentials) {
        try {
            await apiClient.post('/users/', credentials);
            await this.login({ username: credentials.username, password: credentials.password });
        } catch (error) {
            console.error('注册失败! Error:', error.response?.data || error.message);
            const detail = error.response?.data?.detail || '用户名可能已被占用！';
            alert(`注册失败: ${detail}`);
        }
    },
    logout() {
      this.token = null;
      localStorage.removeItem('token');
      delete apiClient.defaults.headers.common['Authorization'];
      router.push('/login');
    },
  },
});