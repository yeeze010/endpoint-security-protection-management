<script setup lang="ts">
import { computed, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import { initialPolicies, type PolicyStatus, type SecurityPolicy } from '../data';

const policies = ref<SecurityPolicy[]>(structuredClone(initialPolicies));
const showForm = ref(false);
const notice = ref('');
const form = ref({
  name: '',
  type: '防病毒',
  scope: '全公司终端',
  priority: 50
});

const progress: Record<PolicyStatus, PolicyStatus | undefined> = {
  草稿: '待审批',
  待审批: '已批准',
  已批准: '灰度中',
  灰度中: '已发布',
  已发布: '已回滚',
  已回滚: undefined
};

const nextLabel = (status: PolicyStatus) =>
  ({
    草稿: '提交审批',
    待审批: '批准',
    已批准: '开始灰度',
    灰度中: '全量发布',
    已发布: '执行回滚',
    已回滚: '流程结束'
  })[status];

function createPolicy() {
  if (!form.value.name.trim()) {
    notice.value = '请输入策略名称。';
    return;
  }

  policies.value.unshift({
    id: `pol-${Date.now()}`,
    name: form.value.name,
    type: form.value.type,
    status: '草稿',
    targetScope: form.value.scope,
    priority: form.value.priority,
    version: 'v1',
    owner: '当前用户',
    rollout: 0,
    lastAction: '刚刚创建草稿'
  });

  showForm.value = false;
  notice.value = '策略草稿已创建。';
  form.value = {
    name: '',
    type: '防病毒',
    scope: '全公司终端',
    priority: 50
  };
}

function advancePolicy(policy: SecurityPolicy) {
  const next = progress[policy.status];
  if (!next) {
    return;
  }

  const action = nextLabel(policy.status);
  policy.status = next;
  policy.rollout = next === '灰度中' ? 20 : next === '已发布' ? 100 : 0;
  policy.lastAction = `刚刚执行：${action}`;
  notice.value = `${policy.name} 已进入“${next}”状态。`;
}

const publishedCount = computed(() => policies.value.filter((item) => item.status === '已发布').length);
</script>

<template>
  <section class="page">
    <PageHeader
      code="SEC-03"
      title="策略下发中心"
      :description="`管理策略版本、审批、灰度发布与回滚，当前已发布 ${publishedCount} 条策略。`"
      action="新建策略"
      @action="showForm = true"
    />

    <div v-if="notice" class="notice">
      {{ notice }}
      <button @click="notice = ''">关闭</button>
    </div>

    <div class="policy-workflow">
      <span v-for="step in ['草稿', '待审批', '已批准', '灰度中', '已发布', '已回滚']" :key="step">
        {{ step }}
      </span>
    </div>

    <div class="policy-grid">
      <article v-for="policy in policies" :key="policy.id" class="policy-card">
        <div class="card-top">
          <span class="badge neutral">{{ policy.type }}</span>
          <span class="badge">{{ policy.status }}</span>
        </div>
        <h3>{{ policy.name }}</h3>
        <p>{{ policy.targetScope }} · 优先级 {{ policy.priority }} · {{ policy.owner }}</p>

        <div class="rollout">
          <span>下发进度 {{ policy.rollout }}%</span>
          <div class="track"><i :style="{ width: `${policy.rollout}%` }"></i></div>
        </div>

        <footer>
          <div>
            <strong>{{ policy.version }}</strong>
            <small>{{ policy.lastAction }}</small>
          </div>
          <button class="button secondary" :disabled="!progress[policy.status]" @click="advancePolicy(policy)">
            {{ nextLabel(policy.status) }}
          </button>
        </footer>
      </article>
    </div>

    <div v-if="showForm" class="modal-backdrop" @click.self="showForm = false">
      <form class="modal" @submit.prevent="createPolicy">
        <div class="modal-title">
          <div>
            <h3>新建安全策略</h3>
            <p>新建后进入草稿状态，可继续配置规则并提交审批。</p>
          </div>
          <button type="button" @click="showForm = false">关闭</button>
        </div>

        <label>
          策略名称
          <input v-model="form.name" placeholder="例如：研发终端外设白名单策略" />
        </label>
        <label>
          策略类型
          <select v-model="form.type">
            <option>防病毒</option>
            <option>补丁管理</option>
            <option>外设管控</option>
            <option>软件白名单</option>
            <option>网络隔离</option>
          </select>
        </label>
        <label>
          目标范围
          <select v-model="form.scope">
            <option>全公司终端</option>
            <option>研发部</option>
            <option>财务部</option>
            <option>服务器分组</option>
            <option>高风险动态分组</option>
          </select>
        </label>
        <label>
          优先级
          <input v-model.number="form.priority" type="number" min="1" max="200" />
        </label>

        <div class="form-actions">
          <button type="button" class="button secondary" @click="showForm = false">取消</button>
          <button class="button primary">创建草稿</button>
        </div>
      </form>
    </div>
  </section>
</template>
