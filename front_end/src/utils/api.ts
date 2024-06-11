import axios from 'axios'
import store from '../store/index'
import router from '@/router/index'

const request = axios.create({
  baseURL: "http://localhost:8000",
  timeout: 5000,
})

request.interceptors.request.use(
  (config) => {
    config.headers['token'] = sessionStorage.getItem('token')
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

request.interceptors.response.use(
  (response) => {
    if(response.data.code === 401) {
      sessionStorage.clear();
      store.dispatch('clearUser');
      router.replace('/login');
    }
    return response
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default request;