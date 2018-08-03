import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

const Topbar = styled(({ className }) => (
  <div className={className}>
    <span>
      This is alpha software! How can we make this tool better?
    </span> <a href='https://airtable.com/shr7b1eauaxFWw1et'>
      Share your feedback!
    </a>
  </div>
))`
  background-color: ${colors.monochrome[2]};
  padding: 10px;
  text-align: center;
`

export default Topbar
