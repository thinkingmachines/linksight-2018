import React, { Component } from 'react'
import { FilePond } from 'react-filepond'

import 'filepond/dist/filepond.min.css'

class App extends Component {
  render () {
    return (
      <div className='App'>
        <FilePond
          name='file'
          server='http://localhost:8000/api/datasets/'
          allowRevert={false}
        />
      </div>
    )
  }
}

export default App
