



<template>
    <div class="chat-view">

        <div class="conversationContainer"   ref="conversationContainer">
            <div v-for="m,i in chatHistory" :key="i" :class="['message-bubble', m.role]">
                <div class="content">
                    {{ m.content }}
                </div>
            </div>
            <div class="message-bubble assistant thinking" v-if="isThinking">
                <div class="content">
                    {{ systemResponse }}
                </div>
            </div>
        </div>

        
        <div class="chat-input-container">
            <input
            type="text"
            v-model="userPrompt"
            @keyup.enter="sendMessage"
            placeholder="Ask anything..."
            class="prompt-input"
            />
            <button @click="sendMessage" :disabled="!userPrompt.trim()" class="send-button">
            Send
            </button>
        </div>
        
    </div>
</template>





<script setup lang="ts">
import type { APIChatMessage, APIChatRequest, APIChatResponse } from '@/types/chat.types';
import { nextTick, ref } from 'vue';
import ollama from 'ollama';

const emit = defineEmits(['send-prompt']);
const userPrompt = ref('');
const systemResponse = ref('');
const chatHistory = ref<APIChatMessage[]>([]);
const isThinking = ref(false);
const conversationContainer = ref<HTMLElement | null>(null);

const sendMessage = () => {
    if (userPrompt.value.trim()) {
        //emit('send-prompt', userPrompt.value);


        handleSendPrompt(userPrompt.value)
        
        userPrompt.value = '';
    }
};

const handleSendPrompt = async (prompt: string) => {
    isThinking.value = true; 

    // new user message
    const chatMessage: APIChatMessage = {
        role: 'user',
        content: prompt
    }
    chatHistory.value.push(chatMessage);

    // system prompt
    const systemPrompt: APIChatMessage = { 
        role: 'system', 
        content: 'your are a helpful assistant' 
    };
    const requestMessages: APIChatMessage[] = [systemPrompt, ...chatHistory.value];

    // system response
    systemResponse.value = ""
    
    try {

        //  Ollama API call
        const responseStream = await ollama.chat({
            model: 'llama3',
            messages: requestMessages,
            stream: true
        });

        // 6. Consume the stream and update the assistant message in real-time
        for await (const chunk of responseStream) {
            if (chunk.message.content) {
                systemResponse.value += chunk.message.content;
                updateConversation();
            }
        }
    } catch (error: any) {
        console.error('Ollama API Error:', error);
        systemResponse.value = `ERROR: Could not connect to Ollama server. Please ensure **ollama serve** is running and the model ('llama3') is pulled. (Details: ${error.message})`;
    } finally {
        isThinking.value = false; 
        
        // update history
        chatHistory.value.push({
            role: 'assistant',
            content: systemResponse.value
        });
        systemResponse.value = "";
    }
};

const updateConversation = () => {
    // We use nextTick to wait until Vue has updated the DOM with the new content
    nextTick(() => {
        if (conversationContainer.value) {
            conversationContainer.value.scrollTop = conversationContainer.value.scrollHeight;
        }
    });
}


</script>


<style lang="scss" scoped>
    @use "./chat.scss";
</style>
