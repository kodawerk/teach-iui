import type { StringMappingType } from "typescript"

export interface APIChatRequest {
    model: string,
    messages: APIChatMessage[]
}

export interface APIChatMessage {
    role: string,
    content: string
}

export interface APIChatResponse {
    messageId: number,
    sessionId: string,
    createdAt: Date,
    assistantId: string,
    threadId: string
    imageName: string
    userContent: string
    systemResponse: string
    imageAnalysis: string
}