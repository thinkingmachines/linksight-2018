import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

// Images
import logoIcon from '../images/logo-icon.svg'

function generateKeyframes () {
  let keyframes = ''
  let r = 0
  for (let i = 0; i < 100; i += 10) {
    let s = Math.random() * 0.2 + 0.8
    let y = Math.random() * 10 + 25
    let x = (Math.random() > 0.5 ? -1 : 1) * (Math.random() * 10 + 10)
    r += (Math.random() > 0.5 ? -1 : 1) * (Math.random() * 180 + 180)
    keyframes += `
      ${i}% {
        transform: scale(${s}) translate(${x}%, ${y}%) rotate(${r}deg);
      }
    `
  }
  return keyframes
}

const LoadingOverlay = styled((props) => (
  <div className={props.className}>
    <img src={logoIcon} alt='Loading icon' />
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
  background: rgba(255, 255, 255, 0.9);
  color: ${colors.indigo};
  @keyframes random {
    ${props => generateKeyframes()}
  }
  img {
    width: 60px;
    height: 60px;
    animation: 10s random alternate infinite;
  }
`

export default LoadingOverlay
