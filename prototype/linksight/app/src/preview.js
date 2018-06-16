import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import axios from 'axios'
import {fileSize} from 'humanize-plus'

// Colors
import * as colors from './colors'

class Preview extends React.Component {
  constructor (props) {
    super(props)
    this.state = {preview: null}
  }
  componentDidMount () {
    let {id} = this.props.match.params
    axios.get(`http://localhost:8000/api/datasets/${id}/preview`)
      .then(resp => {
        this.setState({preview: resp.data})
      })
  }
  renderTable () {
    const {fields} = this.state.preview.schema
    const data = {}
    this.state.preview.data.forEach(row => {
      fields.forEach(field => {
        if (!data[field.name]) {
          data[field.name] = []
        }
        data[field.name].push(row[field.name])
      })
    })
    return (
      <div className='table'>
        {fields.filter(field => field.name !== 'index').map((field, i) => (
          <div key={i} className='table-column'>
            <div className='table-header table-cell'>
              {field.name}
            </div>
            {data[field.name].map((value, i) => (
              <div key={i} className='table-cell'>
                {value || ' '}
              </div>
            ))}
          </div>
        ))}
      </div>
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
        <Grid columns={12} gap='0' alignContent='center' className='modal'>
          <Cell width={10} left={2} className='box'>
            <Grid columns={10} gap='0' alignContent='stretch'>
              <Cell width={7} className='preview'>
                <h1>{file.name}</h1>
                <p className='file-info -small'>
                  {file.rows} rows ({fileSize(file.size)})
                </p>
                <br />
                {this.renderTable()}
              </Cell>
              <Cell width={3} className='location-columns'>
                Columns
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
  .modal {
    position: relative;
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
  .table {
    display: flex;
    overflow: auto;
  }
  .table-column {
    border: 1px solid ${colors.monochrome[2]};
    margin: 0 2px;
  }
  .table-column:first-child {
    margin-left: 0;
  }
  .table-column:last-child {
    margin-right: 0;
  }
  .table-header {
    background: ${colors.monochrome[1]};
  }
  .table-cell {
    box-sizing: border-box;
    white-space: pre;
    padding: 10px 15px;
    border-bottom: 1px solid ${colors.monochrome[2]};
  }
  .table-cell:last-child {
    border-bottom: 0;
  }
  .location-columns {
    padding: 40px 30px;
    background: ${colors.monochrome[1]};
    border-left: 1px solid ${colors.monochrome[2]};
  }
`
