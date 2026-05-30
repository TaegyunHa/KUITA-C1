<script setup>
import { ref, computed } from 'vue'
import { CATEGORY_COLORS } from '../categories.js'
import { useLang } from '../composables/useLanguage.js'

const props = defineProps({
  card: { type: Object, required: true },
})

const flipped = ref(false)
const { locale } = useLang()

const colors = computed(() => CATEGORY_COLORS[props.card.category] ?? { chip: '#DBE0E8', card: '#F8F9FA' })

const chipLabel = computed(() =>
  locale.value === 'ko'
    ? props.card.category_ko
    : props.card.category
)

const sourceDomain = computed(() => {
  try {
    return new URL(props.card.url).hostname.replace('www.', '')
  } catch {
    return props.card.url
  }
})

function flip() { flipped.value = !flipped.value }
function openLink(e) {
  e.stopPropagation()
}
</script>

<template>
  <div class="card" :class="{ flipped }" @click="flip">
    <div class="card-inner">
      <!-- FRONT -->
      <div class="card-face card-front" :style="{ background: colors.card }">
        <span class="chip" :style="{ background: colors.chip }">{{ chipLabel }}</span>
        <p class="title">{{ card.title }}</p>
        <p class="what-now-label">What now?</p>
        <p class="impact">{{ card.impact_line }}</p>
      </div>

      <!-- BACK -->
      <div class="card-face card-back">
        <p class="summary">{{ card.summary }}</p>
        <a
          class="source-link"
          :href="card.url"
          target="_blank"
          rel="noopener noreferrer"
          @click="openLink"
        >
          🔗 Read on {{ sourceDomain }}
        </a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card {
  width: 440px;
  height: 208px;
  flex-shrink: 0;
  perspective: 1000px;
  cursor: pointer;
}

.card-inner {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 0.4s ease;
}

.card.flipped .card-inner {
  transform: rotateY(180deg);
}

.card-face {
  position: absolute;
  inset: 0;
  border-radius: 12px;
  padding: 16px;
  backface-visibility: hidden;
  overflow: hidden;
  border: 1px solid var(--surface);
}

/* FRONT */
.card-front {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.chip {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-main);
  align-self: flex-start;
}

.title {
  font-size: 14px;
  font-weight: 600;
  color: var(--text-main);
  line-height: 1.4;
  flex: 1;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
}

.what-now-label {
  font-size: 11px;
  font-weight: 600;
  color: var(--accent);
  letter-spacing: 0.02em;
}

.impact {
  font-size: 12px;
  color: var(--text-main);
  line-height: 1.4;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

/* BACK */
.card-back {
  transform: rotateY(180deg);
  background: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.summary {
  font-size: 13px;
  color: var(--text-main);
  line-height: 1.5;
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  flex: 1;
}

.source-link {
  font-size: 13px;
  color: var(--accent);
  margin-top: 10px;
  flex-shrink: 0;
  word-break: break-all;
}
</style>
