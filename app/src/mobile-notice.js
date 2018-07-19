import React from 'react'
import styled from 'styled-components'

// Images
import laptop from './images/laptop.svg'

// Colors
import * as colors from './colors'

// Fragments
import About from './fragments/about'

class MobileNotice extends React.Component {
  render () {
    return (
      <div className={this.props.className}>
        <div className='notice'>
          <p><img src={laptop} /></p>
          <p>To use this tool, switch to a desktop device.</p>
        </div>
        <div className='about'>
          <About />
        </div>
      </div>
    )
  }
}

export default styled(MobileNotice)`
  padding: 15px;
  &, a {
    color: ${colors.monochrome[0]};
  }
  .notice {
    background: ${colors.monochrome[1]};
    color: ${colors.indigo};
    border-radius: 10px;
    padding: 30px;
    text-align: center;
    box-sizing: border-box;
    margin-bottom: 30px;
  }
  .notice img {
    width: 50%;
  }
  .about h1, .about p {
    margin-bottom: 20px;
  }
`
