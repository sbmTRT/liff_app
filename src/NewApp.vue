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
        const response = await fetch('/.netlify/functions/fastapi/get_data');
        const data = await response.json();
        alert(data.message);s
      } catch (error) {
        console.error('Error calling function:', error);
      }
    },
  },
};
</script>
