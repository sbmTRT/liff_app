<template>
    <div>
        <h2>Main Page</h2>

        <div>
            <p>Username: {{ $route.params.username }}</p>
            <p>Password: {{ $route.params.password }}</p>
        </div>
    </div>
</template>

<script>
export default {
    // Add any necessary logic for the main page component
};
</script>

<style scoped>
    /* Add your custom styles here */
    /* ... */
</style>
