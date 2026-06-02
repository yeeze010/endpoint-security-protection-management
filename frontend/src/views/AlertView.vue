<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { request, SecurityAlert } from '../api';
import DataState from '../components/DataState.vue';
import RiskBadge from '../components/RiskBadge.vue';

const alerts = ref<SecurityAlert[]>([]);
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    alerts.value = await request<SecurityAlert[]>('/api/alerts');
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
        <h2>告警处置</h2>
        <p>完成告警发现、研判、派单、处置、关闭闭环。</p>
      </div>
      <button class="primary-button">创建工单</button>
    </div>

    <DataState :loading="loading" :error="error" :empty="alerts.length === 0">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>告警标题</th>
              <th>终端</th>
              <th>等级</th>
              <th>状态</th>
              <th>处理人</th>
              <th>最近发现</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="alert in alerts" :key="alert.id">
              <td>{{ alert.title }}</td>
              <td>{{ alert.endpoint }}</td>
              <td><RiskBadge :value="alert.severity" /></td>
              <td>{{ alert.status }}</td>
              <td>{{ alert.assignee }}</td>
              <td>{{ new Date(alert.lastSeenAt).toLocaleString() }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </DataState>
  </section>
</template>
