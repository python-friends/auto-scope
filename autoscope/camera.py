
from .utils import log
try:
    from picamera import PiCamera
    from picamera.array import PiRGBArray
except ImportError:
    log.warning("picamera not found! Using picamera fake module.")
    from .fakes.picamera import PiRGBArray, PiCamera

import time
import cv2
import numpy as np
from math import sqrt

class Camera:
    def __init__(self, focus):
        self.zoom = None
        self.focus = focus

    def take_photo(self, resolution=(640, 640), zoom=(0,0,1,1), scale=1):
        resolution = (resolution[0]*scale, resolution[1]*scale)
        with PiCamera() as camera:
            camera.resolution = resolution
            camera.zoom = zoom
            with PiRGBArray(camera) as stream:
                camera.capture(stream, format='bgr')
                # At this point the image is available as stream.array
                return stream.array

    def get_tile(self, resolution=(640, 640), scale=1):
        if self.zoom == None:
            self.zoom = self.calulate_zoom(self.take_photo())
        img = self.take_photo(resolution=resolution, zoom=self.zoom, scale=scale)
        return img
        
    def calulate_zoom(self, BGRimg, scaling_value=0.75):
        BWimg = self.convert_BGR_BW(BGRimg)
        height,width = BWimg.shape
        cX, cY, r = self.find_circle(BWimg)
        side_length = self.square_side_length_from_bounding_circle(cX, cY, r, scaling_value=scaling_value)
        xpos = cX - side_length/2
        ypos = cY - side_length/2
        return (xpos/width, ypos/height, side_length/width, side_length/height)
    
        
    def square_side_length_from_bounding_circle(self, center_x, center_y, r, scaling_value=1):
        side_length = int((r*2/sqrt(2)) * scaling_value)  # https://en.wikipedia.org/wiki/Special_right_triangle
        return side_length
    
    def square_coords_from_bounding_circle(self, center_x, center_y, r, scaling_value=1):
        side_lenght = self.square_side_length_from_bounding_circle(
            center_x, center_y, r
        ) 
        delta = int(((side_lenght) / 2) * scaling_value)
        x1 = center_x - delta
        y1 = center_y - delta
        x2 = center_x + delta
        y2 = center_y + delta
        return (x1, y1, x2, y2)

    def auto_crop_image(self, BWimg, tol=0):
        # img is image data
        # tol  is tolerance
        bool_mask = BWimg>tol
        return BWimg[np.ix_(bool_mask.any(1),bool_mask.any(0))]

    def find_circle(self, BWimg):
        crop = self.auto_crop_image(BWimg)
        r = int(max(crop.shape)/2)
        # find center (in original image) https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/
        M = cv2.moments(BWimg) # I'm not sure how well this work for crops. 
        x = int(M["m10"] / M["m00"])
        y = int(M["m01"] / M["m00"])
        return (x, y, r)

    def convert_BGR_BW(self, BGRimg, thresh=10):
        GRAYimg = cv2.cvtColor(BGRimg, cv2.COLOR_BGR2GRAY)
        BWimg = cv2.threshold(GRAYimg, thresh, 255, cv2.THRESH_BINARY)[1]
        return BWimg

    def scan_down_generator(self, step_size, max_steps, scale=1):
        max_pos = self.focus.zpos - abs(max_steps)
        while self.focus.zpos > max_pos:
            yield self.get_tile(scale=scale)
            self.focus.down(step_size)
    
    def scan_up_generator(self, step_size, max_steps, scale=1):
        max_pos = self.focus.zpos + abs(max_steps)
        while self.focus.zpos < max_pos:
            yield self.get_tile(scale=scale)
            self.focus.up(step_size)
            
            
    def scan(self, stepsize=10, maxsteps=200, thresh=100, direction=-1):
        zpos = []
        blur = []
        sweetspot = False
        if direction == 1:
            image_gen = self.scan_up_generator(stepsize, maxsteps)
        else:
            image_gen = self.scan_down_generator(stepsize, maxsteps)
        for i, img in enumerate(image_gen):
            zpos.append(self.focus.zpos)
            b = max([self.variance_of_laplacian(img) for _ in range(3)])
            print(b)
            blur.append(b)
            if b > thresh:
                sweetspot = True
            if len(blur) == 1:
                continue
            if sweetspot and b < blur[-2]:
                return zpos, blur
        print("Failed to focus")
        return False

    def find(self, stepsize=1, maxsteps=50, blur_target=100, direction=-1):
        zpos = []
        blur = []
        if direction == 1:
            image_gen = self.scan_up_generator(stepsize, maxsteps)
        else:
            image_gen = self.scan_down_generator(stepsize, maxsteps)
        for i, img in enumerate(image_gen):
            zpos.append(self.focus.zpos)
            b = max([self.variance_of_laplacian(img) for _ in range(3)])
            print(b)
            blur.append(b)
            if b >= blur_target:
                return True
        print("Failed to focus")
        return False

    def variance_of_laplacian(self, img):
        return cv2.Laplacian(img, cv2.CV_64F).var()

    def rateFocusByLaplacianGrid(self, img, squares=4):
        squares = int(sqrt(squares))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        maxFocus = 0
        h = int(img.shape[0] / squares)
        w = int(img.shape[1] / squares)
        for i in range(squares):
            for j in range(squares):
                roi_gray = img[i*h:i*h+h, j*w:j*w+w]
                b = self.variance_of_laplacian(roi_gray)
                if b > maxFocus:
                    maxFocus = b
        return maxFocus