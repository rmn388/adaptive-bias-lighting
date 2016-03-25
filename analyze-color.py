from PIL import Image, ImageGrab, ImageDraw
from numpy import array
from scipy.cluster.vq import  kmeans #, whiten, vq
import time
import serial
import serial.tools.list_ports
import timeit






def image_open():
    #image = Image.open("mountain.jpg")
    image = ImageGrab.grab(bbox=None)
    return image

def rgb_pixel_array():
    for x in range(0,img.width):
        for y in range(0,img.height):
            rgbpx = img.getpixel((x,y))
            rgb_array.append([float(rgbpx[0]),float(rgbpx[1]),float(rgbpx[2])])
    return rgb_array

def check_colors(color_array):
    brightest = 0
    most_saturated = 0
    brightest_value = 0
    darkest_value = 768
    most_saturated_value = 0
    for x,colors in enumerate(color_array):
        rgb_sum = sum(colors)
        if rgb_sum > brightest_value:
            brightest = x
            brightest_value = rgb_sum
        if rgb_sum < darkest_value:
            darkest = x
            darkest_value = rgb_sum
        for color in colors:
            for color2 in colors:
                color_dif = abs(color-color2)
                if color_dif > most_saturated_value:
                    most_saturated = x
                    most_saturated_value = abs(color-color2)
        
    return brightest, most_saturated, darkest
    
def draw_on_image():
    img_full = image_open()
    draw = ImageDraw.Draw(img_full)
    for x,color in enumerate(sorted_colors):#range(k)):#
        draw.rectangle([(img_full.width*x/3, img_full.height*9/10),(img_full.width*(x+1)/3,img_full.height)], fill=rgb_tuples[color],outline=None)
        #draw.rectangle([(img_full.width*(x)/20, 0),(img_full.width*(x+1)/20,img_full.height)], fill=rgb_tuples[color],outline=None)
    del draw
    img_full.show()
    return


if __name__ == '__main__':
    k = 4
    #ports = list(serial.tools.list_ports.comports())
    #print (ports[1])
    try: #Attempts to connect to arduino serial usb port
      ser = serial.Serial('COM6', 9600, timeout=0)
    except:
      ser = serial.Serial('COM6', 9600, timeout=0)   
    time.sleep(2) #gives time to connect
    
    while True:
        start = timeit.default_timer()
        img = image_open()
        img.thumbnail((100,100))
        
        rgb_array = []    
        
        rgb_array = rgb_pixel_array()
        vector, distortion = kmeans(array(rgb_array),k)
        sorted_colors = check_colors(vector)
        
        rgb_tuples = [tuple(l) for l in vector.astype(int)]
        
        red,green,blue = rgb_tuples[sorted_colors[1]]
        stop = timeit.default_timer()
        print(red,green,blue)
        green = (green + 2 // 2) // 2
        blue = (blue + 2 // 3) // 3
        print(red,green,blue)
        rgb_led = "0{}r,0{}g,0{}b,".format(red,green,blue).encode()
        #print(rgb_led)
        ser.write(rgb_led)
        print(stop-start)

    #draw_on_image()
