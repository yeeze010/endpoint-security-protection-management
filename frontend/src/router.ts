import { createRouter, createWebHistory } from 'vue-router';
import DashboardView from './views/DashboardView.vue';
import EndpointView from './views/EndpointView.vue';
import PolicyView from './views/PolicyView.vue';
import AlertView from './views/AlertView.vue';
import AuditView from './views/AuditView.vue';

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', redirect: '/dashboard' },
    { path: '/dashboard', component: DashboardView },
    { path: '/endpoints', component: EndpointView },
    { path: '/policies', component: PolicyView },
    { path: '/alerts', component: AlertView },
    { path: '/audit', component: AuditView }
  ]
});
