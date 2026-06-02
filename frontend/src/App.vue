<script setup lang="ts">
import { RouterLink, RouterView, useRoute } from 'vue-router';

const route = useRoute();
const navItems = [
  { path: '/dashboard', label: '安全态势' },
  { path: '/endpoints', label: '终端资产' },
  { path: '/policies', label: '策略中心' },
  { path: '/alerts', label: '告警处置' },
  { path: '/audit', label: '审计日志' }
];
</script>

<template>
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">ES</div>
        <div>
          <strong>终端安全</strong>
          <span>防护管理平台</span>
        </div>
      </div>
      <nav class="nav" aria-label="主导航">
        <RouterLink
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          :class="{ active: route.path === item.path }"
        >
          {{ item.label }}
        </RouterLink>
      </nav>
    </aside>

    <main class="main">
      <header class="topbar">
        <div>
          <p class="eyebrow">企业终端安全运营</p>
          <h1>终端安全防护管理平台</h1>
        </div>
        <div class="operator">
          <span class="status-dot"></span>
          安全管理员
        </div>
      </header>
      <RouterView />
    </main>
  </div>
</template>
