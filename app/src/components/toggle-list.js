import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

const ToggleListItem = styled(props => (
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

export default styled(props => (
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
    max-height: 200px;
    overflow-y: auto;
  }
  ul li:before {
    border-radius: ${props => ({square: '2px', circle: '50%'}[props.bullet])};
  }
`
