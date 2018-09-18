import React from 'react'
import styled from 'styled-components'
import {Cell} from 'styled-css-grid'

// Colors
import * as colors from './colors'

// Elements
import {Button} from './elements'

// Layouts
import Page from './layouts/page'

// Components
import Sidebar from './components/sidebar'
import ToggleList from './components/toggle-list'
import PreviewTable from './components/preview-table'

// API
import api from './api'

class Export extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      preview: null
    }
  }
  componentDidMount () {
    const {id} = this.props.match.params
    api.get(`/matches/${id}/preview`, {
      params: {
        'rowsShown': 100
      }
    })
      .then(resp => {
        this.setState({preview: resp.data})
      })
  }
  getFields () {
    const {fields} = this.state.preview.schema
    return fields.filter(field => field.name !== 'index')
  }
  getColumnHighlights () {
    return {
      'PSGC': colors.green,
      'Population': colors.orange,
      'Administrative Level': colors.orange
    }
  }
  render () {
    if (!this.state.preview) {
      return null
    }
    return (
      <Page>
        <Cell width={9} className={this.props.className}>
          <PreviewTable
            preview={this.state.preview}
            columnHighlights={this.getColumnHighlights()}
          />
        </Cell>
        <Sidebar
          backButton={
            <Button className='btn -back' onClick={this.props.history.goBack}>Back</Button>
          }
          nextButton={
            <a href={`${window.API_HOST}${this.state.preview.file.url}`}>
              <Button className='btn'>Export</Button>
            </a>
          }
        >
          <ol className='steps'>
            <li>Upload your data</li>
            <li>Prep your data</li>
            <li>Review matches</li>
            <li className='current'>Check new columns and export</li>
            <li>Give feedback</li>
          </ol>
        </Sidebar>
      </Page>
    )
  }
}

export default styled(Export)`
  position: relative;
  background: ${colors.monochrome[0]};
  padding: 60px;
  box-sizing: border-box;
`
