<script setup lang="ts">
import type { RiskLevel } from '../data';

defineProps<{ value: RiskLevel }>();
</script>

<template>
  <span class="badge" :class="`risk-${value}`">{{ value }}</span>
</template>
