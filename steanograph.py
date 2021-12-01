import numpy as np
from PIL import Image
from numpy.lib.shape_base import dstack
import piexif
import cv2
import itertools
import os

###DCT image encoding/decoding###

quant_array = [[16,11,10,16,24,40,51,61],      # QUANTIZATION TABLE
                    [12,12,14,19,26,58,60,55],    # required for DCT
                    [14,13,16,24,40,57,69,56],
                    [14,17,22,29,51,87,80,62],
                    [18,22,37,56,68,109,103,77],
                    [24,35,55,64,81,104,113,92],
                    [49,64,78,87,103,121,120,101],
                    [72,92,95,98,112,100,103,99]]
quant = np.array(quant_array)

def divide_2_chunks(l, n):
    m = int(n)
    for i in range(0, len(l), m):
        yield l[i:i + m]

def padding(img, row, col):
    img = cv2.resize(img,(col+(8-col%8),row+(8-row%8)))    
    return img

def convert2bits(msg):
    bits = []
    for char in msg:
        binval = bin(ord(char))[2:].rjust(8,'0')
        bits.append(binval)
    return bits

def DCT_encode(src,secret_msg):
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    secret=secret_msg
    msg = str(len(secret))+'*'+secret
    msg_bits = convert2bits(msg)
    #image size
    row,col = img.shape[:2]
    if((col/8)*(row/8)<len(secret)):
        print("Error: size of image too small")
        return False

    #used to make it divisible by 8x8
    if  col%8 != 0 or row%8 != 0:
        img = padding(img, row, col)
    
    row,col = img.shape[:2]
    #generating RGB channel from the image
    b_img,g_img,r_img = cv2.split(img)
    #Because the message needed to be hidden in the blue channel, it was transformed to float32 for the dct function.
    b_img = np.float32(b_img)
    #breaking into 8x8 blocks
    block_img=[]
    for (j,i) in itertools.product(range(0,row,8),range(0,col,8)):
        block_img.append(np.round(b_img[j:j+8, i:i+8]-128) )
    #using dct cv2 function on the blocks
    dct_block_img=[]
    for img_Block in block_img:
        dct_block_img.append(np.round(cv2.dct(img_Block)))
    #then used quantization table on the blocks
    quantized_dct_block_img=[]
    for dct_Block in dct_block_img:
        quantized_dct_block_img.append(np.round(dct_Block/quant))
    ind1 = 0
    ind2 = 0
    for quantizedBlock in quantized_dct_block_img:
        #finding LSB in the DC coeff and replacing it with current msg bit
        DC = quantizedBlock[0][0]
        DC = np.uint8(DC)
        DC = np.unpackbits(DC)
        DC[7] = msg_bits[ind1][ind2]
        DC = np.packbits(DC)
        DC = np.float32(DC)
        DC= DC-255
        quantizedBlock[0][0] = DC
        ind2 = ind2+1
        if ind2 == 8:
            ind2 = 0
            ind1 = ind1 + 1
            if ind1 == len(msg):
                break
    #now using quantisation table blocks are run in reverse
    out_block_img=[]
    for quantizedBlock in quantized_dct_block_img:
        out_block_img.append(quantizedBlock *quant+128)
    #new image is generated
    out_image=[]
    for row_block in divide_2_chunks(out_block_img, col/8):
        for row_block_i in range(8):
            for block in row_block:
                out_image.extend(block[row_block_i])
    out_image = np.array(out_image).reshape(row, col)
    #converting from type float32
    out_image = np.uint8(out_image)
    out_image = cv2.merge((out_image,g_img,r_img))
    dst = "./dct_encrypted_" + src
    cv2.imwrite(dst,out_image)
    return out_image

