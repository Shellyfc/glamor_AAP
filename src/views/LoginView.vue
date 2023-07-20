<template>
  <div class="container">
    <div class="q-pa-md" style="max-width: 40%; margin: auto">
      <q-form color="secondary" @submit="submit" class="q-gutter-md">
        <q-input type="email" color="secondary" filled v-model="email" label="Your email *" hint="Email Address"
          lazy-rules :rules="[val => val && val.length > 0 || 'Please type your email']">
          <template v-slot:prepend>
            <q-icon name="email" />
          </template>
        </q-input>

        <q-input color="secondary" clearable :type="passwordFieldType" filled v-model="password" label="Your password *"
          hint="Password" lazy-rules :rules="[val => val && val.length > 0 || 'Please type your password']">
          <template v-slot:prepend>
            <q-icon name="lock" />
          </template>
          <template v-slot:append>
            <q-icon :name="visibilityIcon" @click="switchVisibility" class="cursor-pointer" />
          </template>
        </q-input>

        <!-- <q-toggle v-model=" accept" label="I accept the license and terms" /> -->

        <div>
          <q-btn color="secondary" label="Submit" type="submit" />
        </div>
      </q-form>
      <br>
      <q-btn @click="signInWithGoogle">
        <img src="../assets/google-outline.svg" style="height: 10%; width: 10%;">
      </q-btn>
      <br>
      <div class="alternative-option mt-4">
        You don't have an account?
        <q-btn flat color="secondary" label="Register" @click="moveToRegister" />
      </div>

    </div>
  </div>
</template>

<script>
import { getAuth, signInWithEmailAndPassword, GoogleAuthProvider, signInWithPopup } from "firebase/auth";
import { Notify } from 'quasar';
import { useUsersStore } from "../../src/store/user";
// import { storeToRefs } from 'pinia'

export default {
  setup() {
    const userStore = useUsersStore()
    return {
      userStore,
    }
  }
  ,
  data() {
    return {
      email: "",
      password: "",
      errorCode: "",
      visibility: false,
      passwordFieldType: 'password',
      visibilityIcon: 'visibility'
    };
  },
  methods: {
    submit() {
      const auth = getAuth();
      signInWithEmailAndPassword(auth, this.email, this.password)
        .then(() => {
          this.userStore.login(this.email);
          this.$router.push("home");
          Notify.create(
            {
              type: "positive",
              message: "Logging in...",
              timeout: 1000
            })
        })
        .catch((error) => {
          Notify.create(
            {
              type: "negative",
              message: error.message
            })
        });
    },
    signInWithGoogle() {
      const auth = getAuth();
      const provider = new GoogleAuthProvider();
      signInWithPopup(auth, provider)
        .then((result) => {
          // This gives you a Google Access Token. You can use it to access the Google API.
          // const credential = GoogleAuthProvider.credentialFromResult(result);
          // const token = credential.accessToken;
          // The signed-in user info.
          const user = result.user;
          // IdP data available using getAdditionalUserInfo(result)
          console.log(user)
          // ...
        }).catch((error) => {
          // Handle Errors here.
          // const errorCode = error.code;
          // const errorMessage = error.message;
          // // The email of the user's account used.
          // const email = error.customData.email;
          // // The AuthCredential type that was used.
          // const credential = GoogleAuthProvider.credentialFromError(error);
          // ...
          console.log(error)
        });
    },
    switchVisibility() {
      this.visibility = !this.visibility
      this.passwordFieldType = this.visibility ? 'text' : 'password'
      this.visibilityIcon = this.visibility ? 'visibility_off' : 'visibility'
    },
    moveToRegister() {
      this.$router.push("/register");
    },
  },
};
</script>
