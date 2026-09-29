import cv2
import os
import numpy as np 
import matplotlib.pyplot as plt 
import mediapipe as mp 
from mediapipe.tasks import python
from mediapipe.tasks.python import vision 
from sklearn.cluster import KMeans


def skin(img):
    # create a script for fixing the path 
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, img) #path for image
    model_path = os.path.join(script_dir, "face_landmarker.task") #path for model for getting the face landmarks

    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Could not load image at path: {image_path}")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Missing model file! Download face_landmarker.task to: {model_path}")

    # 2. Configure the FaceLandmarker detector
    base_options = python.BaseOptions(model_asset_path=model_path) # set up core mediapipe stuffs

#setting up basic face landmark stuffs
    options = vision.FaceLandmarkerOptions(
    base_options=base_options, # passing the model path
    output_face_blendshapes=True, # detect facial expressions
    output_facial_transformation_matrixes=True, # get face position
    num_faces=1, # number of faces to detect
    )

#making the detector and load it into memory
    detector = vision.FaceLandmarker.create_from_options(options)

# load image
    mp_image = mp.Image.create_from_file(image_path)

# run detection
    result = detector.detect(mp_image)

#check results
    if not result.face_landmarks:
        print("No face detected in the image")
    else:
        print("Face detected in the image!")
    #print(result.face_landmarks[0])

# getting the face landmarks
    face_landmarks = result.face_landmarks[0] 

    h,w,_=image.shape # getting the height and width of the image

    landmarks=[]

# Loop through all the landmarks and get the x and y coordinates
    for landmark in face_landmarks:
        x=int(landmark.x * w)
        y=int(landmark.y * h)
        landmarks.append([x,y])

# converting the landmarks to a numpy array to make it easier to work with
    landmarks = np.array(landmarks,dtype=np.int32) 

    print(landmarks[0]) # printing the first landmark
    '''
    plt.figure(figsize=(7,7)) # setting the size of the plot
    plt.imshow(image)  # showing the image
    # x coordinate (Horizontal axis) is for the width 
    # y coordinate (Vertical axis) is for the height 
    plt.scatter(landmarks[:,0],landmarks[:,1],s=2,c="red") # plotting the landmarks
    plt.axis("off") # turning off the axis
    plt.show()  # showing the plot  
    '''

# for finding the centre of the required regions
    left_cheek_center=(0.45 * landmarks[234] + 0.35 * landmarks[1] + 0.20 * landmarks[61]).astype(int)

    right_cheek_center=(0.45 * landmarks[454] + 0.35 * landmarks[1] + 0.20 * landmarks[291]).astype(int)

    forehead_center=(0.80 * landmarks[10] + 0.20 * landmarks[1]).astype(int)

    nose_center=(0.20 * landmarks[10] + 0.80 * landmarks[1]).astype(int)

# function to make the ellipse mask where indices is the index numbers of the part of the face 
    def ellipse_mask(image_shape, center, rx, ry):
        
        # make a np array with zeros which is basically a black image with the same height and width of the original image
        mask = np.zeros(image_shape[:2], dtype=np.uint8)
        # fill the ellipse with white pixel 255
        cv2.ellipse(mask, tuple(center), (rx, ry), 0, 0, 360, 255, -1)
        # return the mask
        return mask

# getting the width of the face from the left cheek to the right cheek
    face_width = np.linalg.norm(landmarks[454] - landmarks[234])
    face_height = np.linalg.norm(landmarks[10] - landmarks[1])
    print("Face width:  ",face_width)
    print("Face height: ",face_height)

# setting the radius of the ellipses
    cheek_rx = int(face_width * 0.20)
    cheek_ry = int(face_width * 0.12)

    nose_rx = int(face_width * 0.13)
    nose_ry = int(face_width * 0.12)

    forehead_rx = int(face_width * 0.35)
    forehead_ry = int(face_width * 0.11)

    left_cheek_mask = ellipse_mask(image.shape,left_cheek_center,cheek_rx,cheek_ry)

    right_cheek_mask = ellipse_mask(image.shape,right_cheek_center,cheek_rx,cheek_ry)

    nose_mask = ellipse_mask(image.shape,nose_center,nose_rx,nose_ry)

    forehead_mask = ellipse_mask(image.shape,forehead_center,forehead_rx,forehead_ry)

    region_mask = np.zeros(image.shape[:2], dtype=np.uint8)

# combining all the masks using bitwise or
    for mask in [left_cheek_mask,right_cheek_mask,nose_mask,forehead_mask]:

        region_mask = cv2.bitwise_or(region_mask,mask)

    region_visual= image.copy()
    region_visual[region_mask==255] = [255,255,255]
    '''
    plt.figure(figsize=(7,7))
    plt.imshow(region_visual)
    plt.axis("off")
    plt.show()
    '''
#finding skin using YCrCb colour space
#this colour space is used mainly to seperate the skin from hair,shadows,backgrounds etc.
    ycrcb= cv2.cvtColor(image, cv2.COLOR_RGB2YCrCb)

    y=ycrcb[:,:,0] #brightness 
    cr=ycrcb[:,:,1] #red component
    cb=ycrcb[:,:,2] #blue component

