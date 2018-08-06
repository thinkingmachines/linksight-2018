import React from 'react'
import styled from 'styled-components'
import Select from 'react-select'

// Colors
import * as colors from '../colors'

class LocationColumn extends React.Component {
  getSelectStyles () {
    return {
      control: (base, state) => ({
        ...base,
        borderWidth: 0,
        borderRadius: 0,
        boxShadow: 0
      }),
      valueContainer: (base, style) => ({
        ...base,
        padding: '0 15px'
      }),
      option: (base, style) => ({
        ...base,
        padding: '10px 15px'
      }),
      menu: (base, style) => ({
        ...base,
        borderRadius: 0,
        marginTop: 2
      }),
      menuList: (base, style) => ({
        ...base,
        paddingTop: 0,
        paddingBottom: 0,
        maxHeight: '180px'
      }),
      singleValue: (base, style) => ({
        ...base,
        marginLeft: 0,
        marginRight: 2
      }),
      input: (base, style) => ({
        ...base,
        margin: 0
      }),
      placeholder: (base, style) => ({
        ...base,
        marginLeft: 0,
        marginRight: 0
      })
    }
  }
  handleChange (option) {
    this.props.onChange && this.props.onChange(option ? option.value : null)
  }
  render () {
    return (
      <div className={this.props.className}>
        <div className='name'>{this.props.name}</div>
        <div className='selected'>
          <Select
            options={this.props.columnOptions}
            placeholder='Select a column'
            styles={this.getSelectStyles()}
            onChange={this.handleChange.bind(this)}
            isClearable
          />
        </div>
      </div>
    )
  }
}

export default styled(LocationColumn)`
  border: 1px solid ${props => props.color};
  .name {
    color: ${colors.monochrome[0]};
    background: ${props => props.color};
  }
  .name {
    padding: 10px 15px;
  }
`
