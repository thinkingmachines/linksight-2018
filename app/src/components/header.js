import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Fragments
import About from '../fragments/about'

// Components
import Modal from './modal'

class Header extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      isAboutShown: false
    }
  }
  toggleAbout (isAboutShown, e) {
    if (e) {
      e.preventDefault()
    }
    this.setState({isAboutShown})
  }
  render () {
    return (
      <Cell width={10} left={2} className={this.props.className}>
        {this.state.isAboutShown ? (
          <Modal onClose={this.toggleAbout.bind(this, false)}>
            <About />
          </Modal>
        ) : null}
        <Grid columns={10} gap='15px' alignContent='center'>
          <Cell width={9} className='logo'>
            <img src='/static/images/logo.svg' alt='logo' />
          </Cell>
          <Cell width={1}>
            <ul className='links -light'>
              <li>
                <a
                  href='#about'
                  onClick={this.toggleAbout.bind(this, true)}
                >
                  About
                </a>
              </li>
            </ul>
          </Cell>
        </Grid>
      </Cell>
    )
  }
}

export default styled(Header)`
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
