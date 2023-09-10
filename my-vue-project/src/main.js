import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'

//axios.defaults.baseURl = 'http://127.0.0.1:8000'

createApp(App).use(router,axios).mount('#app')
