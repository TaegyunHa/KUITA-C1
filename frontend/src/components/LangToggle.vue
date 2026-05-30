<script setup>
import { useLang } from '../composables/useLanguage.js'

const { locale, toggle } = useLang()
</script>

<template>
  <button class="lang-toggle" @click="toggle" :aria-label="locale === 'ko' ? 'Switch to English' : '한국어로 전환'">
    <span :class="{ active: locale === 'ko' }">KO</span>
    <span class="sep">|</span>
    <span :class="{ active: locale === 'en' }">EN</span>
  </button>
</template>

<style scoped>
.lang-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #282d37;
  border-radius: 20px;
  padding: 6px 14px;
  color: var(--text-sub);
  font-size: 13px;
  font-weight: 600;
  transition: opacity 0.15s;
}

.lang-toggle:hover {
  opacity: 0.85;
}

.sep {
  color: #4a5060;
}

.active {
  color: #ffffff;
}
</style>
