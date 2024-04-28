import cv2
import matplotlib.pyplot as plt

img = cv2.imread("balls_and_rects.png")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

colorsCircleDict = {}
colorsRectangleDict = {}

(labelsAmount, labels, stats, centroids) = cv2.connectedComponentsWithStats(gray, 4, cv2.CV_32S)

for i in range(1, labelsAmount):
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]
    area = stats[i, cv2.CC_STAT_AREA]

    subimg = imgHsv[y:y+h, x:x+w]          
    key = subimg[h//2, w//2, 0]
    
    if(area == w*h):
        if not(key in colorsRectangleDict.keys()):
            colorsRectangleDict[key] = 1
        else:
            colorsRectangleDict[key] += 1     
        
    else:
        if not(key in colorsCircleDict.keys()):
            colorsCircleDict[key] = 1
        else:
            colorsCircleDict[key] += 1

print(f"круги: {colorsCircleDict}")
print(f"прямоугольники: {colorsRectangleDict}")   

plt.imshow(imgHsv)
plt.show()

