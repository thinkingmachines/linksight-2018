import React from 'react'
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

export const ToggleList = styled(props => (
  <div className={props.className}>
    <h3>{props.title}</h3>
    <ul>
      {props.items.map((item, i) => (
        <ToggleListItem key={i} {...item} />
      ))}
    </ul>
  </div>
))`
  margin: 0 15px;
  h3 {
    font-size: 12px;
    font-weight: normal;
    color: ${colors.lightIndigo};
    line-height: 30px;
  }
  ul {
    list-style: none;
    padding: 0;
    margin: 0 0 30px;
  }
  ul li:before {
    border-radius: ${props => ({square: '2px', circle: '50%'}[props.bullet])};
  }
`

export const ToggleListItem = styled(props => (
  <li className={props.className}>{props.label}</li>
))`
  position: relative;
  padding-left: 20px;
  color: ${colors.monochrome[0]};
  line-height: 30px;
  &:before {
    display: block;
    content: ' ';
    position: absolute;
    width: 10px;
    height: 10px;
    box-sizing: border-box;
    background: ${props => props.toggled ? (props.color || colors.lightIndigo) : 'transparent'};
    border: 1px solid transparent;
    border-color: ${props => props.toggled ? 'transparent' : (props.color || colors.lightIndigo)};
    top: 10px;
    left: 2px;
  }
`
