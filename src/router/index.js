import { createRouter, createWebHistory } from 'vue-router'
import TableView from '../views/TableView.vue'
import LoginView from "../views/LoginView.vue";
import PlayView from "../views/PlayView.vue";

const routes = [
  {
    path: '/home',
    name: 'home',
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/HomeView.vue"),
    // meta: {
    //   authRequired: true,
    // },
  },
  {
    path: "/login",
    name: "login",
    component: LoginView,
  },
  {
    path: "/register",
    name: "register",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/RegisterView.vue"),
  },
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: '/tableView',
    name: 'tableView',
    component: TableView,
  },
  {
    path: '/play',
    name: 'play',
    component: PlayView,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/DashboardView.vue"),
    meta: {
      authRequired: true,
    },
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
