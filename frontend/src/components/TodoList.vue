<!-- frontend/src/components/TodoList.vue -->
<template>
  <div class="todo-list">
    <div v-if="!todos.length" class="empty-state card">
      <p>太棒了，没有待办事项！或者...可以点击上方按钮添加一个新任务。</p>
    </div>
    <div v-else class="grid">
      <TodoCard 
        v-for="todo in todos" 
        :key="todo.id" 
        :todo="todo" 
        @edit="$emit('edit', todo)"
      />
    </div>
  </div>
</template>

<script setup>
import TodoCard from './TodoCard.vue';
defineProps({
  todos: {
    type: Array,
    required: true,
  },
});
defineEmits(['edit']);
</script>

<style scoped>
.empty-state {
  text-align: center;
  padding: 2rem;
  color: var(--secondary-color);
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}
</style>