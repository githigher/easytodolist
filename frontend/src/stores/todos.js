// frontend/src/stores/todos.js

import { defineStore } from 'pinia';
import apiClient from '../services/api';

export const useTodosStore = defineStore('todos', {
  state: () => ({
    todos: [],
    tags: [],
    isLoading: false,
  }),
  actions: {
    async fetchTodos() {
      this.isLoading = true;
      try {
        const response = await apiClient.get('/api/todos/');
        this.todos = response.data;
      } catch (error) {
        console.error('Failed to fetch todos:', error);
      } finally {
        this.isLoading = false;
      }
    },
    async fetchTags() {
      try {
        const response = await apiClient.get('/api/tags/');
        this.tags = response.data;
      } catch (error) {
        console.error('Failed to fetch tags:', error);
      }
    },
    async addTodo(todoData) {
      try {
        const response = await apiClient.post('/api/todos/', todoData);
        this.todos.push(response.data);
        // 如果有新标签，重新获取标签列表
        await this.fetchTags();
      } catch (error) {
        console.error('Failed to add todo:', error);
      }
    },
    async updateTodo(todoId, updateData) {
      try {
        const response = await apiClient.put(`/api/todos/${todoId}`, updateData);
        const index = this.todos.findIndex((t) => t.id === todoId);
        if (index !== -1) {
          this.todos[index] = response.data;
        }
      } catch (error) {
        console.error('Failed to update todo:', error);
      }
    },
    async deleteTodo(todoId) {
      try {
        await apiClient.delete(`/api/todos/${todoId}`);
        this.todos = this.todos.filter((t) => t.id !== todoId);
      } catch (error) {
        console.error('Failed to delete todo:', error);
      }
    },
    async addTag(tagName) {
        try {
            const response = await apiClient.post('/api/tags/', { name: tagName });
            this.tags.push(response.data);
        } catch (error) {
            console.error('Failed to add tag:', error);
        }
    },
    // --- NEW ACTIONS START ---
    async updateTag(tagId, newName) {
      try {
        const response = await apiClient.put(`/api/tags/${tagId}`, { name: newName });
        const updatedTag = response.data;

        // 更新标签列表
        const tagIndex = this.tags.findIndex(t => t.id === tagId);
        if (tagIndex !== -1) {
          this.tags[tagIndex] = updatedTag;
        }

        // 更新所有待办事项中关联的该标签，以实现界面实时刷新
        this.todos.forEach(todo => {
          const associatedTagIndex = todo.tags.findIndex(t => t.id === tagId);
          if (associatedTagIndex !== -1) {
            todo.tags[associatedTagIndex].name = updatedTag.name;
          }
        });
      } catch (error) {
        console.error('Failed to update tag:', error);
        alert('更新标签失败！');
      }
    },

    async deleteTag(tagId) {
      try {
        await apiClient.delete(`/api/tags/${tagId}`);

        // 从标签列表中移除
        this.tags = this.tags.filter(t => t.id !== tagId);

        // 从所有待办事项中移除关联的该标签
        this.todos.forEach(todo => {
          todo.tags = todo.tags.filter(t => t.id !== tagId);
        });
      } catch (error) {
        console.error('Failed to delete tag:', error);
        alert('删除标签失败！');
      }
    }
  },
});