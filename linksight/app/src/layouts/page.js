import React from 'react'
import styled from 'styled-components'
import {Grid} from 'styled-css-grid'

class Page extends React.Component {
  render () {
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

export default styled(Page)`
  min-height: 100vh;
`
