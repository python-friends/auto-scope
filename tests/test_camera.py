import pytest
from autoscope import Focus, Camera
import cv2

class TestCamera():
    def setup(self):
        self.camera = Camera(Focus([9,10,11,12]))
        self.test_BGR_image = cv2.imread('tests/test_images/test_BGR_image.jpg') 
        self.test_BGR_tile = cv2.imread('tests/test_images/test_BGR_tile.jpg') 
        
    def test_focus_attr(self):
        if not hasattr(self.camera, "focus"):
            pytest.fail("Camera does not have attribute 'focus'")

    def test_calulate_zoom(self):
        zoom = self.camera.calulate_zoom(
            self.test_BGR_image
        ) 
        zoom = [round(i, 1) for i in zoom]
        assert zoom == [0.3, 0.3, 0.3, 0.4]
        
    def test_convert_BGR_BW(self):
        assert self.camera.convert_BGR_BW(
            self.test_BGR_image
        ).shape == (1536, 2048)
    
    def test_find_circle(self):
        self.camera.find_circle(
            self.camera.convert_BGR_BW(self.test_BGR_image)
        ) == (1023, 767, 1024)
        
    def test_square_side_length_from_bounding_circle(self):
        assert self.camera.square_side_length_from_bounding_circle(
            1023, 767, 1024
        ) == 1448
        
    def test_square_coords_from_bounding_circle(self):
        assert self.camera.square_coords_from_bounding_circle(
            1023, 767, 1024
        ) == (299, 43, 1747, 1491)
        
    def test_auto_crop_image(self):
        assert self.camera.auto_crop_image(
            self.camera.convert_BGR_BW(self.test_BGR_image)
        ).shape == (1199, 1216)
        
   
    def test_variance_of_laplacian(self):
        assert int(self.camera.variance_of_laplacian(
            self.test_BGR_tile
        )) == 252
        
        
    def rateFocusByLaplacianGrid(self):
        assert self.camera.variance_of_laplacian(
            self.test_BGR_tile
        ) == 277.88635379592876
        
    
    