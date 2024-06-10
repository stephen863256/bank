<template>
  <!--
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/login">Login</router-link> |
    <router-link to="/layout/user">User</router-link> |
    <router-link to="/layout/client">Client</router-link> |
    <router-link to="/layout/branch">Branch</router-link> |
    <router-link to="/layout/department">Department</router-link> |
    <router-link to="/layout/employee">Employee</router-link> |
    <router-link to="/layout/creditAccount">Credit Account</router-link> |
    <router-link to="/layout/savingsAccount">Savings Account</router-link> |
    <router-link to="/layout/loan">Loan</router-link> |
    <router-link to="/layout/repayment">Repayment</router-link> |
  </nav>
  -->
  <router-view/>
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50; 
}

nav { 
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
