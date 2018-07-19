import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Colors
import * as colors from '../colors'

// Components
import MatchItem from './match-item'

class MatchesTable extends React.Component {
  render () {
    const columns = `max-content 40px repeat(3, 1fr)`
    return (
      <Grid columns={columns} gap='0' className={this.props.className}>
        <Cell left={3} className='table-header'>Barangay</Cell>
        <Cell className='table-header'>City/Municipality</Cell>
        <Cell className='table-header'>Province</Cell>
        {this.props.items.map((item, i) => (
          <MatchItem
            key={i}
            onChoose={this.props.onChoose}
            chosenItem={this.props.matchChoices[item.dataset_index]}
            item={item}
          />
        ))}
      </Grid>
    )
  }
}

export default styled(MatchesTable)`
  .table-header {
    color: ${colors.monochrome[3]};
    font-size: 12px;
  }
  .table-row {
    display: contents;
  }
  .table-row:hover > .table-cell:first-child {
    box-shadow: inset 5px 0 0 0 ${colors.monochrome[2]};
  }
  .table-row.-choice > .table-cell {
    cursor: pointer;
  }
`
