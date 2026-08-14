<script setup lang="ts">
import { computed } from 'vue';
import { RouterLink } from 'vue-router';
import PageHeader from '../components/PageHeader.vue';
import { acceptanceItems, alerts, endpoints, flowSteps, reportMetrics } from '../data';

const metrics = [
  { label: '纳管终端', value: '1,286', helper: '本周新增 42 台', tone: 'normal' },
  { label: 'Agent 在线率', value: '94.8%', helper: '4 台终端待确认', tone: 'warning' },
  { label: '严重与高危告警', value: '17', helper: '9 条逼近 SLA', tone: 'danger' },
  { label: '综合合规率', value: '89.2%', helper: '距离目标仍差 2.8%', tone: 'warning' }
];

const riskData = [
  { label: '严重', value: 17, percent: 14 },
  { label: '高', value: 129, percent: 38 },
  { label: '中', value: 326, percent: 61 },
  { label: '低', value: 814, percent: 88 }
];

const highestRiskEndpoints = [...endpoints].sort((left, right) => right.riskScore - left.riskScore).slice(0, 3);
const acceptanceSummary = computed(() => ({
  done: acceptanceItems.filter((item) => item.done).length,
  total: acceptanceItems.length,
  blockers: acceptanceItems.filter((item) => !item.done).length
}));
</script>

<template>
  <section class="page">
    <PageHeader
      code="SEC-01"
      eyebrow="总览"
      title="终端安全态势"
      description="集中查看终端风险、Agent 通信、策略执行和告警处置状态，并把构建、验收、整改压到同一工作台。"
    >
      <button class="button secondary">刷新态势</button>
      <RouterLink class="button primary" to="/reports">查看合规报表</RouterLink>
    </PageHeader>

    <div class="hero-grid">
      <section class="panel hero-panel">
        <div class="panel-title">
          <div>
            <span class="section-code">TODAY FOCUS</span>
            <h3>优先处理研发终端异常外联与补丁窗口逾期</h3>
            <p>当前高危告警集中在研发和服务器组，先推进网络隔离复核，再安排补丁维护窗口与外设白名单复审。</p>
          </div>
        </div>
        <div class="hero-actions">
          <RouterLink class="button secondary" to="/alerts">进入告警中心</RouterLink>
          <RouterLink class="button secondary" to="/acceptance">查看验收进度</RouterLink>
        </div>
      </section>

      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">ACCEPTANCE DESK</span>
            <h3>验收推进度</h3>
            <p>构建通过，但仍有 {{ acceptanceSummary.blockers }} 项交付缺口需要在本轮收口。</p>
          </div>
        </div>
        <div class="mini-metrics">
          <article>
            <span>已完成</span>
            <strong>{{ acceptanceSummary.done }}</strong>
          </article>
          <article>
            <span>待收口</span>
            <strong>{{ acceptanceSummary.blockers }}</strong>
          </article>
          <article>
            <span>总项目</span>
            <strong>{{ acceptanceSummary.total }}</strong>
          </article>
        </div>
        <RouterLink class="inline-link" to="/acceptance">前往验收中心</RouterLink>
      </section>
    </div>

    <div class="metric-grid">
      <article v-for="metric in metrics" :key="metric.label" class="metric-card" :class="metric.tone">
        <span>{{ metric.label }}</span>
        <strong>{{ metric.value }}</strong>
        <small>{{ metric.helper }}</small>
      </article>
    </div>

    <div class="content-grid wide-left">
      <section class="panel">
        <div class="panel-title">
          <div>
            <h3>风险终端分布</h3>
            <p>按当前评分模型统计，可直接下钻到高分终端。</p>
          </div>
          <RouterLink to="/endpoints">查看资产</RouterLink>
        </div>
        <div class="risk-bars">
          <div v-for="item in riskData" :key="item.label" class="risk-bar-row">
            <span>{{ item.label }}</span>
            <div class="track"><i :class="`bar-${item.label}`" :style="{ width: `${item.percent}%` }"></i></div>
            <strong>{{ item.value }}</strong>
          </div>
        </div>
        <div class="endpoint-watch">
          <RouterLink v-for="item in highestRiskEndpoints" :key="item.id" :to="`/endpoints/${item.id}`">
            <div>
              <strong>{{ item.hostname }}</strong>
              <span>{{ item.department }} · {{ item.owner }}</span>
            </div>
            <b>{{ item.riskScore }}</b>
          </RouterLink>
        </div>
      </section>

      <section class="panel">
        <div class="panel-title">
          <div>
            <h3>合规指标</h3>
            <p>面向当天验收与巡检的关键结果。</p>
          </div>
        </div>
        <ul class="compact-list">
          <li v-for="item in reportMetrics.slice(0, 4)" :key="item.label">
            <span>{{ item.label }}</span>
            <strong>{{ item.value }}</strong>
            <em :class="`status-${item.status}`">{{ item.status }}</em>
          </li>
        </ul>
      </section>
    </div>

    <div class="content-grid">
      <section class="panel">
        <div class="panel-title">
          <div>
            <h3>安全运营闭环</h3>
            <p>从终端注册到审计归档的最短路径。</p>
          </div>
        </div>
        <ol class="flow-list">
          <li v-for="(step, index) in flowSteps" :key="step">
            <b>{{ index + 1 }}</b>
            <span>{{ step }}</span>
          </li>
        </ol>
      </section>

      <section class="panel">
        <div class="panel-title">
          <div>
            <h3>优先处置告警</h3>
            <p>按严重级别与 SLA 排序，直接驱动闭环。</p>
          </div>
          <RouterLink to="/alerts">进入告警中心</RouterLink>
        </div>
        <div v-for="item in alerts" :key="item.id" class="alert-mini">
          <div>
            <strong>{{ item.title }}</strong>
            <span>{{ item.endpoint }} · {{ item.status }}</span>
          </div>
          <b>{{ item.sla }}</b>
        </div>
      </section>
    </div>
  </section>
</template>
