import { createApp } from 'vue'
import App from './App.vue'
import { Quasar, Loading, Notify } from 'quasar'
import quasarUserOptions from './quasar-user-options'
import router from './router'

// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { createPinia } from "pinia";
import { useUsersStore } from "./store/user"
// import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyADSf8yj-AFdKYMceIOYc5vMvGrfmwr-ck",
  authDomain: "glamor-f4e46.firebaseapp.com",
  projectId: "glamor-f4e46",
  storageBucket: "glamor-f4e46.appspot.com",
  messagingSenderId: "816329817401",
  appId: "1:816329817401:web:6fc20be53d0225f020bce8",
  measurementId: "G-VBT7RQCSDE"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
// const analytics = getAnalytics(app);
export default app;
export const auth = getAuth(app);

// pinia init
const pinia = createPinia();

// preceptor
router.beforeEach((to, from, next) => {
  const userStore = useUsersStore()
  let logined = userStore.logined
  if (to.name == "register") {
    next()
  }
  else if(to.name=="login"){
    if(!logined){
      next();
    }else{
      router.replace("/home");
    }
  }else{
    if (!logined) {
      Notify.create(
            {
              type: "warning",
              message: "You have to log in",
              timeout: 2000
            })
      router.replace({path:"login", query:{redirect:to.name}});
    }else{
      next();
    }
  }
}),

createApp(App).use(pinia).use(router).use(Quasar, {
  plugins: {
    Loading,
    Notify
  },
  config: {
    loading: { /* look at QuasarConfOptions from the API card */ },
    notify: { /* look at QuasarConfOptions from the API card */ },
    brand: "secondary"
  }
}).use(Quasar, quasarUserOptions).mount('#app')