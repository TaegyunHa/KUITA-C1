<script setup>
import { reactive, watch } from 'vue'
import { useLang } from '../composables/useLanguage.js'

const props = defineProps({
  profile: { type: Object, required: true },
  saving: { type: Boolean, default: false },
  ctaLabel: { type: String, default: null },
})

const emit = defineEmits(['save'])
const { t } = useLang()

const AGE_BANDS = ['<25', '25–34', '35–44', '45+']
const OCCUPATIONS = ['Student', 'Office worker', 'Self-employed', 'Researcher', 'Homemaker', 'Other']

const form = reactive({
  postcode_area: '',
  age_band: '25–34',
  occupation: 'Student',
  interests: '',
})

watch(
  () => props.profile,
  (p) => {
    if (!p) return
    form.postcode_area = p.postcode_area ?? ''
    form.age_band = p.age_band ?? '25–34'
    form.occupation = p.occupation ?? 'Student'
    form.interests = p.interests ?? ''
  },
  { immediate: true }
)

function submit() {
  emit('save', { ...form })
}
</script>

<template>
  <form @submit.prevent="submit" class="profile-form">
    <div class="field-group">
      <p class="section-label">{{ t('기본 정보', 'Basic info') }}</p>
      <hr class="divider" />

      <label class="field">
        <span class="field-label">{{ t('우편번호 지역', 'Postcode area') }}</span>
        <input
          v-model="form.postcode_area"
          type="text"
          :placeholder="t('예: SW1, E14, M1', 'e.g. SW1, E14, M1')"
          class="text-input"
        />
      </label>

      <label class="field">
        <span class="field-label">{{ t('연령대', 'Age band') }}</span>
        <div class="radio-group">
          <label v-for="band in AGE_BANDS" :key="band" class="radio-label">
            <input type="radio" :value="band" v-model="form.age_band" />
            {{ band }}
          </label>
        </div>
      </label>

      <label class="field">
        <span class="field-label">{{ t('직업', 'Occupation') }}</span>
        <select v-model="form.occupation" class="select-input">
          <option v-for="occ in OCCUPATIONS" :key="occ" :value="occ">{{ occ }}</option>
        </select>
      </label>
    </div>

    <div class="field-group">
      <p class="section-label">{{ t('관심사', 'Interests') }}</p>
      <hr class="divider" />
      <label class="field">
        <textarea
          v-model="form.interests"
          :placeholder="t('예: central line 출퇴근, Zone 2 이사 계획, ILR 신청 예정', 'e.g. central line commuter, looking for flat in Zone 2, ILR application next year')"
          class="textarea-input"
          rows="3"
        />
      </label>
    </div>

    <button type="submit" class="save-btn" :disabled="saving">
      {{ ctaLabel ?? t('저장 / Save', 'Save') }}
    </button>
  </form>
</template>

<style scoped>
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.section-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-sub);
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.divider {
  border: none;
  border-top: 1px solid var(--surface);
  margin-top: -8px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 14px;
  color: var(--text-main);
}

.text-input,
.select-input,
.textarea-input {
  width: 100%;
  padding: 12px;
  border: 1px solid var(--surface);
  border-radius: 8px;
  font-size: 14px;
  color: var(--text-main);
  background: #ffffff;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.text-input:focus,
.select-input:focus,
.textarea-input:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-light);
}

.radio-group {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  cursor: pointer;
}

.radio-label input {
  accent-color: var(--accent);
  width: 16px;
  height: 16px;
}

.textarea-input {
  resize: vertical;
  min-height: 80px;
}

.save-btn {
  background: var(--accent);
  color: #ffffff;
  font-size: 15px;
  font-weight: 600;
  width: 100%;
  height: 48px;
  border-radius: 8px;
  transition: opacity 0.15s;
}

.save-btn:hover:not(:disabled) {
  opacity: 0.85;
}

.save-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
