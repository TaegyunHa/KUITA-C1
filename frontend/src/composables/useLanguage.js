import { ref, provide, inject } from 'vue'

const LANG_KEY = Symbol('lang')

export function provideLang() {
  const locale = ref('ko')
  const toggle = () => {
    locale.value = locale.value === 'ko' ? 'en' : 'ko'
  }
  provide(LANG_KEY, { locale, toggle })
  return { locale, toggle }
}

export function useLang() {
  const ctx = inject(LANG_KEY)
  const t = (ko, en) => (ctx.locale.value === 'ko' ? ko : en)
  return { locale: ctx.locale, toggle: ctx.toggle, t }
}
