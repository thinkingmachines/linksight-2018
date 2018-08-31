import axios from 'axios'

export default axios.create({
  baseURL: `${window.API_HOST}/api`,
  withCredentials: true
})
