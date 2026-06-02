<script setup lang="ts">
import { onMounted, ref } from 'vue';
import { DashboardOverview, request } from '../api';
import DataState from '../components/DataState.vue';

const data = ref<DashboardOverview>();
const loading = ref(true);
const error = ref('');

onMounted(async () => {
  try {
    data.value = await request<DashboardOverview>('/api/dashboard/overview');
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
        <h2>安全态势总览</h2>
        <p>查看终端风险、告警趋势和补丁合规情况。</p>
      </div>
      <button class="primary-button">导出日报</button>
    </div>

    <DataState :loading="loading" :error="error">
      <div class="metric-grid">
        <article v-for="metric in data?.metrics" :key="metric.label" class="metric-card" :class="metric.tone">
          <span>{{ metric.label }}</span>
          <strong>{{ metric.value }}</strong>
          <small>{{ metric.helper }}</small>
        </article>
      </div>

      <div class="panel-grid">
        <section class="panel">
          <h3>近 7 日告警趋势</h3>
          <div class="bar-chart">
            <div v-for="point in data?.alertTrend" :key="point.date" class="bar-item">
              <div class="bar-track">
                <span class="bar" :style="{ height: `${point.alerts * 2}px` }"></span>
              </div>
              <small>{{ point.date }}</small>
            </div>
          </div>
        </section>

        <section class="panel">
          <h3>风险分布</h3>
          <ul class="risk-list">
            <li v-for="risk in data?.riskDistribution" :key="risk.level">
              <span>{{ risk.level }}</span>
              <strong>{{ risk.count }}</strong>
            </li>
          </ul>
        </section>
      </div>
    </DataState>
  </section>
</template>
