import cv2
from pathlib import Path


image_list = Path(__file__).parent.glob('*.jpg')
#print(image_list)

for image_path in image_list:
    img = cv2.imread(str(image_path))
    factor = 0.25
    width = int(img.shape[1] * factor)
    height = int(img.shape[0] * factor)
    dim = (width, height)
    resized_img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    cv2.imshow(image_path.name, img)
    cv2.imshow('Resized', resized_img)
    cv2.imwrite('resized_' + str(image_path), resized_img)
cv2.waitKey(0)
cv2.destroyAllWindows()