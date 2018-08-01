import React from 'react'
import ReactDOM from 'react-dom'
import App from './app'
import {BrowserRouter} from 'react-router-dom'

ReactDOM.render(
  <BrowserRouter><App /></BrowserRouter>,
  document.getElementById('app-root')
)

window.modalRoot = document.getElementById('modal-root')
