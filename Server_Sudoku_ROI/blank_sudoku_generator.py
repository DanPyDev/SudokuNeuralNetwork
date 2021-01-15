import numpy as np
from PIL import Image, ImageDraw

def image_blanck_generator():
    a = np.uint8(np.zeros((300,300)))
    for i in range(0, a.shape[0]):
        for j in range(0, a.shape[1]):
            a[i][j] = 255

    im = Image.fromarray(a,'L')

    draw = ImageDraw.ImageDraw(im)

    dim=250
    li = 25
    #major frame
    draw.line([(0,0), (0, im.size[1])], fill=0,width=6)
    draw.line([(0,0), (im.size[0],0)], fill=0,width=6)
    draw.line([(0,im.size[1]), (im.size[0], im.size[1])], fill=0,width=10)
    draw.line([(im.size[0],0), (im.size[0],im.size[1])], fill=0,width=10)
    #main frame
    draw.line([(li,li), (li, dim+li)], fill=0,width=4)
    draw.line([(li,li), (dim+li,li)], fill=0,width=4)
    draw.line([(li,li+dim), (li+dim, dim+li)], fill=0,width=4)
    draw.line([(dim+li, li), (dim+li,dim+li)], fill=0,width=4)
    #main divisions
    draw.line([(li,li+2*dim/3), (dim+li, li+2*dim/3)], fill=0,width=3)
    draw.line([(li+dim/3, li), (li+dim/3, li+dim)], fill=0,width=3)
    draw.line([(li, li+dim/3), (li+dim, li+dim/3)], fill=0,width=3)
    draw.line([(li+2*dim/3, li), (li+2*dim/3, li+dim)], fill=0,width=3)
    #smaller divisions
    draw.line([(li,li+2*dim/9), (li+dim, li+2*dim/9)], fill=0)
    draw.line([(li+dim/9, li), (li+dim/9, li+dim)], fill=0)
    draw.line([(li, li+dim/9), (li+dim, li+dim/9)], fill=0)
    draw.line([(li+2*dim/9, li), (li+2*dim/9, li+dim)], fill=0)
    draw.line([(li,li+4*dim/9), (li+dim, li+4*dim/9)], fill=0)
    draw.line([(li+4*dim/9, li), (li+4*dim/9, li+dim)], fill=0)
    draw.line([(li,li+5*dim/9), (li+dim, li+5*dim/9)], fill=0)
    draw.line([(li+5*dim/9, li), (li+5*dim/9, li+dim)], fill=0)
    draw.line([(li,li+7*dim/9), (li+dim, li+7*dim/9)], fill=0)
    draw.line([(li+7*dim/9, li), (li+7*dim/9, li+dim)], fill=0)
    draw.line([(li,li+8*dim/9), (li+dim, li+8*dim/9)], fill=0)
    draw.line([(li+8*dim/9, li), (li+8*dim/9, li+dim)], fill=0)

    draw.ellipse((10, 10, 20, 20), fill=128)

    return im