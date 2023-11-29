<!-- MyButton.vue -->
<template>
  <div>
    <button @click="getData">Click me!</button>
  </div>
</template>

<script>
export default {
  methods: {
    async getData() {
      try {
        const response = await fetch('http://127.0.0.1:8000/getAll');
        const data = await response.json();
        alert(`Response from server: ${JSON.stringify(data)}`);
      } catch (error) {
        console.error('Error calling FastAPI function:', error);
        alert('Error calling FastAPI function');
      }
    }
  }
}
</script>

<style scoped>
/* Add your component styles here if needed */
</style>
