<template>
  <div>
    <div class="text-center">You're now logged as</div>
    <div id="username_display" class="display-6">{{ this.email }}</div>
    <q-btn color="secondary" flat label="Logout" @click="signOut" />
  </div>
</template>

<script>
import { getAuth } from "firebase/auth";
import { useUsersStore } from "../../src/store/user";
import { Notify } from 'quasar';

const auth = getAuth();

export default {
  setup() {
    const useUserStore = useUsersStore();
    return {
      useUserStore
    };
  },
  data() {
    return {
      email: auth.currentUser.email,
    };
  },
  methods: {
    signOut() {
      auth
        .signOut()
        .then(() => {
          console.log("Sign Out completed");
          this.useUserStore.logout();
          this.email = '';
          Notify.create(
            {
              type: "positive",
              message: "Loged out",
              timeout: 1000
            }
          )
          this.$router.push("/login");
        })
        .catch((error) => console.log(error));
    },
  },
};
</script>
