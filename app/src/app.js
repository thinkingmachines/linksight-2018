import React from 'react'
import {Route, Switch} from 'react-router-dom'
import styled from 'styled-components'

// Stylesheets
import 'filepond/dist/filepond.min.css'

// Images
import backgroundCircle from './images/background-circle.svg'

// Colors
import * as colors from './colors'

// Components
import Topbar from './components/topbar'
import RequestToken from './components/request-token'

// Pages
import Home from './home'
import Upload from './upload'
import Preview from './preview'
import Check from './check'
import Export from './export'
import Feedback from './feedback'
import MobileNotice from './mobile-notice'

class App extends React.Component {
  constructor (props) {
    super(props)
    const mql = window.matchMedia('(max-width: 1000px)')
    this.state = {
      isMobile: !!mql.matches
    }
  }
  render () {
    if (this.state.isMobile) {
      return <MobileNotice />
    }
    return (
      <div className={'app ' + this.props.className}>
        <Topbar />
        <RequestToken />
        <Switch>
          <Route exact path='/' component={Home} />
          <Route exact path='/upload' component={Upload} />
          <Route exact path='/datasets/:id/preview' component={Preview} />
          <Route exact path='/matches/:id/check' component={Check} />
          <Route exact path='/matches/:id/export' component={Export} />
          <Route exact path='/feedback' component={Feedback} />
        </Switch>
      </div>
    )
  }
}

export default styled(App)`
  background: ${colors.indigo} url(${backgroundCircle}) no-repeat -60vw -60vh;
  background-size: 100vw;
`
