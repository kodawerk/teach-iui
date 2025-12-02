import cv2
import requests
import base64
import io
import os
import time

OLLAMA_API_URL = "http://localhost:11434/api/generate" 
OLLAMA_MODEL = "llava" 
DEFAULT_PROMPT = "What do you see in this image? Provide a detailed description."
IMAGE_FILENAME = "captured_image.jpg"
TEMP_DIR = os.path.dirname(os.path.abspath(__file__)) + "/../temp"

def show_webcam_feed():
    cap = cv2.VideoCapture(0) 

    if not cap.isOpened():
        print("Error: webcam not accessible.")
        return None

    cv2.namedWindow("Live Webcam Feed (Press 'q' to capture and quit)")
    print("Opening live webcam feed. Press 'q' to capture the current frame and proceed.")
    
    # Wait for the camera to initialize
    time.sleep(1)

    # Frame to be captured later
    last_frame = None

    while True:
        ret, frame = cap.read() 
        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break
        
        # Display the frame
        cv2.imshow("Live Webcam Feed (Press 'q' to capture and quit)", frame)
        last_frame = frame # Keep the last successful frame
        
        # Wait for 1ms and check for key press
        # If 'q' (ASCII 113) is pressed, break the loop
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the capture and destroy all windows
    cap.release() 
    cv2.destroyAllWindows()
    
    return last_frame

def capture_image_from_frame(frame):
    if frame is None:
        print("Error: No frame available for capture.")
        return None
        
    filename=TEMP_DIR + "/" + IMAGE_FILENAME
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)

    cv2.imwrite(filename, frame)
    print(f"Stored snapshot as '{filename}'.")
    return filename


def send_image_to_llava(image_path, prompt=DEFAULT_PROMPT):
    if not os.path.exists(image_path):
        print(f"Error: image file '{image_path}' does not exist.")
        return

    try:
        # read image and encode to base64
        with open(image_path, "rb") as image_file:
            img_bytes = image_file.read()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')

        # request
        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "images": [img_base64],
            "stream": False 
        }

        print(f"\nSending '{image_path}' to Ollama LLaVA with Prompt: '{prompt}'")
        print("Please wait for the response...\n")

        response = requests.post(OLLAMA_API_URL, json=payload, timeout=300)
        response.raise_for_status()

        data = response.json()
        llava_response = data.get("response", "no response content")

        print("\n--- LLaVA Response ---")
        print(llava_response)
        print("----------------------\n")

    except requests.exceptions.Timeout:
        print("Error: Timeout")
    except requests.exceptions.ConnectionError:
        print("Error: Connection. Check http://localhost:11434?")
    except requests.exceptions.RequestException as e:
        print(f"Error: at LLaVA request {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    user_prompt = DEFAULT_PROMPT
    
    final_frame = show_webcam_feed()
    
    if final_frame is not None:
        captured_file = capture_image_from_frame(final_frame)
    else:
        captured_file = None

    if captured_file:
        send_image_to_llava(captured_file, user_prompt)
    else:
        print("Error: No image captured, aborting.")