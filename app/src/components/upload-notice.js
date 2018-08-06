import React from 'react'
import styled from 'styled-components'

import * as colors from '../colors'

import {Button} from '../elements'

class UploadNotice extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      hasAgreed: false
    }
  }
  hideNotice (e) {
    e.preventDefault()
    this.setState({hasAgreed: true})
  }
  render () {
    return (
      <div className={this.props.className}>
        {this.state.hasAgreed ? null : (
          <div className='notice'>
            <h3>Before you upload your data:</h3>
            <p><small>
              LinkSight needs to temporarily save a copy of your data to process it.<br />
              The copy will be deleted from our system within 24 hours of upload.
            </small></p>
            <p>
              <Button onClick={this.hideNotice.bind(this)}>
                I understand and agree
              </Button>
            </p>
          </div>
        )}
        {this.props.children}
      </div>
    )
  }
}

export default styled(UploadNotice)`
  position: relative;
  .notice {
    background: ${colors.monochrome[1]};
    border-radius: 7.5px;
    position: absolute;
    z-index: 1;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }
  p {
    margin-bottom: 20px;
  }
  p:last-child {
    margin-bottom: 0;
  }
`
