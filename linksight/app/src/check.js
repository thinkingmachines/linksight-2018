import React from 'react'
import styled from 'styled-components'
import axios from 'axios'
import Papa from 'papaparse'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Colors
import * as colors from './colors'

// Elements
import {Button} from './elements'

// Layouts
import Page from './layouts/page'

// Components
import Sidebar from './components/sidebar'
import ToggleList from './components/toggle-list'
import MatchesTable from './components/matches-table'
import LoadingOverlay from './components/loading-overlay'

class Check extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      matchItems: null,
      matchChoices: {},
      isSaving: false,
      isSaved: false
    }
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
  getFoundCount () {
    return this.state.matchItems.filter(item => item.matched === 'True').length
  }
  getMultipleCount () {
    return this.state.matchItems.filter(item => item.matched !== 'True').length
  }
  saveChoices () {
    const {matchChoices} = this.state
    const {id} = this.props.match.params
    this.setState({isSaving: true})
    axios.post(
      `http://localhost:8000/api/matches/${id}/save-choices`, {
        match_choices: matchChoices
      })
      .then(resp => {
        this.setState({
          isSaving: false,
          isSaved: true
        })
      })
  }
  render () {
    if (!this.state.matchItems) {
      return null
    }
    if (this.state.isSaved) {
      return <Redirect push to={`/matches/${this.props.match.params.id}/export`} />
    }
    return (
      <Page>
        <Sidebar
          button={
            Object.keys(this.state.matchChoices).length === this.getMultipleCount()
              ? <Button onClick={this.saveChoices.bind(this)}>Proceed</Button>
              : null
          }
        >
          <ToggleList
            title='Tags'
            bullet='square'
            items={[
              {
                toggled: true,
                color: colors.green,
                label: `Found locations (${this.getFoundCount()})`
              },
              {
                toggled: true,
                color: colors.orange,
                label: `Multiple matches (${this.getMultipleCount()})`
              }
            ]}
          />
          <ToggleList
            title='Columns'
            bullet='circle'
            items={[
              {toggled: true, label: 'Barangay'},
              {toggled: true, label: 'City/Municipality'},
              {toggled: true, label: 'Province'}
            ]}
          />
        </Sidebar>
        <Cell width={10} className={this.props.className}>
          {this.state.isSaving ? (
            <LoadingOverlay>Saving choices&hellip;</LoadingOverlay>
          ) : null}
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
