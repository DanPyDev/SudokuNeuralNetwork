from PIL import ImageDraw, ImageFont

def convert_sudoku_txt_to_image(data,im,font):
    """ Converts a sudoku passed as an array of 81 integers to the corresponding image.
        Does not alter the input image.
        Parameters:
        ---------------
        data    sudoku representative array of 81 integers
        im      blank sudoku grid image to be filled
        
        Returns:
        ---------------
        im1     sudoku grid image with the corresponding sudoku from data
    """
    li=24
    im1 = im.copy()
    d = ImageDraw.Draw(im1)
    fnt = ImageFont.truetype(font, 28)
    for i in range(0,9):
        for j in range(0,9):
            if (data[j+9*i]!=0):          
                d.text((li+8+i*im1.size[0]/10.8,li+2+j*im1.size[1]/10.9), str(data[j+9*i])[0],font=fnt, fill=0)
    return im1