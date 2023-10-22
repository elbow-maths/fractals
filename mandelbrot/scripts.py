from PIL import Image
from dataclasses import dataclass
from math import log
from PIL import ImageEnhance
from matplotlib import colormaps as cm
import numpy as np
from scipy.interpolate import interp1d



@dataclass
class MandelbrotSet:
    max_iterations: int
    escape_radius: float = 2.0
    
    def __contains__(self, c:complex) -> bool:
        return self.stability(c) == 1
    
    def stability(self, c:complex, smooth=False, clamp=True) -> float:
        value = self.escape_count(c,smooth)/self.max_iterations
        return max(0.0,min(value,1.0)) if clamp else value

    def escape_count(self, c:complex, smooth=False) -> int|float:
        z=0
        for iteration in range(self.max_iterations):
            z=z**2+c
            if abs(z) > self.escape_radius:
                if smooth:
                    return iteration+1-log(log(abs(z)))/log(2)
                return iteration
        return self.max_iterations

@dataclass
class Viewport:
    image: Image.Image
    center: complex
    width: float
    
    @property
    def height(self):
        return self.scale * self.image.height
    
    @property
    def offset(self):
        return self.center + complex(-self.width,self.height)/2
    
    @property
    def scale(self):
        return self.width / self.image.width
    
    def __iter__(self):
        for y in range(self.image.height):
            for x in range(self.image.width):
                yield Pixel(self,x,y)

@dataclass
class Pixel:
    viewport: Viewport
    x: int
    y: int
    
    @property
    def colour(self):
        return self.viewport.image.getpixel((self.x,self.y))
    
    @colour.setter
    def colour(self,value):
        self.viewport.image.putpixel((self.x,self.y),value)
    
    def __complex__(self):
        return (
                complex(self.x,-self.y)
                * self.viewport.scale
                + self.viewport.offset
        )

def paint(mandelbrot_set,viewport,palette,smooth):
    for pixel in viewport:
        stability = mandelbrot_set.stability(complex(pixel),smooth)
        index = int(min(stability * len(palette),len(palette)-1))
        pixel.colour = palette[index % len(palette)]
        
def denormalise(palette):
    return [
        tuple(int(channel*255) for channel in colour)
        for colour in palette
    ]

def make_gradient(colours, interpolation="linear"):
    X = [i/(len(colours)-1) for i in range(len(colours))]
    Y = [[colour[i] for colour in colours] for i in range(3)]
    channels = [interp1d(X,y,kind=interpolation) for y in Y]
    return lambda x: [np.clip(channel(x),0,1) for channel in channels]
