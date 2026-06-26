<script setup lang="ts">
import { ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import RiskBadge from '../components/RiskBadge.vue';
import { alerts as source, type AlertStatus, type SecurityAlert } from '../data';

const alerts = ref<SecurityAlert[]>(structuredClone(source));
const selected = ref<SecurityAlert | null>(alerts.value[0]);
const notice = ref('');
const disposition = ref({
  owner: alerts.value[0]?.owner ?? 'SOC 值班组',
  action: '临时网络隔离',
  note: '先隔离，再拉取终端取证和白名单差异。'
});

const nextStatus: Record<AlertStatus, AlertStatus | undefined> = {
  待研判: '已派单',
  已派单: '处置中',
  处置中: '待复核',
  待复核: '已关闭',
  已关闭: undefined
};

function advance(alert: SecurityAlert) {
  const target = nextStatus[alert.status];
  if (!target) {
    return;
  }

  alert.status = target;
  alert.owner = disposition.value.owner;
  alert.timeline.push(`责任人更新为：${disposition.value.owner}`);
  alert.timeline.push(`处置动作：${disposition.value.action}`);
  alert.timeline.push(`状态变更为：${target}`);
  notice.value = `告警 ${alert.id} 已推进到“${target}”。`;
}

function saveDisposition() {
  if (!selected.value) {
    return;
  }

  selected.value.owner = disposition.value.owner;
  selected.value.timeline.push(`处置备注：${disposition.value.note}`);
  notice.value = `已为 ${selected.value.id} 更新处置记录。`;
}
</script>

<template>
  <section class="page">
    <PageHeader
      code="SEC-05"
      title="告警处置闭环"
      description="完成告警研判、派单、处置、复核和关闭，并保留证据、责任人和审计记录。"
    />

    <div v-if="notice" class="notice">
      {{ notice }}
      <button @click="notice = ''">关闭</button>
    </div>

    <div class="split-layout">
      <div class="alert-list">
        <button
          v-for="alert in alerts"
          :key="alert.id"
          :class="{ active: selected?.id === alert.id }"
          @click="
            selected = alert;
            disposition.owner = alert.owner;
          "
        >
          <div>
            <RiskBadge :value="alert.severity" />
            <span>{{ alert.status }}</span>
          </div>
          <strong>{{ alert.title }}</strong>
          <small>{{ alert.endpoint }} · {{ alert.createdAt }}</small>
          <em>{{ alert.sla }}</em>
        </button>
      </div>

      <section v-if="selected" class="panel alert-detail">
        <div class="panel-title">
          <div>
            <span class="section-code">ALERT DETAIL</span>
            <h3>{{ selected.title }}</h3>
            <p>{{ selected.endpoint }} · {{ selected.owner }} · {{ selected.createdAt }}</p>
          </div>
          <button class="button primary" :disabled="!nextStatus[selected.status]" @click="advance(selected)">
            {{ nextStatus[selected.status] ? `推进到 ${nextStatus[selected.status]}` : '已关闭' }}
          </button>
        </div>

        <dl class="status-details">
          <div><dt>当前状态</dt><dd>{{ selected.status }}</dd></div>
          <div><dt>SLA</dt><dd>{{ selected.sla }}</dd></div>
          <div><dt>证据附件</dt><dd>{{ selected.evidence }}</dd></div>
          <div><dt>责任人</dt><dd>{{ selected.owner }}</dd></div>
        </dl>

        <form class="form-grid" @submit.prevent="saveDisposition">
          <label>
            当前责任人
            <input v-model="disposition.owner" type="text" />
          </label>
          <label>
            当前动作
            <select v-model="disposition.action">
              <option>临时网络隔离</option>
              <option>补丁修复</option>
              <option>白名单复核</option>
              <option>终端取证</option>
            </select>
          </label>
          <label class="form-span-2">
            处置说明
            <textarea v-model="disposition.note" rows="4"></textarea>
          </label>
          <div class="form-actions form-span-2">
            <button type="submit" class="button secondary">保存处置记录</button>
          </div>
        </form>

        <h4>处置时间线</h4>
        <ol class="timeline">
          <li v-for="(line, index) in selected.timeline" :key="`${selected.id}-${index}`">
            <b>{{ index + 1 }}</b>
            <span>{{ line }}</span>
          </li>
        </ol>
      </section>
    </div>
  </section>
</template>
