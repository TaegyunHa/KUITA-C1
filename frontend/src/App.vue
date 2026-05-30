<script setup>
import { ref, provide, onMounted } from 'vue'
import { RouterView } from 'vue-router'
import NavBar from './components/NavBar.vue'
import OnboardingModal from './components/OnboardingModal.vue'
import { provideLang } from './composables/useLanguage.js'
import { getProfile } from './api.js'

provideLang()

const showOnboarding = ref(false)
const defaultProfile = ref({ postcode_area: '', age_band: '25–34', occupation: 'Student', interests: '' })

const feedRevision = ref(0)
provide('feedRevision', feedRevision)

onMounted(async () => {
  if (!localStorage.getItem('profileComplete')) {
    try {
      defaultProfile.value = await getProfile()
    } catch {
      // use defaults if backend unreachable
    }
    showOnboarding.value = true
  }
})

function onboardingDone(savedProfile) {
  localStorage.setItem('profileComplete', 'true')
  defaultProfile.value = savedProfile
  showOnboarding.value = false
  feedRevision.value++
}
</script>

<template>
  <NavBar />
  <RouterView />
  <OnboardingModal
    v-if="showOnboarding"
    :profile="defaultProfile"
    @done="onboardingDone"
  />
</template>