def DCT_decode(src):
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    row,col = img.shape[:2]
    msg_size = None
    msg_bits = []
    buff = 0
    #RGB values are generated from the image
    b_img,g_img,r_img = cv2.split(img)
    #Because the message needed to be hidden in the blue channel, it was transformed to float32 for the dct function.
    b_img = np.float32(b_img)
    #breaking into 8x8 blocks
    block_img=[]
    for (j,i) in itertools.product(range(0,row,8),range(0,col,8)):
        block_img.append(b_img[j:j+8, i:i+8]-128)    
    #then used quantization table on the blocks
    quantized_dct_block_img=[]
    for img_Block in block_img:
        quantized_dct_block_img.append(img_Block/quant)
    i=0
    #extracting msgbits from LSB of DC
    for quantizedBlock in quantized_dct_block_img:
        DC = quantizedBlock[0][0]
        DC = np.uint8(DC)
        DC = np.unpackbits(DC)
        if DC[7] == 1:
            buff+=(0 & 1) << (7-i)
        elif DC[7] == 0:
            buff+=(1&1) << (7-i)
        i=1+i
        if i == 8:
            msg_bits.append(chr(buff))
            buff = 0
            i =0
            if msg_bits[-1] == '*' and msg_size is None:
                try:
                    msg_size = int(''.join(msg_bits[:-1]))
                except:
                    pass
        if len(msg_bits) - len(str(msg_size)) - 1 == msg_size:
            return ''.join(msg_bits)[len(str(msg_size))+1:]
    out_block_img=[]
    for quantizedBlock in quantized_dct_block_img:
        out_block_img.append(quantizedBlock *quant+128)
    #generates the new image
    out_image=[]
    for row_block in divide_2_chunks(out_block_img, col/8):
        for row_block_i in range(8):
            for block in row_block:
                out_image.extend(block[row_block_i])
    out_image = np.array(out_image).reshape(row, col)
    out_image = np.uint8(out_image)
    out_image = cv2.merge((out_image,g_img,r_img))
    return ''


###2 Image hide/extract###

def merge_rgb(rgb1,rgb2):
    """
    it merges the two rgb of the images,takes 4 MSB of rgb 1 and store in 4 MSB of new rgb 
    and take 4 MSB of rgb 2 and store in 4 LSB of new rgb
    """
    r1, g1, b1 = rgb1
    r2, g2, b2 = rgb2
    rgb = (r1[:4] + r2[:4],g1[:4] + g2[:4],b1[:4] + b2[:4])
    return rgb    

def int2bin(rgb):
    #converts integer to binary
    r, g, b = rgb
    t=(f'{r:08b}',f'{g:08b}',f'{b:08b}')
    return t

def bin2int(rgb):
    #converts binary to integer
    r, g, b = rgb
    t=(int(r, 2),int(g, 2),int(b, 2))
    return t

def image_hide(src1, src2):
    img1=Image.open(src1)
    img2=Image.open(src2)
    # Image 2 dimension > Image 1 dimensions
    if img2.size[1] > img1.size[1] or img2.size[0] > img1.size[0]:
        raise ValueError('size of image 1 is smaller thane image2')
    # Generate pixel map of both images
    pixels_1 = img1.load()
    pixels_2 = img2.load()
    # Output image generated
    new_image = Image.new(img1.mode, img1.size)
    pixels_new = new_image.load()
    for i in range(img1.size[0]):
        for j in range(img1.size[1]):
            rgb1 = int2bin(pixels_1[i, j])
            # black pixel will be used if pixel not valid
            rgb2 = int2bin((0, 0, 0))
            if i < img2.size[0] and j < img2.size[1]:
                rgb2 = int2bin(pixels_2[i, j])
            # merging rgb of both images
            rgb = merge_rgb(rgb1, rgb2)
            pixels_new[i, j] = bin2int(rgb)
    new_image.save('image_hide'+src1[-4:])
    x = 'image_hide' + src1[-4:]
    return x

def image_hide_extract(src):
    img=Image.open(src)
    # loads the pixel map of the image
    pixels = img.load()
    # Output image in created
    new_image = Image.new(img.mode, img.size)
    pixels_new = new_image.load()
    original_size = img.size
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            # Get the pixel rgb in binary
            r, g, b =int2bin(pixels[i, j])
            # Take 4LSB and add it to 4MSB of new image
            # we add 0000 at the 4LSB as decoder dosent know the value
            rgb = (r[4:] + '0000',g[4:] + '0000',b[4:] + '0000')
            pixels_new[i, j] = bin2int(rgb)
            if pixels_new[i, j] != (0, 0, 0):
                original_size = (i + 1, j + 1)
    new_image = new_image.crop((0, 0, original_size[0], original_size[1]))
    new_image.save('decrypted'+src)
    return new_image


