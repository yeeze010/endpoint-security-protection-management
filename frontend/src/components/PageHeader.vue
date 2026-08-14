<script setup lang="ts">
defineProps<{
  title: string;
  description: string;
  action?: string;
  eyebrow?: string;
  code?: string;
}>();

defineEmits<{ action: [] }>();
</script>

<template>
  <div class="page-header">
    <div class="page-header-copy">
      <div class="page-header-meta">
        <span v-if="code" class="section-code">{{ code }}</span>
        <span class="eyebrow">{{ eyebrow ?? '业务工作台' }}</span>
      </div>
      <h2>{{ title }}</h2>
      <p>{{ description }}</p>
    </div>
    <div class="page-header-actions">
      <button v-if="action" class="button primary" @click="$emit('action')">{{ action }}</button>
      <slot />
    </div>
  </div>
</template>
