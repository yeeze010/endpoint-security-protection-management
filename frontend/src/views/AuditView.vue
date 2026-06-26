<script setup lang="ts">
import PageHeader from '../components/PageHeader.vue';
import { auditLogs } from '../data';
</script>

<template>
  <section class="page">
    <PageHeader
      code="SEC-08"
      title="审计日志"
      description="追踪策略、告警、报表、权限和终端处置动作。"
    >
      <button class="button secondary">导出日志</button>
    </PageHeader>

    <div class="audit-list">
      <article v-for="log in auditLogs" :key="`${log.time}-${log.actor}-${log.target}`">
        <time>{{ log.time }}</time>
        <div>
          <strong>{{ log.actor }} · {{ log.action }}</strong>
          <span>{{ log.target }}</span>
        </div>
        <div class="audit-result">{{ log.result }}</div>
      </article>
    </div>
  </section>
</template>
