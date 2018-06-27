import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Colors
import * as colors from './colors'

// Layouts
import Page from './layouts/page'

class Check extends React.Component {
  render () {
    return (
      <Page match={this.props.match}>
        <Cell width={10} className={this.props.className}>
          <Grid columns={1} rows='40% 60%' gap='0' height='100%'>
            <Cell>
              <iframe
                src='https://www.google.com/maps/embed/v1/place?q=place_id:ChIJr5Qp-vPIlzMRCuRgR6-IyYk&key=AIzaSyCIXyqG6o62e9kcnpLR_3Pz317ybfDWLiw'
                width='100%'
                height='100%'
                frameborder='0'
                allowfullscreen
              />
            </Cell>
            <Cell className='matches'>
            </Cell>
          </Grid>
        </Cell>
      </Page>
    )
  }
}

export default styled(Check)`
  position: relative;
  .matches {
    background: ${colors.monochrome[1]};
  }
`
