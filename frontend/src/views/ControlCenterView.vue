<script setup lang="ts">
import { ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import { endpoints } from '../data';

const activeTab = ref('防病毒');
const notice = ref('');

const controls = [
  { name: '防病毒', value: '98.1%', helper: '防护启用率', issue: '24 台病毒库过期' },
  { name: '补丁管理', value: '87.3%', helper: '补丁合规率', issue: '129 台存在高危缺失' },
  { name: '外设管控', value: '100%', helper: '违规阻断率', issue: '今日阻断 18 次' },
  { name: '软件白名单', value: '91.5%', helper: '软件合规率', issue: '42 个例外待复核' }
];

function createTask(name: string) {
  notice.value = `已创建“${name}”批量任务，目标范围为全部不合规终端。`;
}
</script>

<template>
  <section class="page">
    <PageHeader
      code="SEC-04"
      title="控制中心"
      description="统一查看防病毒、补丁、外设和软件白名单状态，并批量创建整改任务。"
    />

    <div v-if="notice" class="notice">
      {{ notice }}
      <button @click="notice = ''">关闭</button>
    </div>

    <div class="control-metrics">
      <button v-for="item in controls" :key="item.name" :class="{ active: activeTab === item.name }" @click="activeTab = item.name">
        <span>{{ item.name }}</span>
        <strong>{{ item.value }}</strong>
        <small>{{ item.helper }}</small>
        <em>{{ item.issue }}</em>
      </button>
    </div>

    <section class="panel">
      <div class="panel-title">
        <div>
          <span class="section-code">TASK BOARD</span>
          <h3>{{ activeTab }}异常终端</h3>
          <p>根据当前策略基线筛选需要优先整改的终端。</p>
        </div>
        <button class="button primary" @click="createTask(`${activeTab}整改`)">创建批量整改任务</button>
      </div>

      <div class="stack-list">
        <article v-for="endpoint in endpoints.filter((item) => item.riskScore >= 58)" :key="endpoint.id" class="stack-card">
          <div class="stack-card-top">
            <div>
              <RouterLink :to="`/endpoints/${endpoint.id}`">{{ endpoint.hostname }}</RouterLink>
              <p>{{ endpoint.department }} · {{ endpoint.owner }}</p>
            </div>
            <strong class="risk-score">{{ endpoint.riskScore }}</strong>
          </div>

          <p class="stack-copy">
            {{
              activeTab === '防病毒'
                ? endpoint.antivirusStatus
                : activeTab === '补丁管理'
                  ? endpoint.patchStatus
                  : activeTab === '外设管控'
                    ? endpoint.deviceControl
                    : endpoint.whitelistStatus
            }}
          </p>

          <button class="link-button" @click="createTask(`${endpoint.hostname} ${activeTab}整改`)">
            创建单机任务
          </button>
        </article>
      </div>
    </section>
  </section>
</template>
