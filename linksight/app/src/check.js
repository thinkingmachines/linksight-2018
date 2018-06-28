import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Colors
import * as colors from './colors'

// Layouts
import Page from './layouts/page'

// Components
import MatchesTable from './components/matches-table'

class Check extends React.Component {
  render () {
    return (
      <Page match={this.props.match}>
        <Cell width={10} className={this.props.className}>
          <Grid columns={1} rows='40% 60%' gap='0' height='100%'>
            <Cell className='map'>
              <iframe
                src='https://www.google.com/maps/embed/v1/place?q=place_id:ChIJr5Qp-vPIlzMRCuRgR6-IyYk&key=AIzaSyCIXyqG6o62e9kcnpLR_3Pz317ybfDWLiw'
                width='100%'
                height='100%'
                frameborder='0'
                allowfullscreen
              />
            </Cell>
            <Cell className='matches' >
              <MatchesTable
                headers={[
                  'Branch_Name',
                  'Barangay',
                  'City',
                  'Province'
                ]}
                rows={[
                  [1, 'Found', 'FamilyDOC Buhay Na Tubig', 'Brgy. Buhay Na Tubig', 'Imus', 'Cavite'],
                  [2, 'Multiple', 'FamilyDOC Buhay Na Tubig', 'Brgy. Buhay Na Tubig', 'Imus', 'Cavite'],
                  [3, 'None', 'FamilyDOC Buhay Na Tubig', 'Brgy. Buhay Na Tubig', 'Imus', 'Cavite'],
                  [4, 'Found', 'FamilyDOC Buhay Na Tubig', 'Brgy. Buhay Na Tubig', 'Imus', 'Cavite'],
                  [5, 'Multiple', 'FamilyDOC Marcos Alvarez', 'Brgy. Talon V', 'Las Pinas', null]
                ]}
              />
            </Cell>
          </Grid>
        </Cell>
      </Page>
    )
  }
}

export default styled(Check)`
  position: relative;
  .map {
    background: #e5e3e0;  // color from Google Maps
  }
  .matches {
    background: ${colors.monochrome[1]};
    padding: 30px;
    box-sizing: border-box;
    overflow-y: auto;
  }
`
