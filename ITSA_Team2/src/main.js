
import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { getData } from 'country-list'
import VueTelInput from 'vue-tel-input'
import 'vue-tel-input/vue-tel-input.css'

const app = createApp(App)
// Make country data available globally
app.config.globalProperties.$countries = {
    getCountryData: () => getData()
}

app.use(router)
app.use(VueTelInput)
app.mount('#app')