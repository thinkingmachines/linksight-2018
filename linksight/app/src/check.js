import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import Papa from 'papaparse'

// Colors
import * as colors from './colors'

// Layouts
import Page from './layouts/page'

// Components
import Sidebar from './components/sidebar'
import MatchesTable from './components/matches-table'

class Check extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      matchItems: null,
      matchChoices: {}
    }
  }
  nestItems (items) {
    let prevIndex = null
    return items.reduce((matchItems, item) => {
      if (item.matched === 'True') {
        matchItems = [...matchItems, item]
      } else {
        if (item.dataset_index === prevIndex) {
          let n = matchItems.length
          let lastItem = matchItems[n - 1]
          matchItems[n - 1] = {
            ...lastItem,
            choices: [...lastItem.choices, item]
          }
        } else {
          matchItems = [...matchItems, {...item, choices: [item]}]
        }
        prevIndex = item.dataset_index
      }
      return matchItems
    }, [])
  }
  handleChoice (item) {
    this.setState(prevState => ({
      matchChoices: {
        ...prevState.matchChoices,
        [item.dataset_index]: item.id
      }
    }))
  }
  componentDidMount () {
    const {id} = this.props.match.params
    Papa.parse(`http://localhost:8000/api/matches/${id}/items`, {
      download: true,
      header: true,
      dynamicTyping: true,
      skipEmptyLines: true,
      complete: ({data, meta}) => {
        this.setState({matchItems: this.nestItems(data)})
      }
    })
  }
  render () {
    if (!this.state.matchItems) {
      return null
    }
    return (
      <Page match={this.props.match}>
        <Sidebar />
        <Cell width={10} className={this.props.className}>
          <Grid columns={1} rows='40% 60%' gap='0' height='100vh'>
            <Cell className='map'>
              <iframe
                src='https://www.google.com/maps/embed/v1/place?q=place_id:ChIJr5Qp-vPIlzMRCuRgR6-IyYk&key=AIzaSyCIXyqG6o62e9kcnpLR_3Pz317ybfDWLiw'
                width='100%'
                height='100%'
                frameBorder='0'
                allowFullScreen
              />
            </Cell>
            <Cell className='matches'>
              <MatchesTable
                items={this.state.matchItems}
                matchChoices={this.state.matchChoices}
                onChoose={this.handleChoice.bind(this)}
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