#skin mask with classic human color treshold values
    skin_mask= ((cr >= 133) & (cr <= 173) & (cb >= 77) & (cb <= 127))

# convert to uint8 to use in cv2
    skin_mask=skin_mask.astype(np.uint8)*255
    '''
    plt.figure(figsize=(7,7))
    plt.imshow(skin_mask,cmap="gray")
    plt.title("Raw skin mask")
    plt.axis("off")
    plt.show()
    '''
#combine region mask and skin mask using bitwise_and
    final_mask = cv2.bitwise_and(region_mask,skin_mask)

#used to remove noise and smooth the mask
    kernel = np.ones((3,3),np.uint8)

#remove small noise
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_OPEN, kernel)
#fill small holes
    final_mask = cv2.morphologyEx(final_mask, cv2.MORPH_CLOSE, kernel)

#isolate candidate pixels
    skin_visual=np.zeros_like(image)
    skin_visual[final_mask > 0] = image[final_mask>0] #keeping only the skin pixels

    '''
    plt.figure(figsize=(7,7))
    plt.imshow(skin_visual)
    plt.title("Candidate skin pixels with cleaned mask")
    plt.axis("off")
    plt.show()
    '''

#creating a skin pixel 
    skin_pixels_rgb=image[final_mask > 0]
    print("Skin Pixels : ",len(skin_pixels_rgb))

    '''
    if len(skin_pixels_rgb) < 500: 
        print("Doesn't have enough skin pixels for analysis")

    # Arrange extracted pixels into a visible grid
    num_pixels = len(skin_pixels_rgb)
    grid_width = 100
    grid_height = int(np.ceil(num_pixels / grid_width))

    # Add black pixels if needed to complete the grid
    padding = grid_width * grid_height - num_pixels

    if padding > 0:
        padding_pixels = np.zeros((padding, 3), dtype=np.uint8)
        display_pixels = np.vstack([skin_pixels_rgb, padding_pixels])
    else:
        display_pixels = skin_pixels_rgb

    display_pixels = display_pixels.reshape(grid_height, grid_width, 3)

    plt.figure(figsize=(10, 8))
    plt.imshow(display_pixels)
    plt.axis("off")
    plt.title("Extracted Skin Pixels")
    plt.show()
    '''

#convert rgb to lab 
    skin_pixels_lab= cv2.cvtColor(skin_pixels_rgb.reshape(-1,1,3).astype(np.uint8),cv2.COLOR_RGB2LAB)
    skin_pixels_lab=skin_pixels_lab.reshape(-1,3)

#removing the extreme bright region and shadow region
    L= skin_pixels_lab[:,0]
    valid= ((L > 30) & (L < 240))
    skin_pixels_lab=(skin_pixels_lab[valid])

#Do kmeans++ with skin pixel lab with 5 clusters  
    kmeans= KMeans(n_clusters=5, init="k-means++", n_init=10,random_state=42)
#taking a and b in LAB for clustering and L is avoided 
#L is taken into consideration at last cause we don't want brightness to dominate 
    labels= kmeans.fit_predict(skin_pixels_lab[:, 1:3])

#get the 5 cluster centres
    cluster_centers_ab= (kmeans.cluster_centers_)
    print("Cluster centre : \n ",cluster_centers_ab)

#calculate the no of pixels in each cluster 
    counts= np.bincount(labels, minlength=5)
    print("Cluster counts : ",counts)

#calculated the percentage of each clusters
    cluster_percentage= (counts/counts.sum())*100
    for i,per in enumerate(cluster_percentage):
        print(f"cluster {i} : {per} %")

#get the dominant cluster
    dominant_cluster=np.argmax(counts)
    print("The dominant cluster is : ",dominant_cluster)

#pixels in the dominant cluster 
    dominant_pixels_lab=(skin_pixels_lab[labels==dominant_cluster])
    print("Dominant cluster pixels : ", len(dominant_pixels_lab))

#use to get [L,a,b] value, median of the dominant pixels lab
#used median instead of mean to give robustness against outliers 
    representative_lab=np.median(dominant_pixels_lab,axis=0)
    print("representative value : ",representative_lab)

#convert to uint8 encoding standard encoding for images 
    representative_lab_unit8=np.uint8([[representative_lab]])
#convert lab to rgb
    representative_rgb=cv2.cvtColor(representative_lab_unit8,cv2.COLOR_LAB2RGB)[0][0]
#convert to integer
    representative_rgb=representative_rgb.astype(int)
    print("Representative RGB : ", representative_rgb)

    r,g,b = representative_rgb

#convert rgb to hex
    hex_color=("#{:02X}{:02X}{:02X}".format(r, g, b))
    print("Hex color : ",hex_color)

#display the estimated skin color
    '''
    plt.figure(figsize=(5,3))
    plt.imshow([[representative_rgb]])
    plt.title("Estimated skin color : "+ hex_color)
    plt.axis("off")
    plt.show() 
    '''

#get the confidence of the estimation by getting the % of dominant cluster pixels
    cluster_dominance= ((counts[dominant_cluster]/counts.sum()) * 100).astype(int)
    print("Cluster confidence : ",cluster_dominance,"%")

    return hex_color,representative_lab,representative_rgb

if __name__ == "__main__":
    c= skin("man2.jpg")
    
