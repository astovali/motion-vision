import cv2
import random
import numpy as np
from itertools import product

def rpixel():
    return np.array([int(random.random()*255) for i in range(3)])

class VideoConverter:

    def __init__(self, input_video, output_video, frameSize):
        self.input_video = input_video 
        self.output_video = output_video
        self.change_threshold = 100
        self.frameSize = frameSize

    def convert(self):
        if not self.input_video.isOpened():
            print("Error: Cannot open input video.")
            return
        
        # Initialize image with random pixels
        image = np.zeros((self.frameSize[1], self.frameSize[0], 3), dtype=np.uint8)
        for y, x in product(range(self.frameSize[1]), range(self.frameSize[0])):
            image[y, x] = rpixel()

        while self.input_video.isOpened():
            ret, frame = self.input_video.read()
            if not ret:
                break

            # Process each pixel
            for y, x in product(range(self.frameSize[1]), range(self.frameSize[0])):
                brightness = sum(frame[y, x]) // 3
                if brightness < self.change_threshold:
                    image[y, x] = rpixel()
            
            self.output_video.write(image)

        self.input_video.release()
        self.output_video.release()
        cv2.destroyAllWindows()

input_filename = input("Filename: ")
input_video = cv2.VideoCapture(input_filename)

fps = input_video.get(cv2.CAP_PROP_FPS)
width = int(input_video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(input_video.get(cv2.CAP_PROP_FRAME_HEIGHT))

output_video = cv2.VideoWriter(
    "output.avi", 
    cv2.VideoWriter_fourcc(*'MJPG'),
    fps, 
    (width, height), 
    True
)

converter = VideoConverter(input_video, output_video, (width, height))
converter.convert()

