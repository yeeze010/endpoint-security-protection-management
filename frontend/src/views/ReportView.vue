<script setup lang="ts">
import { computed, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import { endpoints, reportMetrics, reportPackages as initialPackages } from '../data';

const notice = ref('');
const packages = ref(structuredClone(initialPackages));
const form = ref({
  name: '高危告警处置报告',
  scope: '研发部与运维部',
  owner: 'SOC 值班组',
  includeEvidence: true,
  retention: '30 天'
});

const departmentScores = computed(() =>
  endpoints.map((item) => ({
    department: item.department,
    score: item.riskScore
  }))
);

function exportReport() {
  const status = form.value.includeEvidence ? '生成中' : '待生成';
  packages.value.unshift({
    id: `RP-${Date.now()}`,
    name: form.value.name,
    scope: form.value.scope,
    owner: form.value.owner,
    status,
    updatedAt: '刚刚'
  });
  notice.value = `已创建“${form.value.name}”导出任务，归档保留 ${form.value.retention}。`;
}
</script>

<template>
  <section class="page">
    <PageHeader
      code="SEC-06"
      title="报表中心"
      description="查看资产、补丁、防病毒、外设、白名单和告警治理指标，并把导出任务、留存周期和证据包一起收口。"
      action="创建导出任务"
      @action="exportReport"
    />

    <div v-if="notice" class="notice">
      {{ notice }}
      <button @click="notice = ''">关闭</button>
    </div>

    <div class="report-grid">
      <article v-for="metric in reportMetrics" :key="metric.label">
        <div>
          <span>{{ metric.label }}</span>
          <em :class="`status-${metric.status}`">{{ metric.status }}</em>
        </div>
        <strong>{{ metric.value }}</strong>
        <small>验收目标 {{ metric.target }}</small>
        <div class="track"><i :style="{ width: metric.value }"></i></div>
      </article>
    </div>

    <div class="content-grid wide-left">
      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">EXPORT WORKBENCH</span>
            <h3>生成报表与证据包</h3>
            <p>通过统一表单提交报表名称、范围、责任人和归档策略，避免验收材料散落。</p>
          </div>
        </div>

        <form class="form-grid" @submit.prevent="exportReport">
          <label>
            报表名称
            <input v-model="form.name" type="text" placeholder="例如：终端合规周报" />
          </label>
          <label>
            归属范围
            <input v-model="form.scope" type="text" placeholder="例如：总部与研发部" />
          </label>
          <label>
            责任人
            <input v-model="form.owner" type="text" placeholder="例如：SOC 值班组" />
          </label>
          <label>
            保留周期
            <select v-model="form.retention">
              <option>7 天</option>
              <option>30 天</option>
              <option>90 天</option>
            </select>
          </label>
          <label class="form-span-2 checkbox-row">
            <input v-model="form.includeEvidence" type="checkbox" />
            <span>同时打包证据附件与审计日志</span>
          </label>
          <div class="form-actions form-span-2">
            <button type="submit" class="button primary">提交导出任务</button>
          </div>
        </form>
      </section>

      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">RISK VIEW</span>
            <h3>部门风险对比</h3>
            <p>按终端风险评分展示当前暴露面。</p>
          </div>
        </div>
        <div class="department-chart">
          <div v-for="item in departmentScores" :key="`${item.department}-${item.score}`">
            <span>{{ item.department }}</span>
            <div class="track"><i :style="{ width: `${item.score}%` }"></i></div>
            <strong>{{ item.score }}</strong>
          </div>
        </div>
      </section>
    </div>

    <section class="panel">
      <div class="panel-title">
        <div>
          <span class="section-code">ARCHIVE QUEUE</span>
          <h3>报表文件与归档状态</h3>
          <p>导出任务和证据文件保留规则统一展示，便于验收点交。</p>
        </div>
      </div>

      <div class="stack-list">
        <article v-for="item in packages" :key="item.id" class="stack-card">
          <div class="stack-card-top">
            <div>
              <strong>{{ item.name }}</strong>
              <p>{{ item.scope }}</p>
            </div>
            <span class="badge neutral">{{ item.status }}</span>
          </div>
          <p class="stack-copy">责任人：{{ item.owner }} · 更新时间：{{ item.updatedAt }}</p>
        </article>
      </div>
    </section>
  </section>
</template>
