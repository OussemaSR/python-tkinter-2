from tkinter import *
from PIL import Image, ImageTk , ImageFilter
import cv2
import urllib.request
import numpy as np
import time
import tkinter
from tkinter import filedialog
import pylab as plb
import imageio
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from math import *
import os
from scipy import fftpack
import ntpath
from tkinter import Tk, Canvas, Frame, BOTH
from skimage.util import random_noise


### file name extractor
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)
######################
fln=''

root = Tk()
root.title("Traitement d'Image")
root.geometry("1200x680")
## drawing lines ######
class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Traitement d'Image")
        self.pack(fill=BOTH, expand=1)

        canvas = Canvas(self)
        canvas.create_line(340,10, 340, 600, dash=(4, 2))
        canvas.create_line(1000,10, 1000, 600, dash=(4, 2))
        canvas.pack(fill=BOTH, expand=1)
        
ex =  Example()
#######################
#viewing images function
def view_img(imgv):
    plt.figure()
    mg_ = ImageTk.getimage(imgv)
    imgplot = plt.imshow(mg_)
    plt.show()
# median filter  
def filtre_Med(imM):
   median = cv2.medianBlur(imM, 5)
   cv2.imshow('img', median)
   return median
# gauss filter
def filtre_Gauss(imG):
    gauss=cv2.GaussianBlur(imG,(5,5),0)
    cv2.imshow('img', gauss)
    return gauss

##############################################################################
def filtre_M():
   median=filtre_Med(noise_img)
   img_fln=os.path.splitext(fln)[0]
   sm_file=f'C:/images/{img_fln}_filtrer_mediane.png'
   print(sm_file)
   cv2.imwrite(sm_file, median) # saving path for salt and pepper image
   sm_img = Image.open(sm_file)
   sm_imgR=sm_img.resize((250, 200), Image.ANTIALIAS)
   global my_imgm
   my_imgm = ImageTk.PhotoImage(sm_imgR)
   label_img_sp = Label(root, image = my_imgm)
   label_img_sp.image = my_imgm
   label_img_sp.place(x = 700 , y = 20)
   label_imgs_title = Label(root, text='Image filtré avec mediane ', font=("Arial Black ",10),fg='GREEN' )
   label_imgs_title.place(x = 700 , y= 10)
   view_btn=Button(root,text='Aperçu',font=("Arial Black ",10) ,bg='CYAN',command=lambda : view_img(my_imgm))
   view_btn.place(x=770,y=230)
   
def filtre_G():
    gauss=filtre_Gauss(imgbrG)
    img_fln=os.path.splitext(fln)[0]
    smfg_file=f'C:/images/{img_fln}_Fgauss.png'
    cv2.imwrite(smfg_file, gauss)
    global imgfg
    imgfg = cv2.imread(smfg_file)
    smfg_img = Image.open(smfg_file)
    smfg_imgR=smfg_img.resize((250, 200), Image.ANTIALIAS)
    global my_smfg
    my_smfg = ImageTk.PhotoImage(smfg_imgR)
    label_smfg = Label(root, image = my_smfg)
    label_smfg.image = my_smfg
    label_smfg.place(x = 700 , y = 270)
    label_smfg_title = Label(root, text='Image filtré avec Gaussian ', font=("Arial Black ",10),fg='GREEN' )
    label_smfg_title.place(x = 700 , y= 260)
    view_btn=Button(root,text='Aperçu',font=("Arial Black ",10) ,bg='CYAN',command=lambda : view_img(my_smfg))
    view_btn.place(x=770,y=480)
###################################################################################
    
##import image function 
def aquization():
    global imgfile
    imgfile = filedialog.askopenfilename(initialdir="C:/images/", title="Select A File", filetypes=(("all files", "*.*"),("png files","*.png")))
    img = Image.open(imgfile)
    imgR=img.resize((300, 250), Image.ANTIALIAS)
    global fln
    fln = path_leaf(imgfile)
    global newpic
    newpic = ImageTk.PhotoImage(imgR)
    imgg = newpic
    #newpic._PhotoImage__photo.write("test.png")
    label_img1 =  Label(root, image = newpic )
    label_img1.pack()
    label_img1.place(x = 20 , y = 180)
    label_title = Label(root, text="Image Original", font=("Arial ",20),fg='BLUE' )
    label_title.place(x = 90 , y= 115)
    label_img_title = Label(root, text=f'Image: {fln}', font=("Arial Black ",12) )
    label_img_title.place(x = 20 , y= 155)
    view_btn=Button(root,text='Aperçu',font=("Arial Black ",10) ,bg='CYAN',command=lambda : view_img(newpic))
    view_btn.place(x=140,y=440)
# initialisation de image counter

