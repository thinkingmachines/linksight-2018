import styled from 'styled-components'
import ReactToggle from 'react-toggle'

export const Title = styled.h1`
  font-size: 52px;
  line-height: 60px;
`

export const Button = styled.button`
  border: 0;
  background: white;
  padding: 0 1em;
  line-height: 3;
  &:hover {
    background: magenta;
  }
`

export const PrimaryButton = Button.extend`
  background: pink;
`

export const Toggle = styled(ReactToggle)`
  .react-toggle-thumb {
    border-color: #b4b4b4;
  }
  &.react-toggle--checked .react-toggle-track,
  &.react-toggle--checked:hover:not(.react-toggle--disabled) .react-toggle-track {
    background-color: pink;
  }
  .react-toggle-track,
  &:hover:not(.react-toggle--disabled) .react-toggle-track {
    background-color: #b4b4b4;
  }
  &.react-toggle--focus .react-toggle-thumb,
  &:active:not(.react-toggle--disabled) .react-toggle-thumb {
    box-shadow: none;
  }
`
