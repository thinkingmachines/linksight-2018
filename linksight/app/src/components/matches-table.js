import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Colors
import * as colors from '../colors'

class MatchItem extends React.Component {
  render () {
    let tag = {
      'True': 'Found',
      'False': 'Multiple'
    }[this.props.matched]
    return (
      <React.Fragment>
        <Cell middle className='table-cell -index'>{this.props.dataset_index + 1}</Cell>
        <Cell middle className='table-cell'>
          <span className={'tag tag-' + tag}>
            {tag}
          </span>
        </Cell>
        <Cell middle className='table-cell'>{this.props.source_barangay}</Cell>
        <Cell middle className='table-cell'>{this.props.source_city_municipality}</Cell>
        <Cell middle className='table-cell'>{this.props.source_province}</Cell>
        {this.props.matched === 'True' ? null : this.renderChoices(this.props.choices)}
      </React.Fragment>
    )
  }
  renderChoices (choices) {
    return choices.map((choice, i) => (
      <React.Fragment key={i}>
        <Cell middle left={2} className='table-cell -score'>
          {parseFloat(choice.total_score / 4 * 100).toFixed(2)}
        </Cell>
        <Cell middle width={3} className='table-cell -choice'>
          {[
            choice.matched_barangay,
            choice.matched_city_municipality,
            choice.matched_province
          ].filter(v => v).join(', ')}
        </Cell>
      </React.Fragment>
    ))
  }
}

class MatchesTable extends React.Component {
  render () {
    const columns = `max-content 80px repeat(3, 1fr)`
    return (
      <Grid columns={columns} gap='0' className={this.props.className}>
        <Cell left={3} className='table-header'>Barangay</Cell>
        <Cell className='table-header'>City/Municipality</Cell>
        <Cell className='table-header'>Province</Cell>
        {this.props.items.map((item, i) => (
          <MatchItem key={i} {...item} />
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
  .table-cell {
    background: ${colors.monochrome[0]};
    padding: 15px 0;
    box-sizing: border-box;
    border-bottom: 1px solid ${colors.monochrome[2]};
  }
  .table-cell.-index {
    font-size: 12px;
    color: ${colors.monochrome[3]};
    padding: 15px;
  }
  .table-cell .tag {
    display: inline-block;
    color: white;
    font-size: 12px;
    line-height: 20px;
    border-radius: 5px;
    text-align: center;
    margin-right: 15px;
    cursor: pointer;
  }
  .tag-Found {
    background: ${colors.green};
  }
  .tag-Multiple {
    background: ${colors.yellow};
  }
  .tag-None {
    background: ${colors.orange};
  }
  .table-cell.-score {
    font-size: 12px;
    text-align: right;
    padding-right: 15px;
    position: relative;
    color: ${colors.monochrome[3]};
  }
  .table-cell.-score:before {
    display: block;
    content: ' ';
    width: 10px;
    height: 10px;
    box-sizing: border-box;
    border-radius: 50%;
    border: 1px solid ${colors.monochrome[2]};
    position: absolute;
    left: 15px;
    top: 20px;
  }
  .tablce-cell.-score.-chosen:before {
    border-color: ${colors.green};
    background: ${colors.green};
  }
`
