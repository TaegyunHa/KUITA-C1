<script setup>
import { ref } from 'vue'
import ProfileForm from './ProfileForm.vue'
import { putProfile } from '../api.js'

const props = defineProps({
  profile: { type: Object, required: true },
})

const emit = defineEmits(['done'])

const saving = ref(false)
const error = ref(null)

async function handleSave(formData) {
  saving.value = true
  error.value = null
  try {
    await putProfile(formData)
    emit('done', formData)
  } catch (e) {
    error.value = e.message
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="overlay">
    <div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-title">
      <h1 id="modal-title" class="brand">What NOW?</h1>
      <p class="subtitle">나에게 맞는 뉴스를 시작해 보세요</p>
      <hr class="divider" />

      <p v-if="error" class="error-msg">{{ error }}</p>

      <ProfileForm
        :profile="profile"
        :saving="saving"
        cta-label="What's my NOW? →"
        @save="handleSave"
      />
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 200;
  padding: 20px;
}

.modal {
  background: #ffffff;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 480px;
  max-height: 90vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.brand {
  font-size: 24px;
  font-weight: 700;
  color: var(--main);
}

.subtitle {
  font-size: 16px;
  color: var(--text-sub);
}

.divider {
  border: none;
  border-top: 1px solid var(--surface);
  margin: 4px 0;
}

.error-msg {
  font-size: 13px;
  color: #dc2626;
  background: #fef2f2;
  padding: 10px 12px;
  border-radius: 8px;
}
</style>
