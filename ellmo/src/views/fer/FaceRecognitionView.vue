<template>
  <div class="face-recognition-container">

    <div class="info">
        Based on <a href="https://justadudewhohacks.github.io/face-api.js/docs/index.html" target="_blank">face-api.js</a>

        <!-- 
            face-api.js has a MIT license and is built on top of tfjs-core, 
            which comes with the Apache Version 2.0 license.
        -->
        <div class="controls">
            <label>
                <input type="checkbox" v-model="isBlackAndWhite"> Grayscale
            </label>
        </div>


        <div v-if="!isModelLoaded" class="loading-overlay">
            Loading Models...
        </div>
    </div>

    <div class="video-wrapper">
        <video 
            ref="videoEl" 
            width="720" 
            height="560" 
            autoplay 
            muted 
            @play="onPlay"
            :class="{ 'grayscale': isBlackAndWhite }"
        ></video>
      <canvas ref="canvasEl"></canvas>
    </div>

  </div>
</template>


<script setup>
import { ref, onMounted } from 'vue'
import * as faceapi from 'face-api.js'

const videoEl = ref(null)
const canvasEl = ref(null)
const isModelLoaded = ref(false)
const isBlackAndWhite = ref(false)


const loadModels = async () => {
    console.log('Loading models...')
    const MODEL_URL = '/models'

    await Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri(MODEL_URL),
        faceapi.nets.faceLandmark68Net.loadFromUri(MODEL_URL),
        faceapi.nets.faceRecognitionNet.loadFromUri(MODEL_URL),
        faceapi.nets.faceExpressionNet.loadFromUri(MODEL_URL)
    ])
    isModelLoaded.value = true
    startVideo()
}

const startVideo = () => {
    navigator.mediaDevices.getUserMedia({ video: {} })
        .then(stream => {
        videoEl.value.srcObject = stream
        })
        .catch(err => console.error(err))
}

const onPlay = () => {
    const video = videoEl.value
    const canvas = canvasEl.value
    
    // Ensure the video and canvas elements are available
    if (!video || !canvas) return;

    const displaySize = { width: video.width, height: video.height }
    faceapi.matchDimensions(canvas, displaySize)

    // Define the main detection/drawing loop function
    const detectFaces = async () => {
        
        // Check if the video is paused/ended before continuing the loop
        if (video.paused || video.ended) return; 

        // 1. Perform Detections
        const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
            .withFaceLandmarks()
            // NOTE: .withFaceDescriptors() is computationally expensive. Keep it only if you need to identify people.
            .withFaceDescriptors() 
            .withFaceExpressions()
            
        const resizedDetections = faceapi.resizeResults(detections, displaySize)

        // 2. Clear canvas and Draw
        const context = canvas.getContext('2d')
        context.clearRect(0, 0, canvas.width, canvas.height)
        
        // Check if there are detections before drawing
        if (resizedDetections.length > 0) {
            faceapi.draw.drawDetections(canvas, resizedDetections)
            faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
            faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
        }

        // 3. Request the next frame iteration
        requestAnimationFrame(detectFaces)
    }

    // Start the recursive loop
    detectFaces()
}

onMounted(() => {
  loadModels()
})
</script>



<style lang="scss" scoped>
    @import "./faceRecognition.scss";

    .grayscale {
        filter: grayscale(100%);
    }
    
    .controls {
        margin-top: 10px;
    }
</style>
