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
import LoadingOverlay from './components/loading-overlay'
import Topbar from './components/topbar'

// Pages
import Upload from './upload'
import Preview from './preview'
import Check from './check'
import Export from './export'
import MobileNotice from './mobile-notice'

// API
import api from './api'

class App extends React.Component {
  constructor (props) {
    super(props)
    const mql = window.matchMedia('(max-width: 1000px)')
    this.state = {
      isLoading: true,
      isMobile: !!mql.matches
    }
  }
  componentDidMount () {
    api.get('/users/me')
      .then(() => {
        this.setState({isLoading: false})
      })
      .catch(error => {
        if (error.response.status === 403) {
          window.location.href = '/accounts/login'
        }
      })
  }
  render () {
    if (this.state.isLoading) {
      return <LoadingOverlay />
    }
    if (this.state.isMobile) {
      return <MobileNotice />
    }
    return (
      <div className={'app ' + this.props.className}>
        <Topbar />
        <Switch>
          <Route exact path='/' component={Upload} />
          <Route exact path='/datasets/:id/preview' component={Preview} />
          <Route exact path='/matches/:id/check' component={Check} />
          <Route exact path='/matches/:id/export' component={Export} />
        </Switch>
      </div>
    )
  }
}

export default styled(App)`
  background: ${colors.indigo} url(${backgroundCircle}) no-repeat -60vw -60vh;
  background-size: 100vw;
`
