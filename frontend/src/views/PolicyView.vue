<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { Policy, request } from '../api';
import DataState from '../components/DataState.vue';

const policies = ref<Policy[]>([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    policies.value = await request<Policy[]>('/api/policies');
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
        <h2>策略中心</h2>
        <p>管理防病毒、外设、补丁、隔离等安全策略。</p>
      </div>
      <button class="primary-button">新建策略</button>
    </div>

    <DataState :loading="loading" :error="error" :empty="policies.length === 0">
      <div class="policy-grid">
        <article v-for="policy in policies" :key="policy.id" class="policy-card">
          <div>
            <span class="badge neutral">{{ policy.type }}</span>
            <span class="badge">{{ policy.status }}</span>
          </div>
          <h3>{{ policy.name }}</h3>
          <p>目标范围：{{ policy.targetScope }}</p>
          <footer>
            <span>优先级 {{ policy.priority }}</span>
            <strong>{{ policy.version }}</strong>
          </footer>
        </article>
      </div>
    </DataState>
  </section>
</template>
