<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { AuditLog, request } from '../api';
import DataState from '../components/DataState.vue';

const logs = ref<AuditLog[]>([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    logs.value = await request<AuditLog[]>('/api/audit-logs');
  } catch (err) {
    error.value = err instanceof Error ? err.message : '加载失败';
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <section class="page">
    <div class="page-title">
      <div>
        <h2>审计日志</h2>
        <p>追踪登录、策略、处置、导出和系统配置操作。</p>
      </div>
      <button class="secondary-button">导出审计日志</button>
    </div>

    <DataState :loading="loading" :error="error" :empty="logs.length === 0">
      <div class="timeline">
        <article v-for="log in logs" :key="log.id" class="timeline-item">
          <time>{{ new Date(log.createdAt).toLocaleString() }}</time>
          <strong>{{ log.actor }} {{ log.action }}</strong>
          <span>{{ log.resource }} · {{ log.ip }}</span>
        </article>
      </div>
    </DataState>
  </section>
</template>
