import cv2
#imread is used to read image
img=cv2.imread("image.jpg",1)#0 and 1 for gray scale image and coloured image
#To know the type of the image

#-->  print(type(img))

#print(img.shape) #To know number of rows and columns are present in the image. 
#resized = cv2.resize(img,(600,1000))
resized = cv2.resize(img,(int(img.shape[1]/2),int(img.shape[0]/2))) #resizing symmetrically
#imshow prints the image
cv2.imshow("Ladakh",resized)
#waiting time
cv2.waitKey(0)
#when we enters any key automatically it destroys all the windows.
cv2.destroyAllWindows()


