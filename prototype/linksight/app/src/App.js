import React from 'react'
import {Route, Switch} from 'react-router-dom'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Stylesheets
import './css/app.css'
import './css/typography.css'
import './css/react-toggle.css'
import 'filepond/dist/filepond.min.css'

// Images
import logo from './images/linksight-logo.png'

// Colors
import * as colors from './colors'

// Pages
import Upload from './upload'
import Preview from './preview'

class App extends React.Component {
  render () {
    return (
      <div className={this.props.className}>
        <Grid columns={12} gap='15px' className='header'>
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
        <Switch>
          <Route exact path='/' component={Upload} />
          <Route exact path='/:id/preview' component={Preview} />
        </Switch>
      </div>
    )
  }
}

export default styled(App)`
  background: ${colors.indigo};
  height: 100%;
  &:before {
    content: ' ';
    width: 100%;
    padding-bottom: 100%;
    display: block;
    background: ${colors.monochrome[0]};
    border-radius: 50%;
    position: absolute;
    top: -25%;
    left: -55%;
  }
  .header, .page {
    position: relative;
  }
  .header {
    padding: 20px 0 100px;
  }
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
