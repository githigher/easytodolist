<!-- frontend/src/components/TodoCard.vue -->
<template>
  <div class="todo-card card" :class="{ completed: todo.is_completed }">
    <div class="card-header">
      <input type="checkbox" :checked="todo.is_completed" @change="toggleComplete" />
      <h3 class="title">{{ todo.title }}</h3>
    </div>
    <p v-if="todo.description" class="description">{{ todo.description }}</p>
    <div v-if="todo.due_date" class="due-date" :class="dueDateStatus.class">
      {{ dueDateStatus.text }}
    </div>
    <div class="tags">
        <span v-for="tag in todo.tags" :key="tag.id" class="tag">{{ tag.name }}</span>
    </div>
    <div class="actions">
      <button @click="$emit('edit', todo)">编辑</button>
      <button @click="handleDelete" class="danger">删除</button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useTodosStore } from '../stores/todos';

const props = defineProps({
  todo: {
    type: Object,
    required: true,
  },
});
defineEmits(['edit']);

const todosStore = useTodosStore();

const toggleComplete = () => {
  todosStore.updateTodo(props.todo.id, {
    ...props.todo,
    is_completed: !props.todo.is_completed,
    tags: props.todo.tags.map(t => t.id)
  });
};

const handleDelete = () => {
    if(confirm(`确定要删除任务 "${props.todo.title}" 吗？`)) {
        todosStore.deleteTodo(props.todo.id);
    }
}

const dueDateStatus = computed(() => {
    if (!props.todo.due_date) return { text: '', class: ''};
    const today = new Date();
    today.setHours(0,0,0,0);
    const dueDate = new Date(props.todo.due_date);
    const diffTime = dueDate.getTime() - today.getTime();
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays < 0) return { text: `已逾期 ${-diffDays} 天`, class: 'overdue' };
    if (diffDays === 0) return { text: '今天截止', class: 'due-today' };
    if (diffDays === 1) return { text: '明天截止', class: '' };
    return { text: `还剩 ${diffDays} 天`, class: '' };
});
</script>

<style scoped>
.todo-card {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: all 0.2s ease-in-out;
}
.todo-card.completed {
  opacity: 0.6;
}
.todo-card.completed .title {
  text-decoration: line-through;
  color: var(--completed-color);
}
.card-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}
.card-header input[type="checkbox"] {
  width: 20px;
  height: 20px;
}
.title {
  margin: 0;
  font-size: 1.2rem;
}
.description {
  color: var(--secondary-color);
  font-size: 0.9rem;
}
.due-date {
    font-weight: bold;
    font-size: 0.9rem;
}
.due-date.overdue {
    color: var(--danger-color);
}
.due-date.due-today {
    color: orange;
}
.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.tag {
    background-color: #e9ecef;
    padding: 0.2rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
}
.actions {
  margin-top: auto; /* Pushes actions to the bottom */
  padding-top: 0.5rem;
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
}
</style>