<script setup lang="ts">
import { computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import RiskBadge from '../components/RiskBadge.vue';
import { alerts, endpoints } from '../data';

const route = useRoute();
const actionResult = ref('');

const endpoint = computed(
  () => endpoints.find((item) => item.id === route.params.id) ?? endpoints[0]
);
const relatedAlerts = computed(() =>
  alerts.filter((item) => item.endpointId === endpoint.value.id)
);

function run(action: string) {
  actionResult.value = `已创建“${action}”任务，等待 Agent ${endpoint.value.onlineStatus === '在线' ? '执行' : '上线后执行'}。`;
}
</script>

<template>
  <section class="page">
    <div class="page-header">
      <div>
        <RouterLink to="/endpoints" class="back-link">返回终端资产</RouterLink>
        <h2>{{ endpoint.hostname }}</h2>
        <p>{{ endpoint.ip }} · {{ endpoint.os }} · {{ endpoint.department }} · {{ endpoint.owner }}</p>
      </div>
      <div class="action-row">
        <button class="button secondary" @click="run('策略同步')">同步策略</button>
        <button class="button danger" @click="run('网络隔离')">网络隔离</button>
      </div>
    </div>

    <div v-if="actionResult" class="notice">
      {{ actionResult }}
      <button @click="actionResult = ''">关闭</button>
    </div>

    <div class="detail-summary">
      <article>
        <span>风险评分</span>
        <strong>{{ endpoint.riskScore }}</strong>
        <RiskBadge :value="endpoint.riskLevel" />
      </article>
      <article>
        <span>Agent 状态</span>
        <strong>{{ endpoint.onlineStatus }}</strong>
        <small>{{ endpoint.agentVersion }} · {{ endpoint.lastSeen }}</small>
      </article>
      <article>
        <span>当前策略</span>
        <strong>{{ endpoint.policyVersion }}</strong>
        <small>策略同步状态正常</small>
      </article>
      <article>
        <span>未关闭告警</span>
        <strong>{{ endpoint.openAlerts }}</strong>
        <small>优先处理高危告警</small>
      </article>
    </div>

    <div class="content-grid">
      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">SECURE STATE</span>
            <h3>安全状态</h3>
            <p>最近一次 Agent 上报结果。</p>
          </div>
        </div>
        <dl class="status-details">
          <div><dt>防病毒</dt><dd>{{ endpoint.antivirusStatus }}</dd></div>
          <div><dt>补丁</dt><dd>{{ endpoint.patchStatus }}</dd></div>
          <div><dt>外设管控</dt><dd>{{ endpoint.deviceControl }}</dd></div>
          <div><dt>软件白名单</dt><dd>{{ endpoint.whitelistStatus }}</dd></div>
        </dl>
      </section>

      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">RISK FACTORS</span>
            <h3>风险因子</h3>
            <p>驱动当前评分的主要因素。</p>
          </div>
        </div>
        <div class="factor-grid">
          <button @click="run('补丁修复')">
            <strong>{{ endpoint.missingPatches }}</strong>
            <span>缺少补丁</span>
          </button>
          <button @click="run('外设事件复核')">
            <strong>{{ endpoint.blockedDevices }}</strong>
            <span>外设阻断</span>
          </button>
          <button @click="run('白名单复核')">
            <strong>{{ endpoint.unauthorizedApps }}</strong>
            <span>未授权软件</span>
          </button>
          <button @click="run('告警复核')">
            <strong>{{ endpoint.openAlerts }}</strong>
            <span>未关闭告警</span>
          </button>
        </div>
      </section>
    </div>

    <div class="content-grid">
      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">ASSET BASELINE</span>
            <h3>资产与通信信息</h3>
            <p>终端基线和通信环境。</p>
          </div>
        </div>
        <dl class="asset-grid">
          <div><dt>处理器</dt><dd>{{ endpoint.cpu }}</dd></div>
          <div><dt>内存</dt><dd>{{ endpoint.memory }}</dd></div>
          <div><dt>磁盘</dt><dd>{{ endpoint.disk }}</dd></div>
          <div><dt>操作系统</dt><dd>{{ endpoint.os }}</dd></div>
          <div><dt>Agent 版本</dt><dd>{{ endpoint.agentVersion }}</dd></div>
          <div><dt>最近心跳</dt><dd>{{ endpoint.lastSeen }}</dd></div>
        </dl>
      </section>

      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">RELATED ALERTS</span>
            <h3>关联告警</h3>
            <p>该终端当前未结清的风险动作。</p>
          </div>
        </div>
        <ul class="compact-list">
          <li v-for="alert in relatedAlerts" :key="alert.id">
            <span>{{ alert.title }}</span>
            <strong>{{ alert.status }}</strong>
            <em :class="`status-${alert.severity === '严重' || alert.severity === '高' ? '未达标' : '关注'}`">
              {{ alert.sla }}
            </em>
          </li>
        </ul>
      </section>
    </div>
  </section>
</template>
