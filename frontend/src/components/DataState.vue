<script setup lang="ts">
defineProps<{ loading?: boolean; error?: string; empty?: boolean; emptyText?: string }>();
</script>

<template>
  <div v-if="loading" class="state-box">正在加载数据…</div>
  <div v-else-if="error" class="state-box state-error">{{ error }}</div>
  <div v-else-if="empty" class="state-box">{{ emptyText || '暂无数据' }}</div>
  <slot v-else />
</template>
