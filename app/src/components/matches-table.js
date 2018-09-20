import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

// Components
import MatchItem from './match-item'

class MatchesTable extends React.Component {
  render () {
    return (
      <table cellSpacing='0' className={this.props.className}>
        <thead>
          <tr>
            <th colSpan='2' />
            <th>Original Locations</th>
            <th colSpan='4'>Candidate Matches</th>
            <th>Confidence Score</th>
          </tr>
        </thead>
        <tbody>
          {this.props.items.map((item, i) => (
            <MatchItem
              key={i}
              onChoose={this.props.onChoose}
              chosenItem={this.props.matchChoices[item.dataset_index]}
              item={item}
              index={i}
            />
          ))}
        </tbody>
      </table>
    )
  }
}

export default styled(MatchesTable)`
  width: 100%;
  thead {
    color: ${colors.monochrome[3]};
    font-size: 12px;
  }
  thead th {
    font-weight: normal;
    text-align: left;
    line-height: 40px;
    padding: 0 15px;
  }
  tr:hover .table-cell.-index,
  tr:hover .table-cell.-choice-content {
    box-shadow: inset 5px 0 0 0 ${colors.monochrome[2]};
  }
  tr.-choice > .table-cell {
    cursor: pointer;
  }
  .table-cell {
    padding: 15px 15px;
    box-sizing: border-box;
    background: ${colors.monochrome[0]};
    border-bottom: 1px solid ${colors.monochrome[2]};
    box-shadow: 0;
    transition: box-shadow 0.2s ease-in-out;
  }
`
