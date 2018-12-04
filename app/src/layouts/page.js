import React from 'react'
import {Redirect} from 'react-router-dom'
import styled from 'styled-components'
import {Grid} from 'styled-css-grid'
import api from '../api'

class Page extends React.Component {
  constructor (props) {
    super(props)
    if (this.props.restricted) {
      this.state = {authorized: true}
      api.get('users/me').catch(e => this.setState({authorized: false}))
    }
  }
  render () {
    if (this.props.restricted && !this.state.authorized) {
      return <Redirect push to={`/`} />
    } else {
      return (
        <Grid
          columns={12}
          rows={this.props.withHeader ? '100px 1fr' : 1}
          gap='0'
          className={this.props.className}
        >
          {this.props.children}
        </Grid>
      )
    }
  }
}

export default styled(Page)`
  min-height: calc(100vh - 30px);
`
