<!-- frontend/src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <div class="login-card card">
      <h1>{{ isRegistering ? '注册' : '登录' }}</h1>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="username">用户名</label>
          <input type="text" id="username" v-model="credentials.username" required />
        </div>
        <div class="form-group">
          <label for="password">密码</label>
          <input type="password" id="password" v-model="credentials.password" required />
        </div>
        <button type="submit" class="primary full-width">
          {{ isRegistering ? '注册并登录' : '登录' }}
        </button>
      </form>
      <div class="toggle-form">
        <a href="#" @click.prevent="isRegistering = !isRegistering">
          {{ isRegistering ? '已有账户？点击登录' : '没有账户？点击注册' }}
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const isRegistering = ref(false);
const credentials = ref({
  username: '',
  password: '',
});

const handleSubmit = () => {
  if (isRegistering.value) {
    authStore.register(credentials.value);
  } else {
    authStore.login(credentials.value);
  }
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
}
.login-card {
  width: 100%;
  max-width: 400px;
}
h1 {
  text-align: center;
  margin-bottom: 1.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}
.full-width {
  width: 100%;
}
.toggle-form {
  margin-top: 1rem;
  text-align: center;
}
.toggle-form a {
  color: var(--primary-color);
  text-decoration: none;
}
</style>