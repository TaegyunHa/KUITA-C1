<script setup>
import { computed } from 'vue'
import NewsCard from './NewsCard.vue'
import { CATEGORY_COLORS } from '../categories.js'
import { useLang } from '../composables/useLanguage.js'

const props = defineProps({
  category: { type: String, required: true },
  categoryKo: { type: String, required: true },
  cards: { type: Array, required: true },
})

const { locale } = useLang()

const colors = computed(() => CATEGORY_COLORS[props.category] ?? { chip: '#DBE0E8', card: '#F8F9FA' })
const displayName = computed(() => locale.value === 'ko' ? props.categoryKo : props.category)
</script>

<template>
  <section class="category-section">
    <div class="section-header">
      <div class="header-left">
        <span class="chip" :style="{ background: colors.chip }">{{ displayName }}</span>
        <span class="cat-name">{{ category }}</span>
      </div>
      <span class="see-more">{{ locale === 'ko' ? '더 보기 →' : 'See more →' }}</span>
    </div>
    <hr class="divider" />
    <div class="card-row">
      <NewsCard v-for="card in cards" :key="card.id" :card="card" />
    </div>
  </section>
</template>

<style scoped>
.category-section {
  margin-bottom: 40px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 10px;
}

.chip {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 13px;
  font-weight: 600;
  color: var(--text-main);
}

.cat-name {
  font-size: 16px;
  font-weight: 600;
  color: var(--text-sub);
}

.see-more {
  font-size: 13px;
  color: var(--text-sub);
  cursor: default;
}

.divider {
  border: none;
  border-top: 1px solid var(--surface);
  margin-bottom: 16px;
}

.card-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
</style>
