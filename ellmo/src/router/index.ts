import HomeView from '@/views/home/HomeView.vue'
import FaceRecognitionView from '@/views/fer/FaceRecognitionView.vue'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [    
    {
        path: '/',
        name: '',
        component: HomeView
        
    }, 
    {
        path: '/fer',
        name: '',
        component: FaceRecognitionView
        
    }
    ]
})

export default router
