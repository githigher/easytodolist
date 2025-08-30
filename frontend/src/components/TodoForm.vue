<!-- frontend/src/components/TodoForm.vue -->
<template>
  <form @submit.prevent="handleSubmit" class="todo-form">
    <div class="form-group">
      <input type="text" v-model="form.title" placeholder="任务标题 (必填)" required />
    </div>
    <div class="form-group">
      <textarea v-model="form.description" placeholder="任务描述 (选填)"></textarea>
    </div>
    <div class="form-group">
      <label>截止日期</label>
      <input type="date" v-model="form.due_date" />
    </div>
    <div class="form-group">
        <label>标签 (可多选)</label>
        <div class="tag-selector">
            <label v-for="tag in todosStore.tags" :key="tag.id">
                <input type="checkbox" :value="tag.id" v-model="form.tags" /> {{ tag.name }}
            </label>
        </div>
        <div class="new-tag-creator">
            <input type="text" v-model="newTagName" placeholder="或创建新标签" @keydown.enter.prevent="createNewTag" />
            <button type="button" @click.prevent="createNewTag">+</button>
        </div>
    </div>
    <div class="form-actions">
      <button type="button" @click="$emit('close')">取消</button>
      <button type="submit" class="primary">{{ props.todoToEdit ? '更新任务' : '添加任务' }}</button>
    </div>
  </form>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useTodosStore } from '../stores/todos';

const props = defineProps({
  todoToEdit: {
    type: Object,
    default: null,
  },
});
const emit = defineEmits(['close']);

const todosStore = useTodosStore();

const form = ref({
  title: '',
  description: '',
  due_date: null,
  tags: [],
});
const newTagName = ref('');

// 监听编辑对象变化，填充表单
watch(() => props.todoToEdit, (newVal) => {
    if (newVal) {
        form.value = {
            title: newVal.title,
            description: newVal.description || '',
            due_date: newVal.due_date,
            tags: newVal.tags.map(t => t.id),
        };
    } else {
        // 重置表单
        form.value = { title: '', description: '', due_date: null, tags: [] };
    }
}, { immediate: true });

const createNewTag = async () => {
    if (newTagName.value.trim()) {
        await todosStore.addTag(newTagName.value.trim());
        const newTag = todosStore.tags.find(t => t.name === newTagName.value.trim());
        if (newTag && !form.value.tags.includes(newTag.id)) {
            form.value.tags.push(newTag.id);
        }
        newTagName.value = '';
    }
};

const handleSubmit = () => {
  // 过滤掉空的 due_date
  const payload = { ...form.value };
  if (!payload.due_date) {
    delete payload.due_date;
  }

  if (props.todoToEdit) {
    todosStore.updateTodo(props.todoToEdit.id, payload);
  } else {
    todosStore.addTodo(payload);
  }
  emit('close');
};
</script>

<style scoped>
.todo-form {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}
.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}
.tag-selector {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
}
.tag-selector label {
    display: flex;
    align-items: center;
    gap: 0.3rem;
    cursor: pointer;
}
.new-tag-creator {
    display: flex;
    gap: 0.5rem;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
}
</style>