import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Colors
import * as colors from './colors'

// Layouts
import Page from './layouts/page'

// Components
import Sidebar from './components/sidebar'
import PreviewTable from './components/preview-table'
import LocationColumn from './components/location-column'
import LoadingOverlay from './components/loading-overlay'
import ErrorOverlay from './components/error-overlay'

// Elements
import {Button, Instruction} from './elements'

// API
import api from './api'

// Constants
const highlightColors = {
  'barangay': colors.indigo,
  'city_municipality': colors.teal,
  'province': colors.orange
}

class Preview extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      preview: null,
      selectedLocationColumns: {},
      isMatching: false,
      matchId: null
    }
  }
  componentDidMount () {
    const {id} = this.props.match.params
    api.get(`/datasets/${id}/preview`)
      .then(resp => {
        this.setState({preview: resp.data})
      })
  }
  getFields () {
    const {fields} = this.state.preview.schema
    return fields.filter(field => field.name !== 'index')
  }
  getColumnOptions () {
    return this.getFields().map(field => ({
      label: field.name,
      value: field.name
    }))
  }
  getColumnHighlights () {
    const {selectedLocationColumns} = this.state
    const highlights = {}
    for (let locationType in selectedLocationColumns) {
      let column = selectedLocationColumns[locationType]
      if (column) {
        highlights[column] = highlightColors[locationType]
      }
    }
    return highlights
  }
  selectLocationColumn (locationType, column) {
    const {selectedLocationColumns} = this.state
    this.setState({
      selectedLocationColumns: {
        ...selectedLocationColumns,
        [`${locationType}`]: column
      }
    })
  }
  hasLocationColumnsSelected () {
    const {selectedLocationColumns} = this.state
    return (
      selectedLocationColumns.barangay ||
      selectedLocationColumns.city_municipality ||
      selectedLocationColumns.province
    )
  }
  match () {
    this.setState({isMatching: true})
    const {selectedLocationColumns} = this.state
    const {id} = this.props.match.params
    api.post(
      `/datasets/${id}/match`, {
        barangay_col: selectedLocationColumns.barangay,
        city_municipality_col: selectedLocationColumns.city_municipality,
        province_col: selectedLocationColumns.province
      })
      .then(resp => this.setState({matchId: resp.data.id}))
      .catch(_ => this.setState({
        isMatching: false,
        error: <p>
          Uh oh! An unexpected error has occured.<br />
          We've been notified about this and will try to<br />
          look into it as soon as possible!
        </p>
      }))
  }
  render () {
    if (!this.state.preview) {
      return null
    }
    if (this.state.matchId) {
      return <Redirect push to={`/matches/${this.state.matchId}/check`} />
    }
    return (
      <Page>
        <Cell width={9} className={this.props.className}>
          <Grid columns={12} gap='0' height='100%' alignContent='center' className='preview'>
            <Cell width={12} className='box'>
              {this.state.isMatching ? (
                <LoadingOverlay>Cleaning your dataset. Don't leave!<br />
                This will take a few minutes.</LoadingOverlay>
              ) : null}
              {this.state.error ? (
                <ErrorOverlay>
                  {this.state.error}
                </ErrorOverlay>
              ) : null}
              <Grid columns={12} gap='0' alignContent='space-between'>
                <Cell width={12} className='preview'>
                  <PreviewTable
                    preview={this.state.preview}
                    columnHighlights={this.getColumnHighlights()}
                  />
                </Cell>
              </Grid>
            </Cell>
          </Grid>
        </Cell>
        <Sidebar>
          <ol className='steps'>
            <li>Upload your data</li>
            <li className='current'>
              <p>Prep your data</p>
              <p className='step-desc'>
                Select the columns in your dataset that refer to locations for cleaning. If you need to standardize either barangays or municipalities/cities, please choose at least two columns (ex: barangay & municipality, municipality & province).
              </p>
            </li>
            <li>Clean your data</li>
            <li>Check and export</li>
          </ol>
        </Sidebar>
      </Page>
    )
  }
}

export default styled(Preview)`
  position: relative;
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    background: ${colors.indigo};
    opacity: 0.5;
    height: 100%;
    width: 100%;
  }
  .box {
    position: relative;
    background: ${colors.monochrome[0]};
  }
  .preview, .location-columns {
    box-sizing: border-box;
  }
  .preview {
    padding: 40px 0 40px 30px;
  }
  .location-columns {
    box-sizing: border-box;
    min-height: 540px;
    padding: 40px 30px;
    background: ${colors.monochrome[1]};
    border-left: 1px solid ${colors.monochrome[2]};
    position: relative;
  }
  .proceed {
    position: absolute;
    bottom: 40px;
  }
  .preview {
    background: ${colors.monochrome[1]};
    padding: 30px;
    box-sizing: border-box;
    overflow-y: auto;
  }
`
