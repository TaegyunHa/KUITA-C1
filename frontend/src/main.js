import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import FeedView from './views/FeedView.vue'
import ProfileView from './views/ProfileView.vue'
import './tokens.css'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: FeedView },
    { path: '/profile', component: ProfileView },
  ],
})

createApp(App).use(router).mount('#app')
