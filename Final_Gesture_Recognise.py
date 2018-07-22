import cv2
import numpy as np

def nothing(x):
	pass

def distance(x1,x2,y1,y2):
	return ((x1 - x2)**2 + (y1 - y2)**2)**(1/2.0)

cap=cv2.VideoCapture(0)
cv2.namedWindow("Trackbar")
cv2.createTrackbar("G","Trackbar",0,255,nothing)
trigger=0
j=0
ix=0
flag=0
iy=0
while (True):
	ret,img=cap.read()
	defects=[]
	tips=[]
	gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	gray=cv2.GaussianBlur(gray,(5,5),1)
	g=cv2.getTrackbarPos("G","Trackbar")
	ret,thresh=cv2.threshold(gray,g,255,cv2.THRESH_BINARY_INV)
	thresh=cv2.medianBlur(thresh,5)
	thresh2=thresh.copy()
	_,contours,heirarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	max_area=-1
	maxim=0
	for i in range(len(contours)):
		area=cv2.contourArea(contours[i])
		perimeter=cv2.arcLength(contours[i],True)
		if area>max_area and area>10000:
			maxim=i
		max_cont=contours[maxim]

	if len(contours)>0:
		vertices = cv2.approxPolyDP(max_cont,0.01*cv2.arcLength(max_cont,True),True)
		#for i in vertices:
		#	ix,iy=i[0]
		#	cv2.circle(img,(ix,iy),10,(0,255,0),2)
		
		hull=cv2.convexHull(max_cont)					

		cv2.drawContours(img,contours,maxim,(0,0,255),2)
		cv2.drawContours(img,[hull],0,(0,255,0),2)

		for i in range(len(hull)-1):
			if i==len(hull)-1:
				ix,iy=hull[i][0]
				ex2,iy2=hull[0][0]
			else:
				ix,iy=hull[i][0]
				ix2,iy2=hull[i+1][0]
			if distance(ix,ix2,iy,iy2)>10:
				tips.append([ix,iy])
				cv2.circle(img,(ix,iy),5,(255,0,255),-1)
				print len(tips)
			#else:
			#	cv2.circle(img,(ix,iy),5,(255,255,0),2)

		for i in vertices:
			x1,y1=i[0]
			flag=0
			for j in tips:
				x2,y2=j
				if distance(x1,x2,y1,y2)<20:
					flag=1
					break
			if flag==0:
				defects.append([x1,y1])
				cv2.circle(img,(x1,y1),5,(0,255,255),-1)
			#cv2.circle(img,(tuple)(i),5,(0,255,255),-1)

		print len(defects)
		
	cv2.imshow("Image",img)
	cv2.imshow("Thresh",thresh2)
	if cv2.waitKey(1) == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()

