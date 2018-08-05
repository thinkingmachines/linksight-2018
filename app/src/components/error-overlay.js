import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

// Images
import logoIcon from '../images/logo-icon.svg'

const ErrorOverlay = styled((props) => (
  <div className={props.className}>
    <img src={logoIcon} alt='Error icon' />
    <br />
    {props.children}
  </div>
))`
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
  text-align: center;
  background: rgba(255, 255, 255, 0.9);
  color: ${colors.indigo};
  img {
    width: 60px;
    height: 60px;
    transform: rotate(45deg);
  }
`

export default ErrorOverlay
