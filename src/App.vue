<template>
  <nav>
    <router-link to="/home">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link to="/tableView">Search</router-link> |
    <router-link to="/play">Play</router-link>
    <div class="nav-el">
      <!-- <a href="https://github.com/vladpostu/vue-firebase-auth" target="blank"
          >GitHub Repo</a
        > -->
      <span v-if="isLoggedIn">
        <router-link to="/dashboard">{{ email }}</router-link>
      </span>
      <span v-else>
        <router-link to="/login">Log in</router-link>
      </span>
    </div>
  </nav>
  <router-view />
</template>

<style lang="scss">
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;

  a {
    font-weight: bold;
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
</style>


<script setup>
import { ref } from 'vue' // used for conditional rendering
// import firebase from 'firebase'
import { getAuth } from "firebase/auth";
import { useUsersStore } from "../src/store/user";
import { useRouter } from 'vue-router'
import { Notify } from 'quasar';

const isLoggedIn = ref(true)
const email = ref(null)
const userStore = useUsersStore()
const router = useRouter()
// runs after firebase is initialized
getAuth().onAuthStateChanged(function (user) {
  if (user) {
    isLoggedIn.value = true // if we have a user
    email.value = user.email
    userStore.login(user.email)
    Notify.create(
      {
        type: "positive",
        message: "Loged in",
        timeout: 1000
      }
    )
    router.push("/dashboard");
  } else {
    isLoggedIn.value = false // if we do not
  }
})
// const signOut = () => {
//   getAuth().signOut()
//   router.push('/')
// }

</script>
<!-- <script>
// import { getAuth } from "firebase/auth";
// const auth = getAuth();
import { auth } from "./main"
import { getAuth } from "firebase/auth";
export default {
  data() {
    return {
      email: "",
    };
  },
  created() {
    getAuth().onAuthStateChanged(function(user) {
      if (user) {
        // User is signed in, see docs for a list of available properties
        // https://firebase.google.com/docs/reference/js/firebase.User
        this.email = user.email
        // ...
      } else {
        // User is signed out
        // ...
      }
    });
  },
  methods: {

    signOut() {
      auth
        .signOut()
        .then(() => {
          console.log("Sign Out completed");
          this.$router.push("/");
        })
        .catch((error) => console.log(error));
    },
  },
};
</script> -->

