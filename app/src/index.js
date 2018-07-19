import React from 'react'
import ReactDOM from 'react-dom'
import App from './app'
import {BrowserRouter} from 'react-router-dom'
import registerServiceWorker from './registerServiceWorker'

ReactDOM.render(
  <BrowserRouter><App /></BrowserRouter>,
  document.getElementById('app-root')
)
registerServiceWorker()

window.modalRoot = document.getElementById('modal-root')
