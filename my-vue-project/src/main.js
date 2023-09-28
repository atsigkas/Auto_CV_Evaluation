import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store';

//axios.defaults.baseURl = 'http://127.0.0.1:8000'

createApp(App).use(router).use(store).mount('#app')
