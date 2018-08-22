import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

const Topbar = styled(({ className }) => (
  <div className={className}>
    This is alpha software! How can we make this tool better?
    <a href='https://airtable.com/shr7b1eauaxFWw1et' target='_blank'
      rel='noopener noreferrer'>
      Share your feedback!
    </a>
  </div>
))`
  background-color: ${colors.monochrome[2]};
  text-align: center;
  font-size: 12px;
  height: 30px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  z-index: 1;
  a {
    margin-left: 5px;
  }
`

export default Topbar
