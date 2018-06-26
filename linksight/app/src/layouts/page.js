import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Images
import logo from '../images/linksight-logo.png'

const Header = styled(props => (
  <Grid columns={12} gap='15px' className={props.className}>
    <Cell width={10} left={2}>
      <Grid columns={10} gap='15px' alignContent='center'>
        <Cell width={8}>
          <div className='logo'>
            <img src={logo} />
          </div>
        </Cell>
        <Cell width={2}>
          <ul className='links -light'>
            <li><a href='#'>Datasets</a></li>
            <li><a href='#'>About</a></li>
            <li><a href='#'>Contact</a></li>
          </ul>
        </Cell>
      </Grid>
    </Cell>
  </Grid>
))`
  position: relative;
  padding: 20px 0 100px;
  .logo img {
    height: 52px;
  }
  .links {
    padding: 0;
    list-style: none;
    display: flex;
    justify-content: space-between;
  }
  .links li a {
    text-decoration: none;
  }
`

class Page extends React.Component {
  isHeaderShown () {
    return true
  }
  isSidebarShown () {
  }
  render () {
    return (
      <React.Fragment>
        {this.isHeaderShown() && <Header />}
        {this.isSidebarShown() && null}
        {this.props.children}
      </React.Fragment>
    )
  }
}

export default styled(Page)`
`
