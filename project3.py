# CPS121 Project 3
# Written: <11/12> <Simon Voyer> <Simon.Voyer@gordon.edu>
# 
# <Include description of program here>
##
# Change each occurrence of "_" in the list below to be "Y" or "N" to indicate
# whether or not the given transformation is implemented in your program.
#
#   Can be done using just getPixels()
#   Y Altering colors of the image
#   Y Grayscale
#   Y Making darker or lighter
#   Y Sepia-toned
#   Y Posterized
#   Need nested loops
#   Y Mirrorizing
#   Y Edge detection
#   Y Chromakey (change background)
#   N Blurring
#   Need nested loops and alter size or shape
#   Y Rotation
#   Y Cropping
#   Y Shifting
#   Other transformations
#   _ <description of transformation>
#   _ <description of transformation>
#   _ <description of transformation>
# ============================================================================

import GCPictureTools as pgt
import pygame as pg
import os, sys
import traceback


# ============================================================================
# ================ Start making changes after this comment ===================
# ============================================================================

# ---- SUPPORTING FUNCTIONS SHOULD GO HERE ----

def createCollage():
    """Create a collage.
 
    Returns
    -------
    Picture
        the collage.
    """
    # create "canvas" on which to make a collage.  You may exchange the
    # width and height values if you prefer a landscape orientation.
    collage = pgt.Picture(1400, 900)

    # ---- YOUR CODE TO BUILD THE COLLAGE GOES HERE ----
    # Notice that this is **inside** the createCollage() function.  Because
    # createCollage() should be a "one-and-only-one-thing" function, you
    # should use supporting functions to do transformations, etc.  These
    # supporting functions should be defined below, after the code for this
    # function.

    #Turns picture red by reducing the amount of green and blue
    def makeRed(picture):
        for x in range(0, picture.getWidth()):
            for y in range(0, picture.getHeight()):
                p = picture.getPixel(x, y);
                p.setBlue(p.getBlue()*0.5)
                p.setGreen(p.getGreen()*0.5)
    
    #Turns picture gray by averaging the colors
    def grayScale(picture):
        for x in range(0, picture.getWidth()):
            for y in range(0, picture.getHeight()):
                p = picture.getPixel(x, y);
                value = (p.getRed() + p.getGreen() + p.getBlue())/3
                p.setRed(value)
                p.setGreen(value)
                p.setBlue(value)

    #Turns picture into whatever sepia is by tinting colors
    def sepiaTint(picture):
        grayScale(picture)
        for x in range(0, picture.getWidth()):
            for y in range(0, picture.getHeight()):
                p = picture.getPixel(x, y);
                red = p.getRed()
                blue = p.getBlue()
                #tint shadows
                if (red < 63):
                    red = red*1.1
                    blue = blue*0.9
                #tint midtones
                if (red > 62 and red < 192):
                    red = red*1.15
                    blue = blue*0.85
                #tint highlights
                if (red > 191):
                    red = red*1.08
                if (red > 255):
                    red = 255
                    blue = blue*0.93
                #set the new color values
                p.setBlue(blue)
                p.setRed(red)

    #Polarizes picture by changing color values very spefically
    def polarize(picture):
        for x in range(0, picture.getWidth()):
            for y in range(0, picture.getHeight()):
                pix = picture.getPixel(x, y);
                newRed = pix.getRed() * 0.299
                newGreen = pix.getGreen() * 0.587
                newBlue = pix.getBlue() * 0.114
                color = 255 - (newRed + newGreen + newBlue)
                # set Color of pix as(color, color, color)
                picture.setColor(x,y, (color, color, color))

    #Rotates picture 90 degrees to the right
    def rotate90R(pic):
        width = pic.getWidth()
        height = pic.getHeight()
        #make an empty picture
        canvas = pgt.Picture(height, width)
        for col in range(0, width):
            for row in range(0, height):
                color = pic.getColor(col, row)
                canvas.setColor(height-1-row, col, color)
        return canvas
    
    #Rotates picture 90 degrees to the left
    def rotate90L(pic):
        width = pic.getWidth()
        height = pic.getHeight()
        #make an empty picture
        canvas = pgt.Picture(height, width)
        for col in range(0, width):
            for row in range(0, height):
                color = pic.getColor(col, row)
                canvas.setColor(row, width-1-col, color)
        return canvas
    
    #Rotates picture any number of time in either direction without any delay
    def betterRotate(pic, direction, number):
        canvas = pic
        for i in range(number%4):
            if direction == 'r':
                canvas = rotate90R(canvas)
            elif direction == 'l':
                canvas = rotate90L(canvas)
        return canvas
    
    #Crops picture to chosen size
    def cropIt(pic, newWidth, newHeight):
        oldWidth = pic.getWidth()
        oldHeight = pic.getHeight()
        picWidth = (oldWidth - newWidth) // 2
        picHeight = (oldHeight - newHeight) // 2
        canvas = pgt.Picture(newWidth, newHeight)
        for col in range(newWidth):
            for row in range(newHeight):
                color = pic.getColor(picWidth + col, picHeight + row)
                canvas.setColor(col, row, color)
        return canvas
    
    #Highlights blues in the picture by turn anything mostly blue fully blue
    def turnBlue(pic):
        canvas = pic
        for p in pic.getPixels():
            red = p.getRed()
            green = p.getGreen()
            blue = p.getBlue()
            if blue > red and blue > green:
                p.setBlue(255)
        return canvas
    
    #Dectects edges of that picture
    def edge(canvas):
        """Do edge detection in a picture"""
        height= canvas.getHeight()
        width = canvas.getWidth()
        for p in canvas.getPixels():   
            red = p.getRed()
            green = p.getGreen()
            blue = p.getBlue()
            x = p.getX()
            y = p.getY()
            p1=  pgt.Pixel(p.getPicture(), p.getX()+1, p.getY()+1)
            if y < height-1 and x < width-1:
                sum = red+green+blue
                sum2 = p1.getRed()+p1.getGreen() + p1.getBlue() 
                diff = min(255, abs(sum2-sum))
                canvas.setColor(p.getX(),p.getY(), (diff, diff, diff))

    #Mirrors picture by copying one side to the other
    def mirror(pic):
        width = pic.getWidth()
        height = pic.getHeight()
        for row in range(height):
            for col in range(width//2):
                color = pic.getColor(col, row)
                pic.setColor(width-1-col, row, color)
        return pic
    

    #Prints out the Collage
    pic1 = pgt.Picture('G.jpg')
    pic2 = pgt.Picture('M.jpeg')
    pic3 = pgt.Picture('C.png')

    pic1.copyInto(collage, -150, 0)
    pic2.copyInto(collage, 1200, 650)
    pic3.copyInto(collage, 235, 650)

    makeRed(pic1)
    pic1b = mirror(pic1)
    pic1b.copyInto(collage, 300, 0)
    grayScale(pic1)
    pic1 = cropIt(pic1, 250, 600)
    pic1.copyInto(collage, 900, 0)
    polarize(pic1)
    pic1 = cropIt(pic1, 250, 600)
    pic1 = betterRotate(pic1, 'r', 2)
    pic1.copyInto(collage, 1150, 0)

    turnBlue(pic2)
    pic2 = betterRotate(pic2, 'r', 1)
    pic2.copyInto(collage, 975, 650)
    grayScale(pic2)
    pic2 = betterRotate(pic2, 'r', 2)
    pic2.copyInto(collage, 750, 650)
    sepiaTint(pic2)
    pic2 = betterRotate(pic2, 'l', 101)
    pic2.copyInto(collage, 525, 650)

    polarize(pic3)
    edge(pic3)
    pic3.copyInto(collage, 0, 650)


    
    
    return collage

def createWebPage(imageFile, webPageFile):
    """Create web page that contains the collage.
    Parameter: imageFile - the image file name 
    Parameter: webPageFile - the finename of the output web page 
    Returns
    -------
    nothing
    """

    htmlFile = open(webPageFile, "wt")

    htmlFile.write("<!DOCTYPE html>\n")
    htmlFile.write("<html>\n")
    htmlFile.write("<head>\n")
    htmlFile.write(f"<title>Simon Voyer's Epic Collage</title>\n")
    htmlFile.write("</head>\n")
    htmlFile.write("<body>\n")
    htmlFile.write(f"<h4>This is my awesome Collage</h4>\n")
    htmlFile.write(f"<p>Look at all of the cool images that were created!</p>\n")
    htmlFile.write(f"<img src='Collage.png'/>\n")
    htmlFile.write("</body>\n")
    htmlFile.write("</html>\n")

    print("output file:", htmlFile.name)
    htmlFile.close()    







# ============================================================================
# ============== Do NOT make any changes below this comment ==================
# ============================================================================

if __name__ == '__main__':

    # first command line argument, if any, is name of image file for output
    # second command line argument, if any, is name of the output html file name
    collageFile = None
    htmlFileName = "webpage.html"  #Default name

    if len(sys.argv) > 1:
        collageFile = sys.argv[1]
    if len(sys.argv) > 2:
        htmlFile = sys.argv[2]    

    # temporarily set media path to project directory
    scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))

    # create the collage
    
    collage = createCollage()
    #collage.display()

    try:
        # either show collage on screen or write it to file
        if collageFile is None:
            collage.display()
            input('Press Enter to quit...')
        else:
            print(f'Saving collage to {collageFile}')
            collage.save(collageFile)
            createWebPage(collageFile, htmlFileName)
    except:
        print('Could not show or save picture')

