<template>
    <div class="home">
      <h1 class="title">Pneumonia Detector</h1>
      <UploadForm />
    </div>
</template>

<script>
import UploadForm from '../components/UploadForm.vue'; 

export default {
  name: 'App',
  components: {
    UploadForm
  }
}
</script>

<style scoped>
.home{
  justify-content: center;
  align-items: center;
}

.title{
  font-size: 70px;
  text-align: center;
  margin-bottom: 20px;
  margin-top: 20px;
}


</style>
