<template>
  <div>
    <button @click="callFunction">Call Netlify Function</button>
  </div>
</template>

<script>
export default {
  methods: {
    async callFunction() {
      try {
        const response = await fetch('/.netlify/functions/hello');
        const data = await response.json();
        alert(data.message); // Show an alert message
      } catch (error) {
        console.error('Error calling function:', error);
      }
    },
  },
};
</script>
