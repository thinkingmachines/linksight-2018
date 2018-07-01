import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

// Images
import logoIcon from '../images/logo-icon.svg'

class LoadingOverlay extends React.Component {
  render () {
    return (
      <div className={this.props.className}>
        <img src={logoIcon} />
        <br />
        {this.props.children}
      </div>
    )
  }
}

export default styled(LoadingOverlay)`
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.9);
  color: ${colors.indigo};
  @keyframes rotate {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  img {
    width: 60px;
    height: 60px;
    animation: 1s rotate infinite;
  }
`
