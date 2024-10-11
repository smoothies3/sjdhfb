# -*- coding: utf-8 -*-
import cv2
import numpy as np
import matplotlib.pyplot as plt
import logging

logging.basicConfig(level=logging.INFO)

class VideoProcessor:
    def __init__(self, video_path, start_time, end_time, color_palette):
        self.video_path = video_path
        self.start_time = start_time
        self.end_time = end_time
        self.color_palette = color_palette
        self.cap = None
        self.density_map = None

    def open_video(self):
        self.cap = cv2.VideoCapture(self.video_path)
        if not self.cap.isOpened():
            logging.error("Error opening video file")
            return False
        return True

    def initialize_density_map(self):
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.density_map = np.zeros((height, width), dtype=np.float32)

    def process_frames(self):
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        start_frame = int(self.start_time * fps)
        end_frame = int(self.end_time * fps)

        backSub = cv2.createBackgroundSubtractorMOG2()
        
        for frame_num in range(start_frame, end_frame):
            ret, frame = self.cap.read()
            if not ret:
                break
            
            self.process_frame(frame, backSub)

    def process_frame(self, frame, backSub):
        fg_mask = backSub.apply(frame)
        fg_mask = cv2.GaussianBlur(fg_mask, (5, 5), 0)
        _, thresh = cv2.threshold(fg_mask, 30, 255, cv2.THRESH_BINARY)

        # Морфологические операции для удаления мелкого шума
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

        self.filter_motion(thresh, frame)
        self.density_map += thresh

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return

    def filter_motion(self, thresh, frame):
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 1000:  # Фильтр для удаления малых объектов
                if self.is_relevant_movement(contour):
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def is_relevant_movement(self, contour):
        # Фильтрация на основе соотношения сторон и площади
        area = cv2.contourArea(contour)
        if area < 500:  # Дополнительный фильтр по площади
            return False

        # Пример проверки соотношения сторон
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = float(w) / h
        if 0.2 < aspect_ratio < 5:  # Фильтрация по соотношению сторон
            return True
        return False

    def show_density_map(self):
        plt.imshow(self.density_map, cmap=self.color_palette)
        plt.colorbar()
        plt.title("Density Map")
        plt.axis('off')
        plt.show()

    def process_video(self):
        if not self.open_video():
            return
        self.initialize_density_map()
        self.process_frames()
        self.cap.release()
        cv2.destroyAllWindows()
        self.show_density_map()


def process_video(video_path, start_time, end_time, color_palette):
    processor = VideoProcessor(video_path, start_time, end_time, color_palette)
    processor.process_video()
