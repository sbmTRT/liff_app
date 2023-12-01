<template>
  <div id="app">
    <Header />
    <div v-if="currentView === 'home'">
      <Home />
    </div>
    <div v-else-if="currentView === 'about'">
      <About />
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import Home from './views/Home.vue';
import About from './views/About.vue';

export default {
  components: {
    Header,
    Footer,
    Home,
    About,
  },
  data() {
    return {
      currentView: 'home', // Set the default view
    };
  },
  // App-level logic goes here
}
</script>

<style>
/* Global styles go here */
</style>
