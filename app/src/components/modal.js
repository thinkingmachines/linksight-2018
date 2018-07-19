import React from 'react'
import ReactDOM from 'react-dom'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

class Modal extends React.Component {
  constructor (props) {
    super(props)
    this.el = document.createElement('div')
  }
  componentDidMount () {
    this.el.className = this.props.className
    window.modalRoot.appendChild(this.el)
  }
  componentWillUnmount () {
    this.el.className = null
    window.modalRoot.removeChild(this.el)
  }
  handleClose (e) {
    e.preventDefault()
    this.props.onClose()
  }
  render () {
    return ReactDOM.createPortal(
      <React.Fragment>
        <div
          className='modal-overlay'
          onClick={this.handleClose.bind(this)}
        />
        <div className='modal-box'>
          <a
            href='#close'
            className='close'
            onClick={this.handleClose.bind(this)}
          >
            &times;
          </a>
          {this.props.children}
        </div>
      </React.Fragment>,
      this.el
    )
  }
}

export default styled(Modal)`
  .modal-overlay {
    content: ' ';
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    width: 100%;
    background: ${colors.indigo};
    opacity: 0.5;
    pointer-events: auto;
  }
  .modal-box {
    position: relative;
    background: ${colors.monochrome[0]};
    max-width: 40em;
    box-sizing: border-box;
    padding: 30px;
    border-radius: 10px;
    pointer-events: auto;
  }
  .modal-box h1,
  .modal-box h2,
  .modal-box h3,
  .modal-box p {
    margin-bottom: 20px;
  }
  .modal-box h1,
  .modal-box h2,
  .modal-box h3 {
    color: ${colors.indigo};
  }
  .modal-box .close {
    font-size: 30px;
    line-height: 15px;
    position: absolute;
    top: 30px;
    right: 30px;
    color: ${colors.monochrome[3]};
    text-decoration: none;
  }
`
