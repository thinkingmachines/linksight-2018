import React from 'react'
import styled from 'styled-components'

import * as colors from '../colors'

import {
  Toggle
} from '../elements'

class DatasetCard extends React.Component {
  render () {
    return <div className={this.props.className}>
      <div className='icon'>
        <img src={this.props.iconUrl} />
      </div>
      <div className='info'>
        <h3 className='name'>{this.props.name}</h3>
        <p className='description -small'>{this.props.description}</p>
        <div className='actions -small'>
          <a href='#'>About</a>
          <span className='bull'>&bull;</span>
          <a href='#'>Preview</a>
          <span className='bull'>&bull;</span>
          <a href='#'>Download</a>
        </div>
      </div>
      <div className='toggle'>
        <Toggle icons={false} />
      </div>
    </div>
  }
}

export default styled(DatasetCard)`
  display: flex;
  background: ${colors.monochrome[0]};
  align-items: center;
  height: 80px;
  .info {
    flex: 1;
  }
  .icon, .toggle {
    flex: none;
  }
  .icon, .icon img {
    width: 80px;
    height: 80px;
  }
  .info, .toggle {
    padding: 0 20px;
  }
  .actions a {
    color: ${colors.monochrome[3]};
    text-decoration: none;
  }
  .bull {
    color: ${colors.monochrome[3]};
    font-size: 24px;
    margin: 0 5px;
    vertical-align: -2px;
  }
`
