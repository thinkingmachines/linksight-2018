import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Colors
import * as colors from '../colors'

// Images
import logoLight from '../images/logo-light.svg'

// Elements
import {
  Button,
  ToggleList
} from '../elements'

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

export default Sidebar
