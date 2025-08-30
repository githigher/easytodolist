<!-- frontend/src/views/DashboardView.vue -->
<template>
  <div>
    <header class="dashboard-header">
      <h2>我的待办事项</h2>
      <button @click="authStore.logout()" class="secondary">登出</button>
    </header>

    <div class="controls card">
      <button @click="showForm = !showForm" class="primary">
        {{ showForm ? '取消创建' : '+ 添加新任务' }}
      </button>
      <div v-if="showForm" class="form-wrapper">
        <TodoForm @close="showForm = false" />
      </div>

      <div class="filters">
        <div class="filter-group">
          <span>按标签筛选:</span>
          <div class="tag-list">
            <button @click="selectedTagId = null" :class="{ active: selectedTagId === null }">全部</button>
            <div v-for="tag in todosStore.tags" :key="tag.id" class="tag-item">
              <!-- 编辑状态 -->
              <input
                v-if="editingTagId === tag.id"
                type="text"
                v-model="editingTagName"
                @keydown.enter="saveTag(tag)"
                @blur="saveTag(tag)"
                ref="editTagInput"
              />
              <!-- 显示状态 -->
              <button v-else @click="selectedTagId = tag.id" :class="{ active: selectedTagId === tag.id }">
                {{ tag.name }}
              </button>
              
              <!-- 操作按钮 -->
              <div class="tag-actions" v-if="editingTagId !== tag.id">
                <button class="icon-btn" @click="startEditTag(tag)">✏️</button>
                <button class="icon-btn" @click="handleDeleteTag(tag)">❌</button>
              </div>
            </div>
          </div>
        </div>
        <div class="filter-group">
          <span>排序:</span>
          <select v-model="sortBy">
            <option value="due_date">按截止日期</option>
            <option value="created_at_newest">按创建日期 (新->旧)</option>
            <option value="created_at_oldest">按创建日期 (旧->新)</option>
            <option value="status">按完成状态</option>
          </select>
        </div>
      </div>
    </div>

    <TodoList :todos="filteredAndSortedTodos" @edit="handleEdit" />

    <div v-if="editingTodo" class="modal-overlay" @click.self="editingTodo = null">
      <div class="modal-content card">
        <h3>编辑任务</h3>
        <TodoForm :todoToEdit="editingTodo" @close="editingTodo = null" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useTodosStore } from '../stores/todos';
import TodoList from '../components/TodoList.vue';
import TodoForm from '../components/TodoForm.vue';

const authStore = useAuthStore();
const todosStore = useTodosStore();

const showForm = ref(false);
const editingTodo = ref(null);
const selectedTagId = ref(null);
const sortBy = ref('due_date');

// --- 新增的用于标签编辑的状态 ---
const editingTagId = ref(null);
const editingTagName = ref('');
const editTagInput = ref(null);

onMounted(() => {
  todosStore.fetchTodos();
  todosStore.fetchTags();
});

const handleEdit = (todo) => {
  editingTodo.value = todo;
};

// --- 新增的标签处理方法 ---
const startEditTag = async (tag) => {
  editingTagId.value = tag.id;
  editingTagName.value = tag.name;
  // 等待DOM更新后，自动聚焦到输入框
  await nextTick();
  if(editTagInput.value && editTagInput.value[0]) {
    editTagInput.value[0].focus();
  }
};

const saveTag = (tag) => {
  if (editingTagName.value.trim() && editingTagName.value.trim() !== tag.name) {
    todosStore.updateTag(tag.id, editingTagName.value.trim());
  }
  editingTagId.value = null;
};

const handleDeleteTag = (tag) => {
    if(confirm(`确定要删除标签 "${tag.name}" 吗？\n(这不会删除关联的待办事项，只会解除它们的关联)`)) {
        todosStore.deleteTag(tag.id);
        // 如果删除的是当前筛选的标签，则重置筛选
        if (selectedTagId.value === tag.id) {
            selectedTagId.value = null;
        }
    }
};

const filteredAndSortedTodos = computed(() => {
    // ... (这部分代码保持不变) ...
    let todos = [...todosStore.todos];
    if (selectedTagId.value) {
        todos = todos.filter(todo => todo.tags.some(tag => tag.id === selectedTagId.value));
    }
    switch (sortBy.value) {
        case 'due_date':
            todos.sort((a, b) => {
                if (a.is_completed !== b.is_completed) return a.is_completed ? 1 : -1;
                if (!a.due_date) return 1;
                if (!b.due_date) return -1;
                return new Date(a.due_date) - new Date(b.due_date);
            });
            break;
        case 'created_at_newest':
            todos.sort((a, b) => b.id - a.id);
            break;
        case 'created_at_oldest':
            todos.sort((a, b) => a.id - b.id);
            break;
        case 'status':
            todos.sort((a, b) => a.is_completed - b.is_completed);
            break;
    }
    return todos;
});
</script>

<style scoped>
/* ... (保留大部分现有样式) ... */
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}
.controls {
  margin-bottom: 1.5rem;
}
.form-wrapper {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
}
.filters {
    margin-top: 1rem;
    display: flex;
    flex-direction: column; /* 改为纵向排列 */
    gap: 1.5rem;
    align-items: flex-start; /* 左对齐 */
}
.filter-group {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex-wrap: wrap;
}
.filter-group span {
    white-space: nowrap;
}
.tag-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.tag-item {
    display: flex;
    align-items: center;
    background-color: #f1f1f1;
    border-radius: var(--border-radius);
    overflow: hidden; /* 保证圆角效果 */
}
.tag-item button {
    background: none;
    border: none;
    padding: 0.5rem 0.8rem;
}
.tag-item button.active {
    background-color: var(--primary-color);
    color: white;
}
.tag-item input {
    padding: 0.5rem;
    border: 1px solid var(--primary-color);
    max-width: 120px;
}
.tag-actions {
    display: flex;
}
.icon-btn {
    padding: 0.5rem;
    font-size: 0.8rem;
    background-color: transparent;
    color: #555;
}
.icon-btn:hover {
    color: #000;
}
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}
.modal-content {
    width: 90%;
    max-width: 500px;
}
</style>