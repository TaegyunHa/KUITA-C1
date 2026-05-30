<script setup>
import { ref, computed, onMounted, inject, watch } from 'vue'
import CategorySection from '../components/CategorySection.vue'
import { getFeed } from '../api.js'
import { CATEGORY_ORDER } from '../categories.js'
import { useLang } from '../composables/useLanguage.js'

const { t } = useLang()

const cards = ref([])
const loading = ref(false)
const error = ref(null)

const feedRevision = inject('feedRevision', ref(0))

const grouped = computed(() => {
  const map = {}
  for (const card of cards.value) {
    if (!map[card.category]) map[card.category] = { category_ko: card.category_ko, cards: [] }
    map[card.category].cards.push(card)
  }
  return CATEGORY_ORDER
    .filter((cat) => map[cat]?.cards.length)
    .map((cat) => ({ category: cat, category_ko: map[cat].category_ko, cards: map[cat].cards }))
})

async function fetchFeed() {
  loading.value = true
  error.value = null
  try {
    cards.value = await getFeed()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

watch(feedRevision, fetchFeed)

onMounted(fetchFeed)
</script>

<template>
  <div class="feed-page">
    <div class="feed-toolbar">
      <button class="refresh-btn" @click="fetchFeed" :disabled="loading">
        ↻ {{ t('피드 새로고침', 'Refresh feed') }}
      </button>
    </div>

    <!-- Loading -->
    <div v-if="loading" class="state-msg">
      <div class="spinner" />
      <p>{{ t('불러오는 중…', 'Loading…') }}</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="state-msg error">
      <p>{{ t('피드를 불러오지 못했습니다.', 'Failed to load feed.') }}</p>
      <p class="error-detail">{{ error }}</p>
      <button class="retry-btn" @click="fetchFeed">{{ t('다시 시도', 'Retry') }}</button>
    </div>

    <!-- Empty -->
    <div v-else-if="grouped.length === 0" class="state-msg">
      <p>{{ t('표시할 뉴스가 없습니다.', 'No news to display yet.') }}</p>
    </div>

    <!-- Feed -->
    <div v-else class="feed-content">
      <CategorySection
        v-for="group in grouped"
        :key="group.category"
        :category="group.category"
        :category-ko="group.category_ko"
        :cards="group.cards"
      />
    </div>
  </div>
</template>

<style scoped>
.feed-page {
  padding-top: 88px; /* 64px navbar + 24px gap */
  padding-left: 40px;
  padding-right: 40px;
  padding-bottom: 60px;
  max-width: 1512px;
  margin: 0 auto;
}

.feed-toolbar {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 32px;
}

.refresh-btn {
  background: var(--accent);
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  padding: 10px 18px;
  border-radius: 8px;
  transition: opacity 0.15s;
}

.refresh-btn:hover:not(:disabled) {
  opacity: 0.85;
}

.refresh-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.state-msg {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 80px 0;
  color: var(--text-sub);
  font-size: 15px;
}

.state-msg.error {
  color: #dc2626;
}

.error-detail {
  font-size: 12px;
  color: var(--text-sub);
}

.retry-btn {
  background: var(--accent);
  color: #ffffff;
  font-size: 13px;
  font-weight: 600;
  padding: 8px 20px;
  border-radius: 8px;
}

.retry-btn:hover {
  opacity: 0.85;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--surface);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.feed-content {
  display: flex;
  flex-direction: column;
}
</style>
