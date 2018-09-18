import React from 'react'
import styled from 'styled-components'
import {Cell} from 'styled-css-grid'

// Layouts
import Page from './layouts/page'

class Feedback extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      preview: null
    }
  }

  render () {
    if (!this.state.preview) {
      return null
    }
    return (
      <Page>
        <Cell width={9} className={this.props.className}>
          <Grid columns={12} gap='15px' height='100%' className='upload'>
            <Cell width={6} left={4} alignContent='center' middle />
          </Grid>
        </Cell>
        <Sidebar>
          <ol className='steps'>
            <li>Upload your data</li>
            <li>Prep your data</li>
            <li>Review matches</li>
            <li>Check new columns and export</li>
            <li className='current'>Give feedback</li>
          </ol>
        </Sidebar>
      </Page>
  }
}

export default styled(Feedback)`

`