count = 1
##  capture image
def PCcam():

    global count
    count = count
    while True:
        cap = cv2.VideoCapture(0)
        ret,img=cap.read()
        cv2.imshow('My webcam             P:Capture         Q:quit',img)
        q=cv2.waitKey(1)
        if q == ord("q"):
            break;
        elif q == ord("p"):
            PCphoto="C:/images/Capture_0"+str(count)+".png"  #choose the file save path
            rval, frame = cap.read()
            cv2.imwrite(PCphoto, frame)
            img = Image.open(PCphoto) #marwen add this
            imgR=img.resize((300, 250), Image.ANTIALIAS)
            global newpic
            newpic = ImageTk.PhotoImage(imgR)
            label_img3 = Label(root, image = newpic )
            label_img3.image = newpic # keep a reference!
            #extacting base-name of image
            fln = path_leaf(PCphoto)
            label_img3.place(x = 20 , y = 180)
            label_title = Label(root, text="Image Original", font=("Arial ",20),fg='BLUE' )
            label_title.place(x = 90 , y= 115)
            label_img_title = Label(root, text=f'Image: {fln}', font=("Arial Black ",10) )
            label_img_title.place(x = 20 , y= 155)
            count+=1
            break;
    cv2.destroyAllWindows()

    global imgfile
    imgfile=PCphoto
    view_btn=Button(root,text='Aperçu',font=("Arial Black ",10) ,bg='CYAN',command=lambda : view_img(newpic))
    view_btn.place(x=140,y=440)

    
#################################### noises #####################################################
###################################### salt & pepper noise
def s__p ():
    imgsp = cv2.imread(imgfile)
    global noise_img
    noise_img = random_noise(imgsp, mode='s&p',amount=0.3)
    noise_img = np.array(255*noise_img, dtype = 'uint8')
    img_fln=os.path.splitext(fln)[0]
    global s_p_file
    s_p_file=f'C:/images/{img_fln}_salt&papper.png'
    print(s_p_file)
    cv2.imwrite(s_p_file, noise_img) # saving path for salt and pepper image
    # Display the noise image
    cv2.imshow('blur',noise_img)
    s_p_img = Image.open(s_p_file)
    s_p_imgR=s_p_img.resize((250, 200), Image.ANTIALIAS)
    global my_imgs
    my_imgs = ImageTk.PhotoImage(s_p_imgR)
    label_img_sp = Label(root, image = my_imgs)
    label_img_sp.image = my_imgs
    label_img_sp.place(x = 400 , y = 20)
    label_imgs_title = Label(root, text='Image Brouillé Salt and Pepper ', font=("Arial Black ",10),fg='GREEN' )
    label_imgs_title.place(x = 400 , y= 10)
    view_btn=Button(root,text='Aperçu',font=("Arial Black ",10) ,bg='CYAN',command=lambda : view_img(my_imgs))
    view_btn.place(x=430,y=230)
    view_btn=Button(root,text='Filtrer avec Mediane',font=("Arial Black ",10) ,bg='YELLOW',command=filtre_M)
    view_btn.place(x=500,y=230)
###################################### Gaussian noise
def BrGuass ():
    image = cv2.imread(imgfile)
    row,col,ch= image.shape
    mean = 0
    var = 0.1
    sigma = var**0.5
    gauss = np.random.normal(mean,sigma,(row,col,ch))
    gauss = gauss.reshape(row,col,ch)
    noisy = image + image*gauss
    img_fln=os.path.splitext(fln)[0]
    Brm_file=f'C:/images/{img_fln}_BGauss.png'
    cv2.imwrite(Brm_file, noisy)
    global imgbrG
    imgbrG = cv2.imread(Brm_file)
    cv2.imshow('img', imgbrG)

    Brm_img = Image.open(Brm_file)
    Brm_imgR=Brm_img.resize((250, 200), Image.ANTIALIAS)
    global Brm_imgs
    Brm_imgs = ImageTk.PhotoImage(Brm_imgR)
    label_img_Brm = Label(root, image = Brm_imgs)
    label_img_Brm.image = Brm_imgs
    label_img_Brm.place(x = 400 , y = 270)
    label_imgBrm_title = Label(root, text='Image Brouillé Gaussian ', font=("Arial Black ",10),fg='GREEN' )
    label_imgBrm_title.place(x = 400 , y= 260)
    view_btn=Button(root,text='Aperçu',font=("Arial Black ",10) ,bg='CYAN',command=lambda : view_img(Brm_imgs))
    view_btn.place(x=430,y=480)
    view_btn=Button(root,text='Filtrer avec Gaussian ',font=("Arial Black ",10) ,bg='YELLOW',command=filtre_G)
    view_btn.place(x=500,y=480)

###################################################################

def filtre_Mediane():
    img = cv2.imread(imgfile)
    median = filtre_Med(img)
    img_fln=os.path.splitext(fln)[0]
    sm_file=f'C:/images/{img_fln}_FMed.png'
    print(sm_file)
    cv2.imwrite(sm_file, median) # saving path for salt and pepper image
    sm_img = Image.open(sm_file)
    sm_imgR=sm_img.resize((250, 200), Image.ANTIALIAS)
   
    global my_imgG
    my_imgG = ImageTk.PhotoImage(sm_imgR)
    label_img_sp = Label(root, image = my_imgG)
    label_img_sp.image = my_imgG
    label_img_sp.place(x = 1050 , y = 270)
    label_imgs_title = Label(root, text='Image filtré avec mediane ', font=("Arial Black ",10),fg='GREEN' )
    label_imgs_title.place(x = 1050 , y= 260)
    view_btn=Button(root,text='Aperçu',font=("Arial Black ",10) ,bg='CYAN',command=lambda : view_img(my_imgG))
    view_btn.place(x=1120,y=480)
    
