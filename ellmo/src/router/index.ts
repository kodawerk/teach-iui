import ChatView from '@/components/chat/ChatView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [    
    {
        path: '/',
        name: '',
        component: ChatView
        }
    ]
})

export default router
