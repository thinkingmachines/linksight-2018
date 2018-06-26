import styled from 'styled-components'
import ReactToggle from 'react-toggle'

import * as colors from './colors'

export const Title = styled.h1`
  font-size: 52px;
  line-height: 60px;
`

export const Button = styled.button`
  border: 0;
  background: ${colors.yellow};
  color: ${colors.monochrome[0]};
  padding: 0 1em;
  line-height: 35px;
  border-radius: 10px;
  &:hover {
    background: ${colors.yellow};
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
