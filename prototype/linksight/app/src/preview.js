import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import axios from 'axios'
import {fileSize} from 'humanize-plus'

// Colors
import * as colors from './colors'

// Components
import PreviewTable from './components/preview-table'
import LocationColumn from './components/location-column'

// Elements
import {Button} from './elements'

// Constants
const highlightColors = {
  'barangay': colors.indigo,
  'city_municipality': colors.teal,
  'province': colors.orange,
}

class Preview extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      preview: null,
      selectedLocationColumns: {}
    }
  }
  componentDidMount () {
    let {id} = this.props.match.params
    axios.get(`http://localhost:8000/api/datasets/${id}/preview`)
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
  render () {
    if (!this.state.preview) {
      return null
    }
    const {file} = this.state.preview
    return (
      <div className={this.props.className}>
        <div className='overlay' />
        <Grid columns={12} gap='0' alignContent='center' className='page'>
          <Cell width={10} left={2} className='box'>
            <Grid columns={10} gap='0' alignContent='space-between'>
              <Cell width={8} className='preview'>
                <h1>{file.name}</h1>
                <p className='file-info -small'>
                  {file.rows} rows ({fileSize(file.size)})
                </p>
                <br />
                <PreviewTable
                  preview={this.state.preview}
                  columnHighlights={this.getColumnHighlights()}
                />
              </Cell>
              <Cell width={2} className='location-columns'>
                Select the following<br />
                location columns:
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
                  <Button className='proceed'>Proceed</Button>
                )}
              </Cell>
            </Grid>
          </Cell>
        </Grid>
      </div>
    )
  }
}

export default styled(Preview)`
  &, .overlay {
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
  }
  .overlay {
    background: ${colors.indigo};
    opacity: 0.5;
    height: 100%;
    width: 100%;
  }
  .page {
    height: 100%;
    .box {
      background: ${colors.monochrome[0]};
    }
  }
  .preview, .location-columns {
    box-sizing: border-box;
  }
  .preview {
    padding: 40px 0 40px 30px;
  }
  h1 {
    color: ${colors.indigo};
  }
  .file-info {
    color: ${colors.monochrome[4]};
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
