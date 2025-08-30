// frontend/src/services/api.js

import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const apiClient = axios.create({
  baseURL: 'http://101.34.237.144:12003',  // 线上
  // baseURL: 'http://127.0.0.1:8000'
  // --- 修正 ---
  // 不要在这里全局设置 Content-Type。
  // Axios 会根据发送的数据自动设置它。
  // - 如果发送的是普通 JS 对象，它会设为 'application/json'。
  // - 如果发送的是 URLSearchParams，它会设为 'application/x-www-form-urlencoded'。
  // 这正是我们需要的行为。
});

// 请求拦截器：在每个请求发送前，附加token
apiClient.interceptors.request.use(
  (config) => {
    // Pinia store 必须在拦截器函数内部获取，以避免循环依赖问题
    const authStore = useAuthStore();
    const token = authStore.token;
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default apiClient;