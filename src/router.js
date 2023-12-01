// Import necessary dependencies
import Vue from 'vue';
import VueRouter from 'vue-router';
import Login from '@/views/Login.vue'; // Import your Login.vue component
import Main from '@/views/Main.vue';     // Import your Main.vue component

// Use VueRouter plugin
Vue.use(VueRouter);

// Define your routes
const routes = [
    {
        path: '/',
        redirect: '/login', // Redirect to the login page by default
    },
    {
        path: '/login',
        name: 'login',
        component: Login,
    },
    {
        path: '/main',
        name: 'main',
        component: Main,
    },
    // Add other routes as needed
];

// Create a new VueRouter instance
const router = new VueRouter({
    mode: 'history', // Use history mode for clean URLs (requires server configuration)
    routes,
});

// Export the router instance
export default router;
