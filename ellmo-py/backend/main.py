import ollama
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = 'llama3'

app = FastAPI()

# use ollama.AsyncClient for non-blocking network i/o
async_ollama_client = ollama.AsyncClient(host=OLLAMA_BASE_URL)


class ChatRequest(BaseModel):
    user_prompt: str
    model_name: str = DEFAULT_MODEL

# --- streaming endpoint ---
@app.post("/chat/stream")
async def stream_chat_endpoint(request: ChatRequest):
    # assemble messages for history
    messages = [
        {"role": "system", "content": "you are a helpful and concise assistant."},
        {"role": "user", "content": request.user_prompt}
    ]

    print(f'user: {request.user_prompt}')
    print(f'response stream:')

    # await the start of the stream
    stream = await async_ollama_client.chat(
        model=request.model_name,
        messages=messages,
        stream=True
    )
    
    # generator function to process and yield chunks
    async def generate_chunks():
        # iterate over the async generator from ollama
        async for chunk in stream:
            content = chunk.get('message', {}).get('content', '')
            if content:
                print(content)
                # yield content chunk for client consumption
                yield content.encode("utf-8")
            
    # return the streaming response
    return StreamingResponse(generate_chunks(), media_type="text/event-stream")


# --- non-streaming endpoint ---
@app.post("/chat/nonstream")
async def non_stream_chat_endpoint(request: ChatRequest):
    # build the messages array
    messages = [
        {"role": "system", "content": "you are a helpful and concise assistant."},
        {"role": "user", "content": request.user_prompt},
    ]
    print(f'user: {request.user_prompt}')
    print(f'response:')

    # await the call to get the final complete response
    response = await async_ollama_client.chat(
        model=request.model_name,
        messages=messages,
        stream=False
    )
    
    # extract the content
    final_content = response.get('message', {}).get('content', 'error: no response content found')
    print(final_content)

    # return a standard json response
    return {
        "model": request.model_name,
        "content": final_content,
        "finished": True,
    }