###metadata encoding/decoding###

def metadata_encode(src,msg):
    im = Image.open(src)
    if "exif" in im.info:
        exif_dict = piexif.load(im.info["exif"])
        exif_dict["0th"][piexif.ImageIFD.ImageDescription] = msg
        exif_bytes = piexif.dump(exif_dict)
    else:
        exif_bytes = piexif.dump({"0th":{piexif.ImageIFD.ImageDescription:msg}})
    dest="encoded_"+os.path.basename(src)
    im.save(dest, exif=exif_bytes)
    return dest

def metadata_decode(src):
    im = Image.open(src)
    a=piexif.load(im.info["exif"])["0th"]\
        [piexif.ImageIFD.ImageDescription].decode("utf-8")
    return a


###LSB encoding/decoding###

def LSB_encoding(src,msg):
    img = Image.open(src, 'r')
    width, height = img.size
    img_pixel = np.array(list(img.getdata()))

    """
    We check if the mode of the image is RGB or RGBA and consequently set the value of n
    We also calculate the total number of pixels.
    """
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    i_size = img_pixel.size//n
    
    """
    we add a delimiter (“#END#") at the end of the secret message, so that when the program decodes, 
    it knows when to stop. We convert this updated message to binary form and calculate the required pixels.
    """
    msg+="#END#"
    b_msg="".join([format(ord(i),'08b') for i in msg])
    n_pix=len(b_msg)

    """
    we make a check if the total pixels available is sufficient for the secret message or not. 
    If yes, we proceed to iterating the pixels one by one and modifying their 
    least significant bits to the bits of the secret message until the complete message 
    including the delimiter has been hidden.
    """
    if n_pix > i_size:
        print("ERROR(File size is small for this msg to insert)")
    else:
        i=0
        for p in range(i_size):
            for q in range(0,3):
                if i < n_pix:
                    img_pixel[p][q]=int(bin(img_pixel[p][q])[2:9] + b_msg[i],2)
                    i+=1
        img_pixel=img_pixel.reshape(height,width,n)
        enc=Image.fromarray(img_pixel.astype('uint8'),img.mode)
        dest="lsb_encoded_"+os.path.basename(src)
        enc.save(dest)
    return dest

def LSB_Decode(src):
    img = Image.open(os.path.basename(src), 'r')
    img_pixel = np.array(list(img.getdata()))
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    i_size = img_pixel.size//n
    secret = ""
    for p in range(i_size):
        for q in range(0, 3):
            secret += (bin(img_pixel[p][q])[2:][-1])

    secret = [secret[i:i+8] for i in range(0, len(secret), 8)]

    msg = ""
    for i in range(len(secret)):
        if msg[-5:] == "#END#":
            break
        else:
            msg += chr(int(secret[i], 2))
    if "#END#" in msg:
        return "Secret: "+msg[:-5]
    else:
        return "ERROR(No Secret Found)"

'''DCT_encode('babylon.png',"hello_world") # arg 1 = image source , arg 2 = secret message , (saves the encrypted image)
msg=DCT_decode('dct_encrypted_babylon.png') # arg = image source , return= secret message
print(msg)

image_hide('lenna.png','pepper.png') # arg 1 = image source , arg 2 = image , (saves the encrypted image)
image_hide_extract('image_hide.png') # arg = image source , (saves the decrypted image)

metadata_encode('img1.jpg','yo_world') # arg 1 = image source , arg 2 = secret message , (saves the encrypted image)
msg=metadata_decode('encoded_img1.jpg') # arg = image source ,  return = secret message
print(msg)

LSB_encoding('lenna.png','very_secret_message') # arg 1 = image source , arg 2 = secret message
msg=LSB_Decode('lsb_encoded_lenna.png') # arg = image source , return = secret message
print(msg)'''