def filter_gaussian():
    img = cv2.imread(imgfile)
    gauss=filtre_Gauss(img)
    img_fln=os.path.splitext(fln)[0]
    sm_file=f'C:/images/{img_fln}_FGauss.png'
    print(sm_file)
    cv2.imwrite(sm_file, gauss) # saving path for salt and pepper image
    sm_img = Image.open(sm_file)
    sm_imgR=sm_img.resize((250, 200), Image.ANTIALIAS)

    global my_imgFG
    my_imgFG = ImageTk.PhotoImage(sm_imgR)
    label_img_sp = Label(root, image = my_imgFG)
    label_img_sp.image = my_imgFG
    label_img_sp.place(x = 1050 , y = 20)
    label_imgs_title = Label(root, text='Image filtré avec Gaussian ', font=("Arial Black ",10),fg='GREEN' )
    label_imgs_title.place(x = 1050 , y= 10)
    view_btn=Button(root,text='Aperçu',font=("Arial Black ",10) ,bg='CYAN',command=lambda : view_img(my_imgG))
    view_btn.place(x=1120,y=230)
    
def compression():
    global Labelmemo
    Labelmemo= Label(root, text="Taille d'image intiale\n"+str((os.path.getsize(imgfile)/1024))+" koctets", font=("Arial Black",14),fg='RED' )
    Labelmemo.place(x=400,y=540)
    im = Image.open(imgfile).convert('RGB')
    im.save('C:/images/photoJPEG.jpg', format='JPEG', quality=50)
    global LabelmemJ
    LabelmemJ= Label(root, text="Taille d'image EN JPEG:\n"+str((os.path.getsize('C:/images/photoJPEG.jpg')/1024))+" Koctets", font=("Arial Black",14),fg='GREEN')
    LabelmemJ.place(x=700,y=540)
    
    imgfilee = "C:/images/photoJPEG.jpg"
    img = Image.open(imgfilee)
    imgR=img.resize((200, 200), Image.ANTIALIAS)
    plt.imshow(imgR, cmap = 'gray')
    plt.title('Photo_Compressé_JPEG')
    plt.show()

def TFF():
    img = cv2.imread(imgfile,0)
    im_fft = fftpack.fft2(img)
    # Show the results

    def plot_spectrum(im_fft):
        from matplotlib.colors import LogNorm
    # A logarithmic colormap
        plt.imshow(np.abs(im_fft), norm=LogNorm(vmin=5))
        plt.colorbar()

    plt.figure()
    f = np.fft.fft2(img)
    fshift = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(fshift))
    plt.subplot(221),plt.imshow(img, cmap = 'gray')
    plt.title('Input Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(222),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.subplot(223),plot_spectrum(im_fft)
    plt.title('Fourier transform')
    plt.show()

label_tools=Label(root,text="Tools",font=('Arial Black',12))
label_tools.place(x=140,y=480)

label_tools=Label(root,text="Bruit",font=('Arial',10))
label_tools.place(x=50,y=520)

label_tools=Label(root,text="Fonctions",font=('Arial',10))
label_tools.place(x=230,y=520)

DD = Button(root, text=('Importer une Image'), font=('Arial', 10), bg='ORANGE', command=aquization)
DD.place(x=20,y=20)

PC = Button(root, text=('Prendre une image'), font=('Arial', 10), bg='ORANGE',command=PCcam)
PC.place(x=20,y=50)

################### main filter buttons
Filtregaussien = Button(root, text=('Filtre Gauss'), font=('Arial',10), bg='ORANGE',command=filter_gaussian)
Filtregaussien.place(x=200,y=550)

Filtremed = Button(root, text=('Filtre Mediane'), font=('Arial', 10), bg='ORANGE',command=filtre_Mediane)
Filtremed.place(x=200,y=580)
################### compression button
Filtrebrouiller = Button(root, text=('Compression'), font=('Arial', 10), bg='ORANGE',command=compression)
Filtrebrouiller.place(x=200,y=610)

################### tff buttons
Filtrebrouiller = Button(root, text=('TFF'), font=('Arial', 10), bg='ORANGE',command=TFF)
Filtrebrouiller.place(x=200,y=640)

################### noise buttons
s_p_btn = Button(root, text=('Sault&Pepper '), font=('Arial',10), bg='ORANGE',command=s__p)
s_p_btn.place(x=20,y=550)

s_p_btn = Button(root, text=('Bruit Gaussian '), font=('Arial',10), bg='ORANGE',command=BrGuass)
s_p_btn.place(x=20,y=580)


root.mainloop()
