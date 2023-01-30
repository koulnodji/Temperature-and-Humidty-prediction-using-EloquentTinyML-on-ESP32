# -*- coding: utf-8 -*-
"""Test_Success.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ccdItncqS0fPfw1igGCphqmTfMJbnOCv
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Create a dataframe with random values
df = pd.DataFrame(np.random.randint(0, 100, size=(50, 5)), columns=['temp', 'hum', 'soil', 'ldr', 'carbon'])

# Split the data into input and output
input_data = df[['temp', 'hum', 'carbon']]
output_data = df[['soil', 'ldr']]

# Apply standardization to the input and output data
scaler = StandardScaler()
input_data_scaled = scaler.fit_transform(input_data)
output_data_scaled = scaler.fit_transform(output_data)

# Split the data into training, validation, and testing data
input_train, input_test, output_train, output_test = train_test_split(input_data_scaled, output_data_scaled, test_size=0.05, random_state=0)
input_train, input_val, output_train, output_val = train_test_split(input_train, output_train, test_size=0.2, random_state=0)
print(input_train.shape)
print(output_train.shape)
print(input_test.shape)
print(output_test.shape)
print(input_val.shape)
print(output_val.shape)

# Create a model using the Dense layer
model = tf.keras.Sequential()

model.add(tf.keras.layers.Dense(units=32, input_shape=(3,), activation='relu'))
model.add(tf.keras.layers.Dense(units=64, activation='relu'))
model.add(tf.keras.layers.Dense(units=2, activation='relu'))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')
model.summary()

# Train the model
model.fit(input_train, output_train, epochs=100, validation_data=(input_val, output_val))

# Use the model to make predictions with the testing data
predictions = model.predict(input_test)

# Inverse the standardization to the predictions
predictions = scaler.inverse_transform(predictions)
predictions = pd.DataFrame(predictions, columns=['temp', 'hum'])
print(predictions)

# Create new dataset
new_data = np.random.rand(10, 3)
# Standardize the new dataset
mean = np.mean(new_data, axis=0)
std = np.std(new_data, axis=0)
new_data = (new_data - mean) / std

# Make predictions using the model
predictions = model.predict(new_data)
predictions = pd.DataFrame(predictions, columns=['temp', 'hum'])
print(predictions)

new_data

# Create new dataset
new_data = np.random.rand(15, 3)
# Make predictions using the model
predictions = model.predict(new_data)
predictions = pd.DataFrame(predictions, columns=['temp', 'hum'])
new_data = pd.DataFrame(new_data, columns=['temp', 'hum', 'soil'])
result_df = pd.concat([new_data, predictions], axis=1)
print(result_df)

model.save('model.h5')

# Reload the saved model
loaded_model = tf.keras.models.load_model('model.h5')

# Convert the model to TensorFlow Lite format
converter = tf.lite.TFLiteConverter.from_keras_model(loaded_model)
tflite_model = converter.convert()

# Save the converted model
open("converted_model.tflite", "wb").write(tflite_model)

!pip install  tinymlgen

c_code = port(model, pretty_print=True)
print(c_code)

converter = tf.lite.TFLiteConverter.from_keras_model(model) #create a converter
tflite_model = converter.convert() 

open("/content/tflite_model.tflite","wb").write(tflite_model) #Create a file containing our tflite model

!apt-get install -qq xxd #the tool is installed
!echo "const unsigned char model[] = {" > /content/tflite_model.h
!cat /content/tflite_model.tflite | xxd -i >> /content/model.h #create an hexadecimal array containing all our parameters
!echo "};" >> /content/model.h
from google.colab import files 
files.download("/content/model.h") # download our file automaticaly