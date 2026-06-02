<script setup lang="ts">
defineProps<{
  loading?: boolean;
  error?: string;
  empty?: boolean;
}>();
</script>

<template>
  <div v-if="loading" class="state">正在加载数据...</div>
  <div v-else-if="error" class="state error">{{ error }}</div>
  <div v-else-if="empty" class="state">暂无数据</div>
  <slot v-else />
</template>
