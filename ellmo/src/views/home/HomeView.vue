



<template>
    <Vision @fer="handleFER">
    </Vision>
    <Chat :ferInput="fer">
    </Chat>
</template>

<script setup lang="ts">
    import Chat from '@/components/chat/Chat.vue'
    import Vision from '@/components/vision/Vision.vue'
    import { ref } from 'vue';

    const fer = ref('');

    const handleFER = (ferInterpretation: string) => {
        fer.value = ferInterpretation
    };
</script>


<style lang="scss" scoped>
    @use "./home.scss";
</style>
