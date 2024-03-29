import { defineStore } from 'pinia'
// import { getAuth } from "firebase/auth";

// const auth = getAuth();
// 'user' is the unique id in the store
export const useUsersStore = defineStore('user', {
    // other options...
    state: () => ({
    username: '',
    token: ''
  }),
   
  // 定义 getters，等同于组件的计算属性
  getters: {
    // getter 函数接收 state 作为参数，推荐使用箭头函数
    logined: state => state.username != ''
  },
  
  // 定义 actions，有同步和异步两种类型
  actions: {
    // 异步 action，一般用来处理异步逻辑
    // async login(userData) {
    //   const result = await axios.post('/api/user/login', userData)
    //   const { data, code } = result.data
    //   if (code === 0) {
    //     // action 中修改状态
    //     this.username = data.username
    //     this.token = data.token
    //   }
    // },
      login(username)
      {
        this.username = username  
      },

    // 同步 action
    logout() {
      this.token = ''
      this.username = ''
    }
  }
})