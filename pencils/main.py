import cv2

def count_pencils(imgPath):

    pencilCount = 0

    image = cv2.imread(imgPath, cv2.IMREAD_GRAYSCALE)
    
    _, thresh = cv2.threshold(image, 120, 255, cv2.THRESH_BINARY)
    thresh = cv2.erode(thresh, None, iterations = 40)
    thresh = cv2.bitwise_not(thresh)
    
    output = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
    (amountLabels, labels, stats, centroids) = output

    for i in range(1, amountLabels):

        area = stats[i, cv2.CC_STAT_AREA]

        if (area > 500000 and area < 700000):
            pencilCount += 1

    return pencilCount


if __name__ == "__main__":

    totalPencilCount = 0

    imgAmount = 12

    for i in range(1, imgAmount+1):

        pencilCount = count_pencils(f"img ({i}).jpg")
        totalPencilCount += pencilCount
        print(f"На изображении {i} найдено {pencilCount} карандашей.")
    
    print(f"Суммарное количество карандашей на всех изображениях: {totalPencilCount}")    
    
