import { createRouter, createWebHistory } from 'vue-router';
import AcceptanceView from './views/AcceptanceView.vue';
import AlertView from './views/AlertView.vue';
import AuditView from './views/AuditView.vue';
import ControlCenterView from './views/ControlCenterView.vue';
import DashboardView from './views/DashboardView.vue';
import EndpointDetailView from './views/EndpointDetailView.vue';
import EndpointView from './views/EndpointView.vue';
import PolicyView from './views/PolicyView.vue';
import ReportView from './views/ReportView.vue';

export const router = createRouter({
  history: createWebHistory(),
  scrollBehavior: () => ({ top: 0, left: 0 }),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: DashboardView, meta: { title: '安全态势' } },
    { path: '/endpoints', component: EndpointView, meta: { title: '终端资产' } },
    { path: '/endpoints/:id', component: EndpointDetailView, meta: { title: '终端详情' } },
    { path: '/policies', component: PolicyView, meta: { title: '策略下发' } },
    { path: '/controls', component: ControlCenterView, meta: { title: '防护控制' } },
    { path: '/alerts', component: AlertView, meta: { title: '告警闭环' } },
    { path: '/reports', component: ReportView, meta: { title: '报表中心' } },
    { path: '/acceptance', component: AcceptanceView, meta: { title: '验收中心' } },
    { path: '/audit', component: AuditView, meta: { title: '审计日志' } }
  ]
});
