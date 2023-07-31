import websockets
import asyncio
import cv2
import multiprocessing

async def listen():
    url = "ws://192.168.212.190:80/CarInput"  # Make sure to use "ws://" instead of "http://"

    async with websockets.connect(url) as ws:
        while True:
            data = input("Enter data to send to the server: ")
            await ws.send(data)  # Use ws.send() to send data

def display_video_feed():
    url = "http://192.168.212.190:81"  # Replace with the URL of the video feed

    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        print("Error: Unable to connect to the video feed.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to retrieve frame from the video feed.")
            break

        cv2.imshow("Video Feed", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    video_process = multiprocessing.Process(target=display_video_feed)
    video_process.start()

    asyncio.run(listen())
