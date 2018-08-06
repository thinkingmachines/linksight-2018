import styled from 'styled-components'
import ReactToggle from 'react-toggle'
import chroma from 'chroma-js'

// Colors
import * as colors from './colors'

export const Title = styled.h1`
  font-size: 40px;
  line-height: 46px;
`

export const Button = styled.button`
  border: 0;
  background: ${colors.yellow};
  color: ${colors.monochrome[0]};
  padding: 0 1em;
  line-height: 35px;
  border-radius: 10px;
  &:hover {
    background: ${chroma(colors.yellow).brighten(0.5)};
  }
`

export const PrimaryButton = Button.extend`
  background: ${colors.purple};
`

export const Toggle = styled(ReactToggle)`
  .react-toggle-thumb {
    border-color: ${colors.monochrome[3]};
  }
  &.react-toggle--checked .react-toggle-track,
  &.react-toggle--checked:hover:not(.react-toggle--disabled) .react-toggle-track {
    background-color: ${colors.yellow} !important;
  }
  .react-toggle-track {
    background-color: ${colors.monochrome[3]};
  }
  &:hover:not(.react-toggle--disabled) > .react-toggle-track {
    background-color: ${colors.monochrome[4]} !important;
  }
  &.react-toggle--focus .react-toggle-thumb,
  &:active:not(.react-toggle--disabled) .react-toggle-thumb {
    box-shadow: none !important;
  }
  &.react-toggle--checked .react-toggle-thumb {
    border-color: ${colors.yellow};
  }
`

export const Instruction = styled.div`
  position: relative;
  @keyframes pulse {
    from {
      transform: scale(1);
    }
    to {
      transform: scale(1.5);
    }
  }
  &:before {
    content: ' ';
    display: block;
    border: .2em solid ${colors.yellow};
    border-radius: 50%;
    width: .4em;
    height: .4em;
    position: absolute;
    top: .27em;
    left: -1.33em;
    animation: pulse 0.5s infinite alternate;
  }
`
