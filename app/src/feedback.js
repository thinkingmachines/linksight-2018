import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Colors
import * as colors from './colors'

// Elements
import {Button} from './elements'

// Layouts
import Page from './layouts/page'

// Components
import Sidebar from './components/sidebar'

class Feedback extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      isDone: null
    }
  }
  componentDidMount () {
    const script = document.createElement('script')
    script.src = 'https://static.airtable.com/js/embed/embed_snippet_v1.js'
    script.async = true

    document.body.appendChild(script)
  }
  uploadNewDataset () {
    this.setState({isDone: true})
  }
  render () {
    if (this.state.isDone) {
      return <Redirect push to={`/upload`} />
    }
    return (
      <Page>
        <Cell width={9} className={this.props.className}>
          <Grid columns={12} gap='15px' height='100%' className='feedback' middle>
            <Cell width={8} left={3} alignContent='center' middle>
              <iframe className='airtable-embed airtable-dynamic-height' src='https://airtable.com/embed/shr7b1eauaxFWw1et?backgroundColor=teal' onWheel={(e) => this.wheel(e)} />
            </Cell>
          </Grid>
        </Cell>
        <Sidebar
          button={
            <Button className='btn' onClick={this.uploadNewDataset.bind(this)}>Upload new dataset</Button>
          }
        >
          <ol className='steps'>
            <li>Upload your data</li>
            <li>Prep your data</li>
            <li>Review matches</li>
            <li>Check new columns and export</li>
            <li className='current'>
              <p>Give feedback</p>
              <p className='step-desc'>Let us know if you found any issues or if you have any suggestions or feature requests.</p>
            </li>
          </ol>
        </Sidebar>
      </Page>
    )
  }
}

export default styled(Feedback)`
  background: ${colors.monochrome[0]};
  .feedback .airtable-embed {
    width: 100%;
    height: 100%;
    background: transparent;
    border: 2px solid ${colors.monochrome[1]};
  }
`
