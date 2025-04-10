import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import countries from 'i18n-iso-countries'

// Import the language data using ES Module syntax
import enLocale from 'i18n-iso-countries/langs/en.json'

// Register the locale
countries.registerLocale(enLocale)

const app = createApp(App)
app.config.globalProperties.$countries = countries
app.use(router)
app.mount('#app')