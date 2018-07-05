import React from 'react'
import styled from 'styled-components'
import {fileSize} from 'humanize-plus'

// Colors
import * as colors from '../colors'

const TableColumn = styled(props => (
  <div className={props.className + ' table-column'}>
    <div className='table-header table-cell'>
      {props.name}
    </div>
    {props.values.map((value, i) => (
      <div key={i} className='table-cell'>
        {value || ' '}
      </div>
    ))}
  </div>
))`
  margin: 0 2px;
  border: ${
  props => props.highlight
    ? '1px solid ' + props.highlight
    : '1px solid ' + colors.monochrome[2]};
  box-shadow: 0 0 0 1px ${props => props.highlight || 'transparent'};
  .table-column:first-child {
    margin-left: 0;
  }
  .table-column:last-child {
    margin-right: 0;
  }
  .table-cell {
    background: ${colors.monochrome[0]};
    box-sizing: border-box;
    white-space: pre;
    padding: 10px 15px;
    border-bottom: 1px solid ${colors.monochrome[2]};
  }
  .table-cell:last-child {
    border-bottom: 0;
  }
  .table-header {
    background: ${colors.monochrome[1]};
    box-shadow: inset 0 4px 0 0 ${props => props.highlight || 'transparent'};
  }
`

class PreviewTable extends React.Component {
  getFields () {
    const {fields} = this.props.preview.schema
    return fields.filter(field => field.name !== 'index')
  }
  getHighlight (column) {
    const columnHighlights = this.props.columnHighlights || {}
    return columnHighlights[column]
  }
  render () {
    const {file} = this.props.preview
    const data = {}
    const fields = this.getFields()
    this.props.preview.data.forEach(row => {
      fields.forEach(field => {
        if (!data[field.name]) {
          data[field.name] = []
        }
        data[field.name].push(row[field.name])
      })
    })
    return (
      <div className={this.props.className}>
        <h1>{file.name}</h1>
        <p className='file-info -small'>
          {file.rows} rows ({fileSize(file.size)})
        </p>
        <br />
        <div className='table'>
          {fields.map((field, i) => (
            <TableColumn
              key={i}
              name={field.name}
              values={data[field.name]}
              highlight={this.getHighlight(field.name)}
            />
          ))}
        </div>
      </div>
    )
  }
}

export default styled(PreviewTable)`
  h1 {
    color: ${colors.indigo};
  }
  .file-info {
    color: ${colors.monochrome[4]};
  }
  .table {
    display: flex;
    overflow-x: scroll;
    padding-bottom: 1px;
  }
`
