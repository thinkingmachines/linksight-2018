import React from 'react'
import {Route, Switch} from 'react-router-dom'
import styled from 'styled-components'

// Stylesheets
import './css/app.css'
import './css/typography.css'
import './css/react-toggle.css'
import 'filepond/dist/filepond.min.css'

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
          <Route exact path='/:id/preview' component={Preview} />
          <Route exact path='/:id/check' component={Check} />
        </Switch>
      </div>
    )
  }
}

export default styled(App)`
  background: ${colors.indigo};
  &:before {
    content: ' ';
    width: 100%;
    padding-bottom: 100%;
    display: block;
    background: ${colors.monochrome[0]};
    border-radius: 50%;
    position: absolute;
    top: -25%;
    left: -55%;
  }
`
