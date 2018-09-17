import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import {Link} from 'react-router-dom'
import chroma from 'chroma-js'

// Colors
import * as colors from '../colors'

const Sidebar = styled(props => (
  <Cell width={3} className={props.className}>
    <div className='sidebar'>
      <Grid columns={1} rows='1fr min-content' height='100%'>
        <Cell>
          <div className='logo'>
            <Link to='/'><img src='/static/images/logo-light.svg' alt='logo' /></Link>
          </div>
          <div className='tags'>
            {props.children}
          </div>
        </Cell>
        <Cell className='buttons' center>
          <Grid columns={2} rows='1fr min-content' height='100%'>
            <Cell>{props.backButton}</Cell>
            <Cell>{props.nextButton}</Cell>
          </Grid>
        </Cell>
      </Grid>
    </div>
  </Cell>
))`
  .sidebar {
    position: relative;
    background: ${colors.darkIndigo};
    padding: 15px;
    overflow: hidden;
    height: 100%;
    box-sizing: border-box;
    padding-right: 25px;
  }
  .sidebar:before {
    display: block;
    content: ' ';
    background: ${colors.indigo};
    border-radius: 50%;
    width: 40vw;
    height: 40vw;
    position: absolute;
    left: 50%;
    top: -32vw;
    transform: translateX(-50%);
  }
  .sidebar * {
    position: relative;
  }
  .logo {
    margin-bottom: 60px;
    text-align: center;
  }
  .logo img {
    width: 200px;
  }
  .steps {
    color: ${colors.monochrome[3]};
    font-size: 20px;
    line-height: 50px;
  }
  .steps .current {
    color: ${colors.monochrome[0]};
  }
  .steps .current .step-desc {
    font-size: 15px;
    line-height: 20px;
  }
  .buttons .btn {
    padding: 0 2.5em;
  }
  .buttons .btn.-back {
    background: ${colors.monochrome[2]};
    color: ${colors.monochrome[5]};
    &:hover {
      background: ${chroma(colors.monochrome[2]).brighten(0.5)};
    }
  }
`

export default Sidebar
