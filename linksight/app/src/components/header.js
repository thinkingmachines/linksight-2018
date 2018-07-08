import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Images
import logo from '../images/logo.svg'

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
            <h1>LinkSight</h1>
            <p>Many Philippine NGOs and grassroots organizations collect, encode, analyze and derive insights from their data. However, this process is usually done manually and the data they get is only limited to what they can physically gather.</p>
            <p>They want to learn more about their communities so they more effectively target their programs and projects. Unfortunately, Philippine Census statistics are often hard to find and hard to use.</p>
            <p>LinkSight will be a repository of ready-to-use Philippine geospatial data and socioeconomic indicators that anyone can merge with their own location datasets to expand their data point of view.</p>
            <p>If you're interested in contributing or learning more about the project, you can contact us at <a href='mailto:linksight@thinkingmachin.es'>linksight@thinkingmachin.es</a></p>
          </Modal>
        ) : null}
        <Grid columns={10} gap='15px' alignContent='center'>
          <Cell width={9} className='logo'>
            <img src={logo} />
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
