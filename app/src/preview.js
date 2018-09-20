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
        <Sidebar
          backButton={
            <Button
              className='btn -back'
              onClick={this.props.history.goBack}
            >
              Back
            </Button>
          }
          nextButton={
            <Button
              className='btn -proceed'
              disabled={!this.hasLocationColumnsSelected() || this.state.isMatching}
              onClick={this.match.bind(this)}
            >
              Next
            </Button>
          }
        >
          <ol className='steps'>
            <li>Upload your data</li>
            <li className='current'>
              <p>Prep your data</p>
              <ul className='step-desc'>
                <li>Select all the administrative units available as columns in your dataset.</li>
                <li>Our tool matches your data against standard barangay, municipality/city, province names in our database.</li>
                <li>The more administrative levels are specified, the better LinkSight can match them.</li>
              </ul>
            </li>
            <li>Review matches</li>
            <li>Check new columns and export</li>
            <li>Give feedback</li>
          </ol>
        </Sidebar>
        <Cell width={9} className={this.props.className}>
          <Grid columns={12} gap='0' height='100%' alignContent='stretch'>
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
              <Grid columns={12} gap='0' height='100%' alignContent='stretch'>
                <Cell width={3} className='location-columns' middle>
                  <Instruction>
                    Indicate which column headers in your dataset refer to the following administrative levels. You may leave a field blank if it's not in your dataset.
                  </Instruction>
                  <br />
                  <LocationColumn
                    name='Barangay'
                    color={colors.indigo}
                    columnOptions={this.getColumnOptions()}
                    onChange={this.selectLocationColumn.bind(this, 'barangay')}
                  />
                  <br />
                  <LocationColumn
                    name='City/Municipality'
                    color={colors.teal}
                    columnOptions={this.getColumnOptions()}
                    onChange={this.selectLocationColumn.bind(this, 'city_municipality')}
                  />
                  <br />
                  <LocationColumn
                    name='Province'
                    color={colors.orange}
                    columnOptions={this.getColumnOptions()}
                    onChange={this.selectLocationColumn.bind(this, 'province')}
                  />
                </Cell>
                <Cell width={9} className='preview-table'>
                  <PreviewTable
                    preview={this.state.preview}
                    columnHighlights={this.getColumnHighlights()}
                  />
                </Cell>
              </Grid>
            </Cell>
          </Grid>
        </Cell>
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
    overflow-y: auto;
  }
  .preview-table, .location-columns {
    box-sizing: border-box;
  }
  .preview-table {
    padding: 40px 0 40px 30px;
  }
  .location-columns {
    box-sizing: border-box;
    min-height: 540px;
    padding: 40px 40px;
    background: ${colors.monochrome[0]};
    border-right: 1px solid ${colors.monochrome[2]};
    position: relative;
  }
  .buttons .btn.-proceed {
    position: absolute;
    bottom: 40px;
  }
`
