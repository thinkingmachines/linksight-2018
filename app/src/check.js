import React from 'react'
import styled from 'styled-components'
import axios from 'axios'
import Papa from 'papaparse'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Colors
import * as colors from './colors'

// Elements
import {Button, Instruction} from './elements'

// Layouts
import Page from './layouts/page'

// Components
import Sidebar from './components/sidebar'
import ToggleList from './components/toggle-list'
import MatchesTable from './components/matches-table'
import LoadingOverlay from './components/loading-overlay'
import ErrorOverlay from './components/error-overlay'

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
    Papa.parse(`${window.API_HOST}/api/matches/${id}/items`, {
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
      if (item.matched === 'True' || item.matched === null) {
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
  getIdentifiedCount () {
    return this.state.matchItems.filter(item => item.matched === 'True').length
  }
  getMultipleCount () {
    return this.state.matchItems.filter(item => (
      !~['True', null].indexOf(item.matched) && !this.state.matchChoices[item.dataset_index]
    )).length
  }
  getCheckedCount () {
    return this.state.matchItems.filter(item => (
      !~['True', null].indexOf(item.matched) && this.state.matchChoices[item.dataset_index]
    )).length
  }
  getNoMatchesCount () {
    return this.state.matchItems.filter(item => item.matched === null).length
  }
  saveChoices () {
    const {matchChoices} = this.state
    const {id} = this.props.match.params
    this.setState({isSaving: true})
    axios.post(
      `${window.API_HOST}/api/matches/${id}/save-choices`, {
        match_choices: matchChoices
      })
      .then(resp => this.setState({
        isSaving: false,
        isSaved: true
      }))
      .catch(error => this.setState({
        isSaving: false,
        error: <p>
          Uh oh! An unexpected error has occured.<br />
          We've been notified about this and will try to<br />
          look into it as soon as possible!
        </p>
      }))
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
            <Button onClick={this.saveChoices.bind(this)}>Proceed</Button>
          }
        >
          <ToggleList
            title='Tags'
            bullet='square'
            items={[
              {
                toggled: true,
                color: colors.green,
                label: `Identified locations (${this.getIdentifiedCount()})`
              },
              {
                toggled: true,
                color: colors.orange,
                label: `Multiple matches (${this.getMultipleCount()})`
              },
              {
                toggled: true,
                color: colors.yellow,
                label: `Checked matches (${this.getCheckedCount()})`
              },
              {
                toggled: true,
                color: colors.purple,
                label: `No matches (${this.getNoMatchesCount()})`
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
          {this.state.error ? (
            <ErrorOverlay>
              {this.state.error}
            </ErrorOverlay>
          ) : null}
          <Grid columns={1} gap='0' height='calc(100vh - 30px)'>
            <Cell className='matches'>
              <Instruction className='instruction'>
                <strong>
                  We've identified {this.getIdentifiedCount()} of the locations!
                </strong> <span>
                  For records with multiple matches, select the correct location
                  match from the list below it. Unchecked records will be
                  excluded from the export.
                </span>
              </Instruction>
              <MatchesTable
                items={this.state.matchItems.filter(matchItem => matchItem.matched === 'False')}
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
  .instruction {
    margin: 0 30px 20px;
  }
  .matches {
    background: ${colors.monochrome[1]};
    padding: 30px;
    box-sizing: border-box;
    overflow-y: auto;
  }
`
