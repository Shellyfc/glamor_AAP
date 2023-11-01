<template>
  <div class="container">
    <div class="q-pa-md" style="max-width: 40%; margin: auto">
      <q-form color="secondary" @submit="register" class="q-gutter-md">
        <q-input type="email" color="secondary" v-model="email" label="Your email *" hint="Email Address" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type your email']">
          <template v-slot:prepend>
            <q-icon name="email" />
          </template>
        </q-input>

        <q-input color="secondary" ref="password" clearable :type="passwordFieldType" v-model="password"
          label="Your password *" hint="Password" lazy-rules
          :rules="[val => val && val.length > 0 || 'Please type your password']">
          <template v-slot:prepend>
            <q-icon name="lock" />
          </template>
          <template v-slot:append>
            <q-icon :name="visibilityIcon" @click="switchVisibility" class="cursor-pointer" />
          </template>
        </q-input>

        <q-input color="secondary" ref="repassword" clearable v-model="repassword" :type="passwordFieldType" lazy-rules
          :rules="[this.diffPassword]" label="Password Confirmation" hint="Re-type password">
          <template v-slot:prepend>
            <q-icon name="lock" />
          </template>
          <template v-slot:append>
            <q-icon :name="visibilityIcon" @click="switchVisibility" class="cursor-pointer" />
          </template>
        </q-input>
        <!-- <q-toggle v-model=" accept" label="I accept the license and terms" /> -->

        <div>
          <q-btn color="secondary" label="Register" type="register" />
        </div>
      </q-form>
      <br>
      <div class="alternative-option mt-4">
        Already have an account?
        <q-btn flat color="secondary" label="Login" @click="moveToLogin" />
      </div>

    </div>
  </div>
</template>

<script>
import { getAuth, createUserWithEmailAndPassword } from "firebase/auth";
import { Notify } from 'quasar';

export default {
  data() {
    return {
      email: "",
      password: "",
      repassword: "",
      visibility: false,
      passwordFieldType: 'password',
      visibilityIcon: 'visibility'
    };
  },
  methods: {
    register() {
      // data update
      // this.email = submitEvent.target.elements.email.value;
      // this.password = submitEvent.target.elements.password.value;

      // firebase registration
      const auth = getAuth();
      createUserWithEmailAndPassword(auth, this.email, this.password)
        .then((userCredential) => {
          const user = userCredential.user;
          console.log(user);
          console.log("Registration completed");
          Notify.create(
            {
              type: "positive",
              message: "Registration succeeded",
              timeout: 1000
            }
          )
          this.$router.push("/home");
        })
        .catch((error) => {
          Notify.create(
            {
              type: "negative",
              message: error.message
            }
          )
        });
    },
    diffPassword(val) {
      return (val && (val == this.password) || "Passwords don't match!")
    },
    switchVisibility() {
      this.visibility = !this.visibility
      this.passwordFieldType = this.visibility ? 'text' : 'password'
      this.visibilityIcon = this.visibility ? 'visibility_off' : 'visibility'
    },
    moveToLogin() {
      this.$router.push("/");
    },
  },
};
</script>
