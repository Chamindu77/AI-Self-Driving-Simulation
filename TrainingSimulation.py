print('Setting UP')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from utlis import *
from sklearn.model_selection import train_test_split




#### STEP 1
path = 'myData'
data = importDataInfo(path)

#### STEP 2
data = balanceData(data, display=False)

#### STEP 3
imagesPath, steering = loadData(path,data)
print(imagesPath[0],steering[0])

#### STEP 4
xTrain, xVal, yTrain, yVal = train_test_split(imagesPath, steering, test_size=0.2,random_state=10)
print('Total Training Images: ',len(xTrain))
print('Total Validation Images: ',len(xVal))

#### STEP 5

#### STEP 6

#### STEP 7

#### STEP 7
model = createModel()
model.summary()

#### STEP 7
history = model.fit(batchGen(xTrain, yTrain, 100, 1),steps_per_epoch=300,epochs=10,
                    validation_data=batchGen(xVal, yVal, 100, 0),validation_steps=200)

#### STEP 10
model.save('model.h5')
print('Model Saved')

plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.legend(['Training','Validation'])
plt.title('Loss')
plt.xlabel('Epoch')
plt. show()
