import math
import random
import copy
import numpy as np
from scipy import ndimage
from skimage import io, transform
 
def noiser(img):
    for i in range(len(img)):
        for j in range(len(img[i])):
            noise = random.randint(0,3)
            if noise == 1:
                colorOne = random.randint(0,255)
                colorTwo = random.randint(0,255)
                colorThree = random.randint(0,255)
                '''
                if color ==0:
                    img[i][j][0] = 0
                    img[i][j][1] = 0
                    img[i][j][2] = 0
                else:
                    img[i][j][0] = 255
                    img[i][j][1] = 255
                    img[i][j][2] = 255
                '''
                img[i][j][0] = colorOne
                img[i][j][1] = colorTwo
                img[i][j][2] = colorThree
    return img
 
def spiral(img):
    temp = 0
    start = 0
    dup = copy.deepcopy(img)
    for i in range(len(img)):
        for j in range(len(img[i])):
            if j+temp > len(img[i])-1:
                #img[i][((j+temp)-len(img[i]))] = dup[i][j]
                img[i][start] = dup[i][j]
                start+=1
            else:
                newRow = j+temp
                img[i][newRow] = dup[i][j]
        #temp = random.randint(0, len(img[i]))
       
        temp+=1
        start = 0
       
    return img
 
def scrambler(img):
    temp = 0
    start = 0
    dup = copy.deepcopy(img)
    #scrambles horizontally
    for i in range(len(img)):
        for j in range(len(img[i])):
            if j+temp > len(img[i])-1:
                #img[i][((j+temp)-len(img[i]))] = dup[i][j]
                img[i][start] = dup[i][j]
                start+=1
            else:
                newRow = j+temp
                img[i][newRow] = dup[i][j]
        temp = random.randint(0, len(img[i]))
       
        start = 0
    #scrambles vertically
    for j in range(len(img[i])):
        for i in range(len(img)):
            if i+temp > len(img)-1:
                #img[i][((j+temp)-len(img[i]))] = dup[i][j]
                img[start][j] = dup[i][j]
                start+=1
            else:
                newCol = i+temp
                img[newCol][j] = dup[i][j]
        temp = random.randint(0, len(img))
       
        start = 0
       
       
    return img
 
def staticSpook(img):
    for i in range(len(img)):
        for j in range(len(img[i])):
            temp = random.randint(0, 100)
            img[i][j][0] = img[i][j][0] - temp
            temp = random.randint(0, 100)
            img[i][j][1] = img[i][j][1] - temp
            temp = random.randint(0, 100)
            img[i][j][2] = img[i][j][2] - temp
    return img
 
def glassDoor( img ):
    for i in range( len( img ) ):
        if i%2 == 1:
            #loop through each odd row
            for j in range( len( img[i] ) ):
                subVal = abs(math.ceil( 10*math.sin(i) ))
                img[i][j], img[i-subVal][j] = img[i-subVal][j], img[i][j]
    return img
 
def bubble( img ):
    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            dist = math.sqrt( (i - 130)**2 + (j - 130)**2 )
            if dist < 90:
                img[i][j][0] = 255
    return img

#ask Tim about 4 blocks and stuff like that
 
def blocks( img ):
    channelT = len(img[0][0])


    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            if math.cos(i*len(img)) * math.sin(j*len(img[i])) < 0.15:
                if channelT == 3:
                    img[i][j] = [0, 0, 0]
                if channelT == 4:
                    img[i][j] = [0, 0, 0, 0]
    return img


 
def hardSpiral( img ):
    channelT = len(img[0][0])

    spiral = io.imread( 'imageProc/static/uploads/spiral.png' )
    spiralSize = transform.resize( spiral, (img.shape[0],img.shape[1]) )
    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            if spiralSize[i][j][3] > 0:

                if channelT == 3:
                    img[i][j] = [0, 0, 0]
                if channelT == 4:
                    img[i][j] = [0, 0, 0, 0]

    return img
 
def blueOverlay( img ):
    blue = transform.resize( io.imread( 'imageProc/static/uploads/blue.jpg' ), (img.shape[0],img.shape[1]) )
    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            for k in range(3):
                #img[i][j][k] = blue[i][j][k]*255
                img[i][j][k] = (blue[i][j][k]*255 * 0.3 + img[i][j][k] * 0.7)
    return img
 
def waves( img ):
    channelT = len(img[0][0])


    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            if math.cos(i*len(img)) + math.sin(j*len(img[i])) < 0.15:
                #img[i][j] = [0, 0, 0]
                if channelT == 3:
                    img[i][j] = [0, 0, 0]
                if channelT == 4:
                    img[i][j] = [0, 0, 0, 0]
    return img
 
