import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Colors
import * as colors from '../colors'

// Images
import logo from '../images/logo.svg'
import logoLight from '../images/logo-light.svg'

// Elements
import {Button} from '../elements'

const Header = styled(props => (
  <Cell width={10} left={2} className={props.className}>
    <Grid columns={10} gap='15px' alignContent='center'>
      <Cell width={8} className='logo'>
        <img src={logo} />
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
    justify-content: space-between;
  }
  .links li a {
    text-decoration: none;
  }
`

const ToggleList = styled(props => (
  <div className={props.className}>
    <h3>{props.title}</h3>
    <ul>
      {props.items.map(item => (
        <ToggleListItem {...item} />
      ))}
    </ul>
  </div>
))`
  margin: 0 15px;
  h3 {
    font-size: 12px;
    font-weight: normal;
    color: ${colors.lightIndigo};
    line-height: 30px;
  }
  ul {
    list-style: none;
    padding: 0;
  }
  ul li:before {
    border-radius: ${props => ({square: '2px', circle: '50%'}[props.bullet])};
  }
`

const ToggleListItem = styled(props => (
  <li className={props.className}>{props.label}</li>
))`
  position: relative;
  padding-left: 20px;
  color: ${colors.monochrome[0]};
  line-height: 30px;
  &:before {
    display: block;
    content: ' ';
    position: absolute;
    width: 10px;
    height: 10px;
    box-sizing: border-box;
    background: ${props => props.toggled ? (props.color || colors.lightIndigo) : 'transparent'};
    border: 1px solid transparent;
    border-color: ${props => props.toggled ? 'transparent' : (props.color || colors.lightIndigo)};
    top: 10px;
    left: 2px;
  }
`

const Sidebar = styled(props => (
  <Cell width={2} className={props.className}>
    <div className='sidebar'>
      <Grid columns={1} rows='1fr min-content' height='100%'>
        <Cell>
          <div className='logo'>
            <img src={logoLight} />
          </div>
          <div className='tags'>
            <ToggleList
              title='Tags'
              bullet='square'
              items={[
                {toggled: true, color: colors.green, label: 'Found locations (15)'},
                {toggled: true, color: colors.yellow, label: 'Multiple matches (10)'},
                {toggled: false, color: colors.orange, label: 'No matches (8)'}
              ]}
            />
            <ToggleList
              title='Columns'
              bullet='circle'
              items={[
                {toggled: true, label: 'Branch_Name'},
                {toggled: true, label: 'Barangay'},
                {toggled: true, label: 'City'},
                {toggled: true, label: 'Province'},
                {toggled: false, label: 'Mobile_Number'},
                {toggled: false, label: 'Telephone_Number'},
                {toggled: false, label: 'Email_Address'},
                {toggled: false, label: 'Landmarks'}
              ]}
            />
          </div>
        </Cell>
        <Cell center>
          <Button>Proceed</Button>
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
  }
  .sidebar:before {
    display: block;
    content: ' ';
    background: ${colors.indigo};
    border-radius: 50%;
    width: 250%;
    padding-bottom: 250%;
    position: absolute;
    left: -75%;
    top: -60%;
  }
  .sidebar * {
    position: relative;
  }
  .logo {
    margin-bottom: 60px;
  }
  .logo img {
    width: 100%;
  }
`

class Page extends React.Component {
  isHeaderShown () {
    return ~[
      '/',
      '/:id/preview'
    ].lastIndexOf(this.props.match.path)
  }
  isSidebarShown () {
    return !this.isHeaderShown()
  }
  render () {
    return (
      <Grid
        columns={12}
        rows={this.isHeaderShown() ? '100px 1fr' : 1}
        gap='0'
        className={this.props.className}
      >
        {this.isHeaderShown() ? <Header /> : null}
        {this.isSidebarShown() ? <Sidebar /> : null}
        {this.props.children}
      </Grid>
    )
  }
}

export default styled(Page)`
  min-height: 100vh;
`
