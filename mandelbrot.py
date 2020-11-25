import pygame
import time
import math
from numpy import arange

black = (0, 0, 0)

class ImageDimensions:
    def __init__(self, width, height):
        self.width, self.height = width, height


    def __repr__(self):
        return '{' f'width={self.width}, height={self.height}' '}'


class MandelbrotImageGenerator:
    def __init__(self, min_x, min_y, max_x, max_y, max_iter, image_dims):
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y
        self.max_iter = max_iter
        self.image_dims = image_dims
        self.screen = None


    def init_screen(self):
        self.screen = pygame.display.set_mode((self.image_dims.width, self.image_dims.height))
        pygame.display.set_caption("MandelbrotImageGenerator")
        self.screen.fill(black)
        pygame.display.flip()


    def iterations_to_exit_set(self, x, y):
        x = float(x)
        y = float(y)
        prev_real = 0.0
        prev_imaginary = 0.0
        for counter in range(self.max_iter):
            cur_real = x + pow(prev_real, 2) - pow(prev_imaginary, 2)
            cur_imaginary = y + 2*(prev_real*prev_imaginary)
            abs_val = pow(cur_real, 2) + pow(cur_imaginary, 2)
            if abs_val >= 4:
                return counter
            prev_real = cur_real
            prev_imaginary = cur_imaginary
        return None


    def get_mapped_color(self, iterations):
        r = pow((iterations/self.max_iter), 64) * 255
        g = (pow((iterations/self.max_iter), 2) % 1) * 255
        b = (pow((iterations/self.max_iter), 2) * 30) + 225
        color = (r, g , b)
        return color


    def add_pixel(self, color, pos):
        self.screen.fill(color, (pos, (1, 1)))


    def draw_to_screen(self):
        x_step = (max_x - min_x)/float(self.image_dims.width)
        y_step = (max_y - min_y)/float(self.image_dims.height)
        x_pixel = 0
        for x in arange(self.min_x, self.max_x, x_step):
            y_pixel = 0
            for y in arange(self.min_y, self.max_y, y_step):
                iters = self.iterations_to_exit_set(x, y)
                if(iters is None): #was in the set
                    self.add_pixel(black, (x_pixel, y_pixel))
                else:
                    self.add_pixel(self.get_mapped_color(iters), (x_pixel, y_pixel))
                y_pixel+=1
            x_pixel+=1


    def generate_image(self, png_name=None):
        pygame.init()

        self.init_screen()
        self.draw_to_screen()

        if png_name is None:
            png_name = f'{self.min_x}_{self.min_y}_{self.max_x}_{self.max_y}_{self.image_dims.width}x{self.image_dims.height}_{self.max_iter}.png'

        pygame.image.save(self.screen, png_name)

        pygame.quit()


if __name__ == '__main__':
    min_x = -.75452 
    max_x = -.754243
    min_y = 0.05424
    max_y = 0.05443

    image_dims = ImageDimensions(1900, 1200)

    max_iter = 255

    mandelbrot_generator = MandelbrotImageGenerator(min_x, min_y, max_x, max_y, max_iter, image_dims)
    mandelbrot_generator.generate_image()

