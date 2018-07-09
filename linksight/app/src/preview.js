import React from 'react'
import styled from 'styled-components'
import axios from 'axios'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Colors
import * as colors from './colors'

// Layouts
import Page from './layouts/page'

// Components
import Header from './components/header'
import PreviewTable from './components/preview-table'
import LocationColumn from './components/location-column'
import LoadingOverlay from './components/loading-overlay'

// Elements
import {Button, Instruction} from './elements'

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
    axios.get(`${window.API_HOST}/api/datasets/${id}/preview`)
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
      selectedLocationColumns.barangay &&
      selectedLocationColumns.city_municipality &&
      selectedLocationColumns.province
    )
  }
  match () {
    this.setState({isMatching: true})
    const {selectedLocationColumns} = this.state
    const {id} = this.props.match.params
    axios.post(
      `${window.API_HOST}/api/datasets/${id}/match`, {
        barangay_col: selectedLocationColumns.barangay,
        city_municipality_col: selectedLocationColumns.city_municipality,
        province_col: selectedLocationColumns.province
      })
      .then(resp => this.setState({matchId: resp.data.id}))
  }
  render () {
    if (!this.state.preview) {
      return null
    }
    if (this.state.matchId) {
      return <Redirect push to={`/matches/${this.state.matchId}/check`} />
    }
    return (
      <Page withHeader>
        <Header />
        <Cell width={12} className={this.props.className}>
          <div className='overlay' />
          <Grid columns={12} gap='0' height='100%' alignContent='center'>
            <Cell width={10} left={2} className='box'>
              {this.state.isMatching ? (
                <LoadingOverlay>Matching&hellip;</LoadingOverlay>
              ) : null}
              <Grid columns={10} gap='0' alignContent='space-between'>
                <Cell width={8} className='preview'>
                  <PreviewTable
                    preview={this.state.preview}
                    columnHighlights={this.getColumnHighlights()}
                  />
                </Cell>
                <Cell width={2} className='location-columns'>
                  <Instruction>
                    Select the following<br />
                    location columns:
                  </Instruction>
                  <br />
                  <br />
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
                  {this.hasLocationColumnsSelected() && (
                    <Button
                      className='proceed'
                      onClick={this.match.bind(this)}
                    >
                      Proceed
                    </Button>
                  )}
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
  }
  .preview, .location-columns {
    box-sizing: border-box;
  }
  .preview {
    padding: 40px 0 40px 30px;
  }
  .location-columns {
    padding: 40px 30px;
    background: ${colors.monochrome[1]};
    border-left: 1px solid ${colors.monochrome[2]};
    position: relative;
  }
  .proceed {
    position: absolute;
    bottom: 40px;
  }
`
