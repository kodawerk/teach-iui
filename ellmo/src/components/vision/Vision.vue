
<template>
    <div :class="'popup' + (isMinimized ? ' hidden' : '')">
        <video 
            ref="videoElement" 
            :class="{ active: isCameraActive }"
            autoplay 
            muted 
            playsinline
        ></video>

        <canvas ref="canvasElement" style="display: none;"></canvas>

        <div class="controls">
            <button @click="isCameraActive ? stopCamera() : startCamera()">
                {{isCameraActive ? "Stop Cam" : "Start Cam" }}
            </button>
            <button @click="toggleAnalysisLoop()">
                {{analysisEnabled ? "Pause FER" : "Start FER"}}
            </button>
            <button @click="isMinimized = true">&larr;</button>
        </div>

        <p class="status">
            <strong>Status:</strong> {{ status }}<br/>
            <strong>Result:</strong> {{ analysisResult }}
        </p>
    </div>

    <div :class="'popup' + (isMinimized ? '' : ' hidden')">
        <button @click="isMinimized = false"> &rarr;</button>
    </div>
</template>


<script setup lang="ts">
import { ref, onMounted, onUnmounted, type Ref } from 'vue';

const videoElement: Ref<HTMLVideoElement | null> = ref(null);
const canvasElement: Ref<HTMLCanvasElement | null> = ref(null);
const isCameraActive = ref(false);
const isMinimized = ref(false);
let analysisInterval = null;
let videoStream = null;
const isAnalyzing = ref(false); 
const analysisEnabled = ref(false);
const analysisResult = ref('');
const status = ref('');

const emit = defineEmits(['fer']);

const startCamera = async () => {
    try {
        videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
        videoElement.value.srcObject = videoStream;
        await videoElement.value.play();
        
        isCameraActive.value = true;
        // analysisResult.value = 'Camera active. Analysis started.';
        
        startAnalysisLoop();

    } catch (error) {
        console.error('Error accessing webcam:', error);
        status.value = 'Error: Could not access webcam. Please check permissions.';
        isCameraActive.value = false;
    }
};

const stopCamera = () => {
    if (videoStream) {
        videoStream.getTracks().forEach(track => track.stop());
    }
    stopAnalysisLoop();
    isCameraActive.value = false;
    videoStream = null;
    status.value = 'Camera stopped.';
};

const startAnalysisLoop = () => {
    stopAnalysisLoop(); 
    
    // run analyze method every 1000ms
    analysisEnabled.value = true;
    analysisInterval = setInterval(analyzeFrame, 1000);
};

const stopAnalysisLoop = () => {
    if (analysisInterval) {
        clearInterval(analysisInterval);
        analysisInterval = null;
        // analysisResult.value = '';
    }
    analysisEnabled.value = false;
};

const toggleAnalysisLoop = () => {
    if (analysisEnabled.value) {
        stopAnalysisLoop();
    } else {
        startAnalysisLoop();
    }
}

const analyzeFrame = async () => { 
    const video = videoElement.value;
    const canvas = canvasElement.value;
    
    if (!video || !canvas || video.paused || video.ended) return;

    if (isAnalyzing.value) {
        return; 
    }

    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    
    // convert canvas content to a base64 JPEG data URL
    //const imageDataUrl = canvas.toDataURL('image/jpeg');
    const imageDataUrl = canvas.toDataURL('image/jpeg').split(',')[1];

    // analyze with LLAVA
    const visionRequest = {
        "model": "llava",
        "messages": [
            {
            "role": "user",
            "content": "Describe the facial expression of the person in the image.",
            "images": [imageDataUrl] 
            }
        ],
        "stream": false
    }
    isAnalyzing.value = true;
    status.value = 'Analyzing...';

    // send request
    try {
        const url = "http://localhost:11434/api/chat"
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(visionRequest),
        });


        if (!response.ok) {
            throw new Error(`Ollama API returned status: ${response.status}`);
        }

        const data = await response.json();
        
        // extract the analysis result and update state
        const analysisText = data.message.content;
        analysisResult.value = analysisText; //`Analysis (${new Date().toLocaleTimeString()}): ${analysisText}`;
        
    } catch (error) {
        console.error('Ollama Vision Analysis Error:', error);
        analysisResult.value = `Error analyzing image: ${error.message}. Ensure 'ollama serve' is running and 'llava' is pulled.`;
    } finally {
        isAnalyzing.value = false;
    }
    
    // Emit the data URL to the parent component for potential processing
    emit('fer', analysisResult.value);
};


onMounted(() => {
    startCamera();
});

onUnmounted(() => {
    stopCamera(); 
});
</script>


<style lang="scss" scoped>
    @use "./vision.scss";
</style>