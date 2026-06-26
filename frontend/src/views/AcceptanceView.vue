<script setup lang="ts">
import { computed, ref } from 'vue';
import PageHeader from '../components/PageHeader.vue';
import { acceptanceItems as source } from '../data';

const items = ref(structuredClone(source));
const notice = ref('');
const conclusion = ref({
  reviewer: '项目经理',
  window: '今日 18:30',
  summary: '构建通过，前端交互已可验收，剩余重点是告警闭环说明与报表归档。'
});

const percent = computed(() =>
  Math.round((items.value.filter((item) => item.done).length / items.value.length) * 100)
);

const blockers = computed(() => items.value.filter((item) => !item.done));

function publishSummary() {
  notice.value = `已生成验收摘要：${conclusion.value.reviewer} 将在 ${conclusion.value.window} 组织评审。`;
}
</script>

<template>
  <section class="page">
    <PageHeader
      code="SEC-07"
      title="验收中心"
      :description="`跟踪功能、证据、测试和交付，当前完成度 ${percent}%。`"
      action="生成验收摘要"
      @action="publishSummary"
    />

    <div v-if="notice" class="notice">
      {{ notice }}
      <button @click="notice = ''">关闭</button>
    </div>

    <div class="acceptance-progress">
      <div>
        <strong>{{ percent }}%</strong>
        <span>验收完成度</span>
      </div>
      <div class="track"><i :style="{ width: `${percent}%` }"></i></div>
    </div>

    <div class="mini-metrics mini-metrics-4">
      <article>
        <span>已完成项</span>
        <strong>{{ items.filter((item) => item.done).length }}</strong>
      </article>
      <article>
        <span>待收口</span>
        <strong>{{ blockers.length }}</strong>
      </article>
      <article>
        <span>构建状态</span>
        <strong>通过</strong>
      </article>
      <article>
        <span>验收窗口</span>
        <strong>{{ conclusion.window }}</strong>
      </article>
    </div>

    <div class="content-grid wide-left">
      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">CHECKLIST</span>
            <h3>验收清单</h3>
            <p>逐项记录状态、证据、责任人与下一步动作。</p>
          </div>
        </div>

        <div class="acceptance-list">
          <article v-for="item in items" :key="item.id" class="acceptance-card">
            <label class="checkbox">
              <input v-model="item.done" type="checkbox" :aria-label="`完成 ${item.id}`" />
              <span>{{ item.done ? '通过' : '待完成' }}</span>
            </label>
            <strong>{{ item.id }} · {{ item.module }}</strong>
            <p>{{ item.item }}</p>
            <small>证据：{{ item.proof }}</small>
            <small>责任人：{{ item.owner }} · 截止：{{ item.dueAt }}</small>
            <small>下一步：{{ item.nextAction }}</small>
          </article>
        </div>
      </section>

      <section class="panel">
        <div class="panel-title">
          <div>
            <span class="section-code">DECISION DESK</span>
            <h3>验收结论</h3>
            <p>把评审人、窗口和当前结论沉淀成可交付摘要。</p>
          </div>
        </div>

        <form class="form-grid" @submit.prevent="publishSummary">
          <label>
            评审负责人
            <input v-model="conclusion.reviewer" type="text" />
          </label>
          <label>
            验收时间
            <input v-model="conclusion.window" type="text" />
          </label>
          <label class="form-span-2">
            当前结论
            <textarea v-model="conclusion.summary" rows="5"></textarea>
          </label>
          <div class="form-actions form-span-2">
            <button type="submit" class="button primary">更新验收结论</button>
          </div>
        </form>

        <ul class="compact-list compact-list-tight">
          <li v-for="item in blockers" :key="item.id">
            <span>{{ item.module }}</span>
            <strong>{{ item.id }}</strong>
            <em class="status-未达标">待完成</em>
          </li>
        </ul>
      </section>
    </div>
  </section>
</template>
