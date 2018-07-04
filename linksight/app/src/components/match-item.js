import React from 'react'
import styled from 'styled-components'
import {Cell} from 'styled-css-grid'

// Colors
import * as colors from '../colors'

const Choice = styled(props => (
  <section className={'table-row -choice ' + props.className}>
    <Cell middle left={2} className='table-cell -score'>
      {parseFloat(props.item.total_score / 6 * 100).toFixed(2)}
    </Cell>
    <Cell
      middle
      width={3}
      className='table-cell'
      onClick={props.onChoose.bind(null, props.item)}
    >
      {[
        props.item.matched_barangay,
        props.item.matched_city_municipality,
        props.item.matched_province
      ].filter(v => v).join(', ')}
    </Cell>
  </section>
))`
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
    transition: border-color, background 0.2s ease-in-out;
    ${props => props.item.id === props.chosenItem ? `
      border-color: ${colors.green};
      background: ${colors.green};
    ` : null}
  }
`

class MatchItem extends React.Component {
  render () {
    const {item} = this.props
    const tag = {
      'True': 'Found',
      'False': 'Multiple'
    }[item.matched]
    return (
      <section className={'table-row ' + this.props.className}>
        <Cell middle className='table-cell -index'>{item.dataset_index + 1}</Cell>
        <Cell middle className='table-cell'>
          <span className={'tag tag-' + tag}>
            {tag}
          </span>
        </Cell>
        <Cell middle className='table-cell'>{item.source_barangay}</Cell>
        <Cell middle className='table-cell'>{item.source_city_municipality}</Cell>
        <Cell middle className='table-cell'>{item.source_province}</Cell>
        {item.matched === 'True' ? null : this.renderChoices(item.choices)}
      </section>
    )
  }
  renderChoices (choices) {
    return choices.map((item, i) => (
      <Choice
        key={i}
        item={item}
        onChoose={this.props.onChoose}
        chosenItem={this.props.chosenItem}
      />
    ))
  }
}

export default styled(MatchItem)`
  .table-cell {
    padding: 15px 0;
    box-sizing: border-box;
    background: ${colors.monochrome[0]};
    border-bottom: 1px solid ${colors.monochrome[2]};
    box-shadow: 0;
    transition: box-shadow 0.2s ease-in-out;
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
`
