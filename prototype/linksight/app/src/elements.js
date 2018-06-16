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
  padding: 0 1em;
  line-height: 3;
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
    background-color: ${colors.yellow};
  }
  .react-toggle-track {
    background-color: ${colors.monochrome[4]};
  }
  &:hover:not(.react-toggle--disabled) .react-toggle-track {
    background-color: ${colors.monochrome[4]} !important;
  }
  &.react-toggle--focus .react-toggle-thumb,
  &:active:not(.react-toggle--disabled) .react-toggle-thumb {
    box-shadow: none;
  }
  &.react-toggle--checked .react-toggle-thumb {
    border-color: ${colors.yellow};
  }
`
