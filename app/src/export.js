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
        <Sidebar button={
          <a href={`${window.API_HOST}${this.state.preview.file.url}`}>
            <Button>Export</Button>
          </a>
        }>
          <ToggleList
            title='Datasets'
            bullet='square'
            items={[
              {
                toggled: true,
                color: colors.green,
                label: 'PSGC'
              },
              {
                toggled: true,
                color: colors.orange,
                label: 'Population'
              }
            ]}
          />
          <ToggleList
            title='Columns'
            bullet='circle'
            items={this.getFields().map(field => ({
              toggled: true,
              label: field.name
            }))}
          />
        </Sidebar>
        <Cell width={10} className={this.props.className}>
          <PreviewTable
            preview={this.state.preview}
            columnHighlights={this.getColumnHighlights()}
          />
        </Cell>
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
