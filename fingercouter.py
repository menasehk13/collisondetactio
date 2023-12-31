import asyncio
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import websockets

detector = HandDetector(maxHands=1, detectionCon=0.8)
video = cv2.VideoCapture("http://192.168.212.190:81")

async def main():
    url = "ws://192.168.212.190:80/CarInput"
    async with websockets.connect(url) as ws:
        print("connected")
        while True:
            _, img = video.read()
            img = cv2.flip(img, 1)
            hand = detector.findHands(img, draw=False)
            if hand:
                lmlist = hand[0]
                if lmlist:
                    fingerup = detector.fingersUp(lmlist)
                    if fingerup == [0, 0, 0, 0, 0]:
                        print("0")
                        await ws.send("s")
                        cv2.putText(img, f'Stop: {int(0)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    # Rest of the fingerup conditions...

            cv2.imshow("Video", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0.1)  # Add a delay to avoid rapid signals

    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    asyncio.run(main())
