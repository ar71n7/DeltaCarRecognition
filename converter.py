##----------------------------------------------
## converter semantic 2 2DBOX
##----------------------------------------------
import os, cv2, sys
import json
from time import sleep

cityPath = './gtFine_trainvaltest/gtFine/train/'	
cityArr = os.listdir(cityPath)

'''
count = 0
for city in cityArr:
	count += len(os.listdir('2DBoxAnnotation/'+str(city)))
print('Total images: %i'%count)
exit()
'''

for city in cityArr:
	print(city)
	picPath = './leftImg8bit_trainvaltest/leftImg8bit/train/'+str(city) + '/'
	picPathCV = '/home/danila/Documents/DeltaCourse/leftImg8bit_trainvaltest/leftImg8bit/train/'+str(city)+'/'
	annotationPath = './gtFine_trainvaltest/gtFine/train/'+str(city) + '/'
	try:
		os.mkdir('2DBoxAnnotation/' + str(city))
	except OSError:
		pass
	annotation2dBoxPath = '2DBoxAnnotation/'+str(city) + '/'

	picNames = os.listdir(picPath)
	annotationNames = os.listdir(annotationPath)

	for i in xrange(len(annotationNames)):
		if ".json" in annotationNames[i]:

			with open(annotationPath + annotationNames[i]) as data_file:
				data = json.load(data_file)
				
			img = cv2.imread(picPathCV + annotationNames[i][:-20]+"leftImg8bit.png")
			countBoxes = 0
			dictArr = []
			flagFindCar = 0
			for i_obj in data["objects"]:
				if "car" in i_obj["label"] or "truck" in i_obj["label"] or "bus" in i_obj["label"] or "caravan" in i_obj["label"] or "trailer" in i_obj["label"] or "train" in i_obj["label"]:
					flagFindCar = 1
					xMin = 1000000
					yMin = 1000000
					xMax = -1
					yMax = -1
					countBoxes += 1
					for i_point in i_obj["polygon"]:
						x = i_point[0]
						y = i_point[1]
						if (x < xMin):
							xMin = x
						if (y < yMin):
							yMin = y
						if (x > xMax):
							xMax = x
						if (y > yMax):
							yMax = y
					cv2.rectangle(img,(xMin, yMin), (xMax, yMax), (0, 255, 0), 2)
					h = abs(xMax - xMin)
					w = abs(yMax - yMin)
					dict = {"box2d_front":{0:{"h":h,"w":w,"x":xMin,"y":yMax}}, "id":countBoxes,"name":"Car_box2d","startTime":0,"stopTime":0}
					dictArr.append(dict)
			json2dBoxName = annotation2dBoxPath + annotationNames[i][:-20]+"leftImg8bit.json"
			with open(json2dBoxName, "w") as file:
				if (flagFindCar):
					json.dump({'LABELS':dictArr}, file, indent=4, sort_keys = True)
				else:
					json.dump({'LABELS':[]}, file, indent=4, sort_keys = True)
				
			##------ Uncomment for debug------
			## cv2.imshow("img", img)
			## key = cv2.waitKey()

	

		