def circ( img ):
    centerX = math.floor(len(img[0])/2)
    centerY = math.floor(len(img)/2)

    channelT = len(img[0][0])
   
    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            distFromCenter = math.sqrt( i**2 + j**2 )
            if i == centerY:
                curAng = 0
            else:
                curAng = math.atan( (j-centerX) / (i-centerY) )
            #if curAng * distFromCenter % 20 < 8:
            if j == round(distFromCenter * math.cos( curAng ))  or i == round(distFromCenter * math.sin( curAng )):
                #img[i][j] = [0, 0, 0]
                if channelT == 3:
                    img[i][j] = [0, 0, 0]
                if channelT == 4:
                    img[i][j] = [0, 0, 0, 0]
               
    return img
 
 
'''def bnwMT( img ):
    start = time.time()
    def pixBnw( rownum ):
        for i in range( rownum ):
            ave = img[rownum][i][0] * 0.299 + img[rownum][i][1] * 0.587 + img[rownum][i][2] * 0.114
            img[rownum][i][0], img[rownum][i][1], img[rownum][i][2] = ave, ave, ave
           
    ts = []
    for i in range( len( img ) ):
        ts.append( threading.Thread(target=pixBnw, args=(i,)) )
    [t.start() for t in ts]    
    [t.join() for t in ts]
   
    print( time.time() - start )
    return img
   
def pixBnw( imgsec, procnum, return_dict ):
        for i in range( len(imgsec) ):
            for j in range( imgsec[i] ):
                ave = imgsec[i][j][0] * 0.299 + imgsec[i][j][1] * 0.587 + imgsec[i][j][2] * 0.114
                imgsec[i][j][0], imgsec[i][j][1], imgsec[i][j][2] = ave, ave, ave
        return_dict[procnum] = imgsec
 
def bnwMP( img ):    
    start = time.time()
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
   
    procSize = math.ceil( len(img) / 3 )
    procs = []
    procs.append( multiprocessing.Process( target = pixBnw, args = (img[0:procSize],0,return_dict) ) )
    procs.append( multiprocessing.Process( target = pixBnw, args = (img[procSize+1:2*procSize],1,return_dict) ) )
    procs.append( multiprocessing.Process( target = pixBnw, args = (img[2*procSize+1:],2,return_dict) ) )
   
    [p.start() for p in procs]
    [p.join() for p in procs]
    img = return_dict[0] + return_dict[1] + return_dict[2]
 
    print( time.time() - start )
    return img'''
 
def bnw( img ):
    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            #ave = max( [img[i][j][0], img[i][j][1], img[i][j][2] ] )
            ave = img[i][j][0] * 0.299 + img[i][j][1] * 0.587 + img[i][j][2] * 0.114
            img[i][j][0], img[i][j][1], img[i][j][2] = ave, ave, ave
    return img
 
def pixellate( img ):
    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            if j%2==1 and j+1 < len(img[i]) and i+1 < len(img):
                img[i][j] = img[i+1][j+1]
    return img
 
def mirror( img ):
    for i in range( math.floor(len( img )/2) ):
        for j in range( len( img[i] ) ):
            img[i][j], img[len(img)-i-1][j] = img[len(img)-i-1][j], img[i][j]
    return img
 
def upsideDown( img ):
    dup = copy.deepcopy(img)
    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            dup[i][j], dup[len(img)-i-1][j] = img[len(img)-i-1][j], img[i][j]
    return dup
    #return np.flipud(img) #boring
 
def sePixel( px ): #taking a list [R, G, B]
    a = [0,0,0]
    a[0] = (px[0] * 0.393) + (px[1] * 0.769) + (px[2] * 0.189)
    a[1] = (px[0] * 0.349) + (px[1] * 0.686) + (px[2] * 0.168)
    a[2] = (px[0] * 0.272) + (px[1] * 0.534) + (px[2] * 0.131)
    for i in range(3): #the dumb a stuff rather than px because it auto loops weird
        if a[i] > 255:
            a[i] = 255
    return a

def setPixelAlpha( px ):
    a = [0,0,0,px[3]]
    a[0] = (px[0] * 0.393) + (px[1] * 0.769) + (px[2] * 0.189)
    a[1] = (px[0] * 0.349) + (px[1] * 0.686) + (px[2] * 0.168)
    a[2] = (px[0] * 0.272) + (px[1] * 0.534) + (px[2] * 0.131)
    for i in range(3): #the dumb a stuff rather than px because it auto loops weird
        if a[i] > 255:
            a[i] = 255
    return a
 
def sepia( img ):
    channelT = len(img[0][0])

    img = bnw(img)
    for i in range( len( img ) ):
        for j in range( len( img[i] ) ):
            if channelT == 4:
                img[i][j] = setPixelAlpha( img[i][j] )
            if channelT == 3:
                img[i][j] = sePixel( img[i][j] )
    return img
 
def particle( img ):
    imgmod = np.vectorize( lambda a : a if a%11 == 0 else 50  )
    return imgmod( img )