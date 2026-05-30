<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ProfileForm from '../components/ProfileForm.vue'
import { getProfile, putProfile } from '../api.js'
import { useLang } from '../composables/useLanguage.js'

const router = useRouter()
const { t } = useLang()

const profile = ref(null)
const saving = ref(false)
const error = ref(null)
const saved = ref(false)

onMounted(async () => {
  try {
    profile.value = await getProfile()
  } catch (e) {
    error.value = e.message
  }
})

async function handleSave(formData) {
  saving.value = true
  error.value = null
  saved.value = false
  try {
    await putProfile(formData)
    localStorage.setItem('profileComplete', 'true')
    saved.value = true
    setTimeout(() => router.push('/'), 600)
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}

function resetProfile() {
  if (!confirm(t('프로필을 초기화하시겠습니까?', 'Reset your profile?'))) return
  localStorage.removeItem('profileComplete')
  profile.value = { postcode_area: '', age_band: '25–34', occupation: 'Student', interests: '' }
}
</script>

<template>
  <div class="profile-page">
    <div class="form-card">
      <h1 class="heading">{{ t('프로필 설정', 'Profile') }}</h1>

      <div v-if="!profile" class="loading">{{ t('불러오는 중…', 'Loading…') }}</div>

      <template v-else>
        <p v-if="error" class="error-msg">{{ error }}</p>
        <p v-if="saved" class="saved-msg">{{ t('저장되었습니다 ✓', 'Saved ✓') }}</p>

        <ProfileForm :profile="profile" :saving="saving" @save="handleSave" />

        <button class="reset-link" @click="resetProfile">
          {{ t('프로필 초기화', 'Reset profile') }}
        </button>
      </template>
    </div>
  </div>
</template>

<style scoped>
.profile-page {
  padding-top: 96px;
  padding-left: 40px;
  padding-right: 40px;
  padding-bottom: 60px;
  display: flex;
  justify-content: center;
}

.form-card {
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.heading {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-main);
}

.loading {
  color: var(--text-sub);
}

.error-msg {
  font-size: 13px;
  color: #dc2626;
  background: #fef2f2;
  padding: 10px 12px;
  border-radius: 8px;
}

.saved-msg {
  font-size: 13px;
  color: #16a34a;
  background: #f0fdf4;
  padding: 10px 12px;
  border-radius: 8px;
}

.reset-link {
  background: none;
  border: none;
  font-size: 13px;
  color: var(--text-sub);
  text-align: center;
  cursor: pointer;
  text-decoration: underline;
}

.reset-link:hover {
  color: var(--text-main);
}
</style>
