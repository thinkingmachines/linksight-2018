import React from 'react'
import styled from 'styled-components'

// Colors
import * as colors from '../colors'

const Choice = styled(props => (
  <tr className={'-choice ' + props.className}>
    <td colSpan='1' />
    <td
      colSpan='5'
      className='table-cell -choice-content'
      onClick={props.onChoose.bind(null, props.item)}
    >
      {props.noChoice ? 'No correct match' : [
        props.item.matched_barangay,
        props.item.matched_city_municipality,
        props.item.matched_province
      ].filter(v => v).join(', ')}
      {props.noChoice ? null : (
        <div className='score'>
          {parseFloat(props.item.total_score).toFixed(2)}
        </div>
      )}
    </td>
  </tr>
))`
  .table-cell.-choice-content {
    position: relative;
    padding-left: 40px;
  }
  .table-cell.-choice-content:before {
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
  .table-cell .score {
    font-size: 12px;
    color: ${colors.monochrome[3]};
  }
`

class MatchItem extends React.Component {
  render () {
    const {item} = this.props
    const tag = this.props.chosenItem
      ? 'checked'
      : {
        'True': 'identified',
        'False': 'multiple'
      }[item.matched]
    const icon = {
      'identified': require('../images/tags/identified.svg'),
      'multiple': require('../images/tags/multiple.svg'),
      'checked': require('../images/tags/identified.svg')
    }[tag]
    return (
      <React.Fragment>
        <tr className={this.props.className}>
          <td className='table-cell -index'>{item.dataset_index + 1}</td>
          <td className='table-cell -tag'>
            <span className={'tag tag-' + tag}>
              <img src={icon} alt={tag} />
            </span>
          </td>
          <td className='table-cell'>
            {item.source_barangay ? item.source_barangay : (
              <span className='missing'>{item.matched_barangay}</span>
            )}
          </td>
          <td className='table-cell'>
            {item.source_city_municipality ? item.source_city_municipality : (
              <span className='missing'>{item.matched_city_municipality}</span>
            )}
          </td>
          <td className='table-cell'>
            {item.source_province ? item.source_province : (
              <span className='missing'>{item.matched_province}</span>
            )}
          </td>
        </tr>
        {item.matched === 'True' ? null : this.renderChoices(item.choices)}
        {item.matched === 'True' ? null : this.renderNoChoice(item)}
      </React.Fragment>
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
  renderNoChoice (item) {
    return (
      <Choice noChoice='true'
        /*
          Based on how chosenItem works, the passed item needs to have:
            - no id
            - a dataset_index
        */
        item={{dataset_index: item.dataset_index}}
        onChoose={this.props.onChoose}
        chosenItem={this.props.chosenItem} />
    )
  }
}

export default styled(MatchItem)`
  .table-cell.-index {
    font-size: 12px;
    color: ${colors.monochrome[3]};
    padding: 15px;
    width: 1px;
  }
  .table-cell.-tag {
    width: 1px;
  }
  .table-cell.-tag .tag {
    display: inline-block;
    color: white;
    font-size: 12px;
    line-height: 20px;
    border-radius: 5px;
    text-align: center;
    width: 20px;
    margin: 0 15px 0 5px;
  }
  .tag img {
    width: 12px;
    height: 12px;
  }
  .tag-identified {
    background: ${colors.green};
  }
  .tag-multiple {
    background: ${colors.orange};
  }
  .tag-checked {
    background: ${colors.yellow};
  }
  .table-cell .missing {
    font-style: italic;
    color: ${colors.monochrome[3]};
  }
`
