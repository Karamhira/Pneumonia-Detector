<template>
    <div class="home">
      <h1>Pneumonia Detector</h1>
      <input type="file" @change="onFileChange" />
      <button @click="uploadImage" :disabled="!file">Upload Image</button>
      <div v-if="result" class="result">
        <h2>Diagnosis Result:</h2>
        <p>{{ result }}</p>
      </div>
    </div>
  </template>