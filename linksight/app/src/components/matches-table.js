import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

// Colors
import * as colors from '../colors'

class MatchesTable extends React.Component {
  render () {
    const columns = `max-content 80px repeat(${this.props.headers.length}, 1fr)`
    return (
      <Grid columns={columns} gap='0' className={this.props.className}>
        {this.props.headers.map((header, i) => (
          <Cell left={i === 0 ? 3 : null} className='table-header'>
            {header}
          </Cell>
        ))}

        {this.props.rows.map(([index, tag, ...values]) => {
          return (
            <React.Fragment>
              <Cell middle className='table-cell -index'>{index}</Cell>
              <Cell middle className='table-cell'>
                <span className={'tag tag-' + tag}>{tag}</span>
              </Cell>
              {values.map(value => (
                <Cell middle className='table-cell'>{value}</Cell>
              ))}
            </React.Fragment>
          )
        })}

        <Cell width={2} className='table-inset' />
        <Cell width={this.props.headers.length} className='table-inset'>
          <div className='choices'>
            <div className='choice -selected'>Talon Singko, City of Las Pinas, Metro Manila</div>
            <div className='choice'>Talon, Altavas, Aklan</div>
            <div className='choice'>Talon, City of Gingoong, Misamis Oriental</div>
          </div>
        </Cell>

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
  .table-inset {
    position: relative;
    padding: 15px 0;
  }
  .table-inset:before {
    display: block;
    content: ' ';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 5px;
    background: linear-gradient(to bottom, ${colors.monochrome[2]}, transparent);
  }
  .choices {
    display: inline-flex;
    flex-flow: column;
  }
  .choice {
    padding: 15px 20px 15px 45px;
    background: ${colors.monochrome[0]};
    border-bottom: 1px solid ${colors.monochrome[2]};
    box-shadow: 0 2.5px 5px 0 ${colors.monochrome[2]};
    position: relative;
  }
  .choice:before {
    display: block;
    content: ' ';
    width: 10px;
    height: 10px;
    box-sizing: border-box;
    border-radius: 50%;
    border: 1px solid ${colors.monochrome[2]};
    position: absolute;
    left: 20px;
    top: 20px;
  }
  .choice.-selected {
    box-shadow: inset 5px 0 0 0 ${colors.monochrome[2]};
  }
  .choice.-selected:before {
    border-color: ${colors.green};
    background: ${colors.green};
  }
`
