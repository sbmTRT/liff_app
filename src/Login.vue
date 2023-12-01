<template>
    <div>
        <h2>Student Information Login</h2>

        <form @submit.prevent="submitForm">
            <label for="username">Username:</label>
            <input type="text" v-model="username" required>

            <label for="password">Password:</label>
            <input type="password" v-model="password" required>

            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>
export default {
    data() {
        return {
            username: '',
            password: ''
        };
    },
    methods: {
        submitForm() {
            // You can add your logic here to handle the login submission
            // For simplicity, let's show an alert with the entered username and password
            alert('Username: ' + this.username + '\nPassword: ' + this.password);

            // You may want to redirect or perform other actions based on the login information
        }
    }
};
</script>

<style scoped>
    /* Add your custom styles here */
    body {
        font-family: Arial, sans-serif;
        margin: 20px;
    }
    form {
        max-width: 400px;
        margin: 0 auto;
    }
    label {
        display: block;
        margin-bottom: 8px;
    }
    input {
        width: 100%;
        padding: 8px;
        margin-bottom: 16px;
        box-sizing: border-box;
    }
    button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 15px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    button:hover {
        background-color: #45a049;
    }
</style>
