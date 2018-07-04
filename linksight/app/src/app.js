import React from 'react'
import {Route, Switch} from 'react-router-dom'
import styled from 'styled-components'

// Stylesheets
import './css/app.css'
import './css/typography.css'
import './css/react-toggle.css'
import 'filepond/dist/filepond.min.css'

// Images
import backgroundCircle from './images/background-circle.svg'

// Colors
import * as colors from './colors'

// Pages
import Upload from './upload'
import Preview from './preview'
import Check from './check'

class App extends React.Component {
  render () {
    return (
      <div className={'app ' + this.props.className}>
        <Switch>
          <Route exact path='/' component={Upload} />
          <Route exact path='/datasets/:id/preview' component={Preview} />
          <Route exact path='/matches/:id/check' component={Check} />
        </Switch>
      </div>
    )
  }
}

export default styled(App)`
  background: ${colors.indigo} url(${backgroundCircle}) no-repeat -300% 75%;
  background-size: 150vh;
`
