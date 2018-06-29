import React from 'react'
import styled from 'styled-components'
import {Grid} from 'styled-css-grid'

// Components
import Header from '../components/header'
import Sidebar from '../components/sidebar'

class Page extends React.Component {
  // TODO: Refactor - split up to different layouts
  isHeaderShown () {
    return ~[
      '/',
      '/:id/preview'
    ].lastIndexOf(this.props.match.path)
  }
  isSidebarShown () {
    return !this.isHeaderShown()
  }
  render () {
    return (
      <Grid
        columns={12}
        rows={this.isHeaderShown() ? '100px 1fr' : 1}
        gap='0'
        className={this.props.className}
      >
        {this.isHeaderShown() ? <Header /> : null}
        {this.isSidebarShown() ? <Sidebar /> : null}
        {this.props.children}
      </Grid>
    )
  }
}

export default styled(Page)`
  min-height: 100vh;
`
