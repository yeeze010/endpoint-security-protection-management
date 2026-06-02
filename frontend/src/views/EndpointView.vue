<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { EndpointAsset, request } from '../api';
import DataState from '../components/DataState.vue';
import RiskBadge from '../components/RiskBadge.vue';

const endpoints = ref<EndpointAsset[]>([]);
const keyword = ref('');
const loading = ref(true);
const error = ref('');

const filtered = computed(() => {
  const key = keyword.value.trim().toLowerCase();
  if (!key) return endpoints.value;
  return endpoints.value.filter((item) =>
    [item.hostname, item.ip, item.department, item.owner].some((value) => value.toLowerCase().includes(key))
  );
});

onMounted(async () => {
  try {
    endpoints.value = await request<EndpointAsset[]>('/api/endpoints');
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
        <h2>终端资产</h2>
        <p>统一查看 Agent 状态、风险评分和最近在线时间。</p>
      </div>
      <button class="primary-button">批量下发策略</button>
    </div>

    <div class="toolbar">
      <label>
        搜索终端
        <input v-model="keyword" type="search" placeholder="主机名 / IP / 部门 / 负责人" />
      </label>
    </div>

    <DataState :loading="loading" :error="error" :empty="filtered.length === 0">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>主机名</th>
              <th>IP</th>
              <th>系统</th>
              <th>部门</th>
              <th>负责人</th>
              <th>Agent</th>
              <th>在线状态</th>
              <th>风险</th>
              <th>评分</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in filtered" :key="item.id">
              <td>{{ item.hostname }}</td>
              <td>{{ item.ip }}</td>
              <td>{{ item.os }}</td>
              <td>{{ item.department }}</td>
              <td>{{ item.owner }}</td>
              <td>{{ item.agentVersion }}</td>
              <td>{{ item.onlineStatus }}</td>
              <td><RiskBadge :value="item.riskLevel" /></td>
              <td>{{ item.riskScore }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </DataState>
  </section>
</template>
