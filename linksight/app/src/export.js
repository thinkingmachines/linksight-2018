import React from 'react'
import styled from 'styled-components'
import axios from 'axios'
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

class Export extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      preview: null
    }
  }
  componentDidMount () {
    const {id} = this.props.match.params
    axios.get(`${window.API_HOST}/api/matches/${id}/preview`)
      .then(resp => {
        this.setState({preview: resp.data})
      })
  }
  getFields () {
    const {fields} = this.state.preview.schema
    return fields.filter(field => field.name !== 'index')
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
                toggled: false,
                color: colors.orange,
                label: 'Population'
              },
              {
                toggled: false,
                color: colors.green,
                label: 'Disaster Risk Factor'
              },
              {
                toggled: false,
                color: colors.purple,
                label: 'Competitiveness Score'
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
