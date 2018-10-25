import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

// Elements
import {Button} from '../elements'

// API
import api from '../api'

class RequestToken extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      isToggled: false,
      token: null
    }
  }
  toggle (e) {
    e.preventDefault()
    this.setState({isToggled: !this.state.isToggled})
  }
  generateToken (e) {
    e.preventDefault()
    api.post('users/me/tokens')
      .then(resp => {
        this.setState({token: resp.data.key})
      })
  }
  render () {
    return (
      <div className={this.props.className}>
        <div className='toggle' onClick={this.toggle.bind(this)}>
          {'\u{1F6E0}\u{FE0F}'} Need API access?
        </div>
        {this.state.isToggled ? (
          <div className='token'>
            {this.state.token ? (
              <p>
                <input readOnly
                  type='text'
                  value={this.state.token}
                  onClick={e => e.target.select()}
                />
              </p>
            ) : null}
            <p>
              <Button onClick={this.generateToken.bind(this)}>Generate token</Button>
              {'\u{1F4D6}'} <a href='/docs'>API Documentation</a>
            </p>
          </div>
        ) : null}
      </div>
    )
  }
}

export default styled(RequestToken)`
  position: fixed;
  top: 0;
  right: 0;
  z-index: 2;
  font-size: 12px;
  line-height: 30px;
  .toggle {
    cursor: pointer;
    text-align: right;
    padding-right: 15px;
  }
  .token {
    border: 1px solid ${colors.monochrome[2]};
    border-top: 0;
    background: ${colors.monochrome[1]};
    padding: 10px 15px;
  }
  .token p {
    padding-bottom: 5px;
  }
  .token input {
    width: 100%;
  }
  .token button {
    margin-right: 15px;
  }
`
