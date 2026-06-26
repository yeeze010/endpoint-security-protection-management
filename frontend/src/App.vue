<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { RouterLink, RouterView, useRoute } from 'vue-router';
import { alerts, endpoints, initialPolicies } from './data';

const route = useRoute();
const navOpen = ref(false);

const pageTitle = computed(() => String(route.meta.title ?? '安全态势'));
const urgentAlertCount = computed(
  () => alerts.filter((item) => item.severity === '严重' || item.severity === '高').length
);
const onlineRate = computed(() => {
  const online = endpoints.filter((item) => item.onlineStatus === '在线').length;
  return `${Math.round((online / endpoints.length) * 1000) / 10}%`;
});
const publishedPolicies = computed(
  () => initialPolicies.filter((item) => item.status === '已发布').length
);
const activeEndpoints = computed(() => endpoints.filter((item) => item.onlineStatus === '在线').length);

const navGroups = [
  {
    label: '运营监测',
    items: [
      { path: '/dashboard', label: '态势总览', note: '风险、覆盖率、闭环进度' },
      { path: '/endpoints', label: '终端资产', note: '在线状态、补丁、白名单' },
      { path: '/alerts', label: '告警闭环', note: '研判、处置、复核' }
    ]
  },
  {
    label: '防护控制',
    items: [
      { path: '/policies', label: '策略下发', note: '审批、灰度、发布、回滚' },
      { path: '/controls', label: '控制中心', note: '补丁、防病毒、设备、软件' },
      { path: '/reports', label: '报表中心', note: '指标、导出、证据归档' }
    ]
  },
  {
    label: '验收治理',
    items: [
      { path: '/acceptance', label: '验收中心', note: '证据、缺口、交付材料' },
      { path: '/audit', label: '审计日志', note: '关键动作追踪与导出' }
    ]
  }
];

const commandStats = computed(() => [
  { label: '在线终端', value: `${activeEndpoints.value}/${endpoints.length}`, helper: '当前联机设备' },
  { label: '高危告警', value: String(urgentAlertCount.value), helper: '含严重与高风险' },
  { label: '已发布策略', value: String(publishedPolicies.value), helper: '等待持续观察' },
  { label: '在线率', value: onlineRate.value, helper: '跨 Windows、macOS、Linux' }
]);

watch(
  () => route.fullPath,
  () => {
    navOpen.value = false;
  }
);
</script>

<template>
  <a class="skip-link" href="#main-content">跳转到主内容</a>
  <div class="app-shell">
    <div v-if="navOpen" class="nav-scrim" @click="navOpen = false"></div>

    <aside class="sidebar" :class="{ open: navOpen }" aria-label="主导航">
      <div class="sidebar-head">
        <div class="brand">
          <div class="brand-mark">ES</div>
          <div class="brand-copy">
            <strong>终端安全防护管理平台</strong>
            <span>Endpoint Security Operations Console</span>
          </div>
        </div>
        <button class="nav-close" type="button" @click="navOpen = false">关闭导航</button>
      </div>

      <div class="status-card">
        <div class="status-card-top">
          <span class="status-pill">策略基线正常</span>
          <strong>{{ onlineRate }}</strong>
        </div>
        <p>当前风险集中在研发和运维域，建议先收敛高危告警再推进补丁窗口。</p>
        <dl>
          <div>
            <dt>严重 / 高风险告警</dt>
            <dd>{{ urgentAlertCount }}</dd>
          </div>
          <div>
            <dt>已发布策略</dt>
            <dd>{{ publishedPolicies }}</dd>
          </div>
        </dl>
      </div>

      <nav class="nav-groups">
        <section v-for="group in navGroups" :key="group.label" class="nav-group">
          <p>{{ group.label }}</p>
          <RouterLink
            v-for="item in group.items"
            :key="item.path"
            :to="item.path"
            :aria-current="route.path === item.path ? 'page' : undefined"
            :class="{
              active:
                route.path === item.path ||
                (item.path === '/endpoints' && route.path.startsWith('/endpoints/'))
            }"
          >
            <strong>{{ item.label }}</strong>
            <span>{{ item.note }}</span>
          </RouterLink>
        </section>
      </nav>

      <footer class="sidebar-footer">
        <span>当前策略基线</span>
        <strong>Baseline v12 · 2026-06-13</strong>
      </footer>
    </aside>

    <main id="main-content" class="main">
      <header class="topbar">
        <div class="topbar-main">
          <button class="nav-toggle" type="button" @click="navOpen = !navOpen" aria-label="切换导航">
            导航
          </button>
          <div class="topbar-copy">
            <p>终端安全运营与验收工作台</p>
            <h1>{{ pageTitle }}</h1>
          </div>
          <div class="topbar-brief">
            <span class="status-pill">优先级 P1</span>
            <strong>先清告警，再做验收</strong>
          </div>
        </div>

        <div class="topbar-stats-grid">
          <article v-for="item in commandStats" :key="item.label">
            <span>{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
            <small>{{ item.helper }}</small>
          </article>
        </div>
      </header>

      <RouterView />
    </main>
  </div>
</template>
