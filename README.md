# Pneumonia Detector

This project aims to detect pneumonia from chest X-ray images using a deep learning model. The model, which utilizes a Convolutional Neural Network (CNN) framework implemented in Keras and TensorFlow, has achieved an accuracy of around 98%. The application is built with a Users can upload X-ray images and receive predictions on whether or not the image shows signs of pneumonia.

## Technologies Used
Utilized Keras for training the CNN model, Flask serves as the backend framework for handling image uploads and processing, while Vue.js is used for developing a responsive and interactive frontend interface.

## Installation Instructions

1. Install the Python dependencies:
   ```bash
   cd ./Model/backend
   pip install -r requirements.txt
2. Install the Vue.js Dependences:
   ```bash
   cd ./Model/frontend
   npm install
## Running Instructions

1. Start the flask server:
   ```bash
   cd ./Model/backend
   flask run
2. Start the Vue.js development server:
   ```bash
   cd ./Model/frontend
   npm run dev
