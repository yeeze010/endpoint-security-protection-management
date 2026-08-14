<script setup lang="ts">
import { computed, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import RiskBadge from '../components/RiskBadge.vue';
import { endpoints } from '../data';

const keyword = ref('');
const risk = ref<'全部' | '严重' | '高' | '中' | '低'>('全部');
const selected = ref<string[]>([]);
const notice = ref('');

const filtered = computed(() =>
  endpoints.filter((item) => {
    const key = keyword.value.trim().toLowerCase();
    const matchedText =
      !key ||
      [item.hostname, item.ip, item.department, item.owner].some((value) =>
        value.toLowerCase().includes(key)
      );
    const matchedRisk = risk.value === '全部' || item.riskLevel === risk.value;
    return matchedText && matchedRisk;
  })
);

function runBatch(action: string) {
  notice.value = `已为 ${selected.value.length} 台终端创建“${action}”任务。`;
}
</script>

<template>
  <section class="page">
    <PageHeader
      code="SEC-02"
      title="终端资产"
      description="管理终端身份、Agent 通信、防病毒、补丁、外设和软件合规状态。"
    >
      <button class="button primary" @click="notice = '已生成 Agent 部署令牌，有效期 24 小时。'">
        部署 Agent
      </button>
    </PageHeader>

    <div v-if="notice" class="notice">
      {{ notice }}
      <button @click="notice = ''">关闭</button>
    </div>

    <div class="filter-bar">
      <label>
        搜索终端
        <input v-model="keyword" type="search" placeholder="主机名 / IP / 部门 / 负责人" />
      </label>
      <label>
        风险等级
        <select v-model="risk">
          <option>全部</option>
          <option>严重</option>
          <option>高</option>
          <option>中</option>
          <option>低</option>
        </select>
      </label>
      <div class="batch-actions">
        <span>已选 {{ selected.length }} 台</span>
        <button :disabled="!selected.length" @click="runBatch('策略同步')">同步策略</button>
        <button :disabled="!selected.length" @click="runBatch('病毒扫描')">病毒扫描</button>
      </div>
    </div>

    <div class="asset-card-grid">
      <article v-for="item in filtered" :key="item.id" class="asset-card">
        <div class="asset-card-top">
          <label class="checkbox">
            <input v-model="selected" type="checkbox" :value="item.id" :aria-label="`选择 ${item.hostname}`" />
            <span>加入批量任务</span>
          </label>
          <RiskBadge :value="item.riskLevel" />
        </div>

        <div class="asset-card-title">
          <RouterLink :to="`/endpoints/${item.id}`">{{ item.hostname }}</RouterLink>
          <p>{{ item.ip }} · {{ item.department }} · {{ item.owner }}</p>
        </div>

        <dl class="asset-meta">
          <div>
            <dt>Agent</dt>
            <dd>{{ item.agentVersion }} · {{ item.onlineStatus }}</dd>
          </div>
          <div>
            <dt>当前策略</dt>
            <dd>{{ item.policyVersion }}</dd>
          </div>
          <div>
            <dt>防病毒</dt>
            <dd>{{ item.antivirusStatus }}</dd>
          </div>
          <div>
            <dt>补丁</dt>
            <dd>{{ item.patchStatus }}</dd>
          </div>
          <div>
            <dt>外设 / 白名单</dt>
            <dd>{{ item.deviceControl }}；{{ item.whitelistStatus }}</dd>
          </div>
        </dl>

        <div class="asset-card-footer">
          <div>
            <span>风险评分</span>
            <strong>{{ item.riskScore }}</strong>
          </div>
          <small>最近心跳 {{ item.lastSeen }}</small>
        </div>
      </article>
    </div>
  </section>
</template>
