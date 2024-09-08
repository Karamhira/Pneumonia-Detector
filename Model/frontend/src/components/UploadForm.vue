<template>
  <div class="page-container">
    <div class="container">
      <input type="file" id="file" accept="image/*" ref="fileInput" hidden @change="handleFileChange">
      <div class="img-area" :data-img="imageName" :class="{ active: hasImage }">
        <h3>Upload Image</h3>
        <p>Image size must be less than <span>5MB</span></p>
        <img v-if="imageUrl" :src="imageUrl" alt="Uploaded Image">
      </div>
      <button class="select-image" @click="selectImage">Upload Image</button>
      <button class="select-image Submit" @click="submit">Submit</button>
    </div>
    
    <div class="prediction-container">
      <div v-if="predictionResult !== null" class="result">
        <h3>Prediction Result:</h3>
        <div class="resultClass">

          <h3>{{ predictionResult }}</h3>
          <p v-if="predictionResult === 'NORMAL'">
            Your image does not show signs of Pneumonia.
          </p>

          <p v-if="predictionResult === 'NORMAL'">
            Note: This prediction is based on the image analysis and may not be 100% accurate. It's important to consult with a healthcare professional for a thorough evaluation.
          </p>

          <p v-else-if="predictionResult === 'PNEUMONIA'">
            The prediction indicates Pneumonia. Please consult a healthcare professional for further evaluation.
          </p>
        </div>

        <div class="warning-text" v-if="predictionResult === 'PNEUMONIA'">
          <p>Warning: Pneumonia is a serious condition that requires medical attention. Do not ignore the symptoms or delay consulting a doctor.</p>
        </div>
      </div>
      
      <div v-else class="no-image">
        <h3>Please Upload and Submit an Image.</h3>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UploadForm',
  data() {
    return {
      imageUrl: null,
      imageName: '',
      hasImage: false,
      imageBase64: null,
      predictionResult: null 
    };
  },
  methods: {
    selectImage() {
      this.$refs.fileInput.click();
    },
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file && file.size < 5000000) { 
        const reader = new FileReader();
        reader.onload = () => {
          this.imageUrl = reader.result;
          this.imageName = file.name;
          this.hasImage = true;
          this.imageBase64 = reader.result.split(',')[1]; 
        };
        reader.readAsDataURL(file);
      } else {
        alert("Image size more than 5MB");
      }
    },
    async submit() {
      if (!this.imageBase64) {
        alert('Please upload an image first.');
        return;
      }

      try {
        const response = await axios.post('http://127.0.0.1:5000/predict', {
          image: this.imageBase64
        });
        this.predictionResult = response.data.prediction;
      } catch (error) {
        console.error(error);
        alert('Error submitting the image.');
      }
    }
  }
}
</script>


<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: "times new roman";
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f0f0;
}

.page-container {
  display: flex;
  max-width: 1200px;
  width: 100%;
  align-content: center;
  justify-content: center;
  gap: 20px; 
}

.container,
.prediction-container {
  background: #fff;
  padding: 30px;
  border-radius: 30px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.container {
  width: 70%;
}

.prediction-container {
  width: 30%;
}

.result {
  margin-top: 20px;
}

.result p {
  font-size: 23px; 
  margin-top: 10px;
  color: #333;
}

.warning-text {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #f44336;
  border-radius: 10px;
  background-color: #fdd;
  color: #f44336;
}

.warning-text p {
  font-size: 20px; 
  font-weight: bold;
  margin: 0;
}

.img-area {
  position: relative;
  width: 100%;
  height: 350px;
  background: rgb(211, 208, 208);
  margin-bottom: 30px;
  border-radius: 15px;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}

.img-area .icon {
  font-size: 100px;
}

.img-area h3 {
  font-size: 26px;
  font-weight: 500;
  margin-bottom: 6px;
  color:black;
}

.img-area p {
  color: #35bb41;
  font-size: 20px;
}

.img-area p span {
  font-weight: 600;
}

.img-area img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  z-index: 100;
}

.img-area::before {
  content: attr(data-img);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, .5);
  color: #fff;
  font-weight: 500;
  text-align: center;
  display: flex;
  justify-content: center;
  align-items: center;
  pointer-events: none;
  opacity: 0;
  transition: all .3s ease;
  z-index: 200;
}

.img-area.active:hover::before {
  opacity: 1;
}

.prediction-container h3 {
  color: black;
  font-size: 30px;
}

.select-image {
  display: block;
  width: 100%;
  padding: 16px 0;
  border-radius: 15px;
  background: blue;
  color: #fff;
  font-weight: 500;
  font-size: 24px;
  border: none;
  cursor: pointer;
  transition: all .3s ease;
}

.select-image:hover {
  background: darkblue;
}

.select-image.Submit {
  margin-top: 10px;
}

.result, .no-image {
  margin-top: 20px;
  padding: 15px;
  background-color: #f9f9f9;
}

.result h3, .no-image h3 {
  margin-bottom: 10px;
}

.no-image h3 {
  text-align: center;
}

@media (max-width: 1070px) {
  .page-container {
    flex-direction: column;
    align-items: center;
  }
  .container,
  .prediction-container {
    width: 100%;
    max-width: none; 
  }
  .prediction-container {
    margin-top: 20px; 
    max-height: 400px; 
  }
}
</style>
