import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Images
import logo from '../images/logo.svg'

const Header = styled(props => (
  <Cell width={10} left={2} className={props.className}>
    <Grid columns={10} gap='15px' alignContent='center'>
      <Cell width={9} className='logo'>
        <img src={logo} />
      </Cell>
      <Cell width={1}>
        <ul className='links -light'>
          <li><a href='#'>About</a></li>
        </ul>
      </Cell>
    </Grid>
  </Cell>
))`
  position: relative;
  padding-top: 20px;
  box-sizing: border-box;
  .logo img {
    height: 52px;
  }
  .links {
    padding: 0;
    list-style: none;
    display: flex;
    justify-content: flex-end;
  }
  .links li a {
    text-decoration: none;
  }
`

export default Header
