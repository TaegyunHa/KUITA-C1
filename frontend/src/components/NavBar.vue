<script setup>
import { useRouter } from 'vue-router'
import LangToggle from './LangToggle.vue'
import { useLang } from '../composables/useLanguage.js'

const router = useRouter()
const { t } = useLang()
</script>

<template>
  <nav class="navbar">
    <span class="logo" @click="router.push('/')">What NOW?</span>
    <LangToggle class="lang" />
    <button class="profile-btn" @click="router.push('/profile')">
      {{ t('프로필 →', 'Profile →') }}
    </button>
  </nav>
</template>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background: var(--main);
  display: flex;
  align-items: center;
  padding: 0 40px;
  z-index: 100;
}

.logo {
  font-size: 20px;
  font-weight: 700;
  color: #ffffff;
  cursor: pointer;
  user-select: none;
  flex-shrink: 0;
}

.lang {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
}

.profile-btn {
  margin-left: auto;
  background: var(--accent);
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 8px;
  transition: opacity 0.15s;
}

.profile-btn:hover {
  opacity: 0.85;
}
</style>
