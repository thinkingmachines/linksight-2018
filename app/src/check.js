import React from 'react'
import styled from 'styled-components'
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
import MatchesTable from './components/matches-table'
import LoadingOverlay from './components/loading-overlay'
import ErrorOverlay from './components/error-overlay'

// API
import api from './api'

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
      withCredentials: true,
      complete: ({data, meta}) => {
        const {matchItems, matchChoices} = this.processItems(data)
        this.setState({matchItems, matchChoices}, () => {
          // Go straight to export when there are no matches to check
          const multipleMatchesCount = this.state.matchItems
            .filter(item => item.match_type === 'near')
            .length
          if (multipleMatchesCount === 0) {
            this.saveChoices()
          }
        })
      }
    })
  }
  processItems (items) {
    let prevIndex = null
    return items.reduce((obj, item) => {
      if (item.match_type === 'near') {
        if (item.dataset_index === prevIndex) {
          let n = obj.matchItems.length
          let lastItem = obj.matchItems[n - 1]
          obj.matchItems[n - 1] = {
            ...lastItem,
            choices: [...lastItem.choices, item]
          }
        } else {
          obj.matchItems = [
            ...obj.matchItems,
            {
              ...item,
              choices: [item]
            }
          ]
          // Select first choice
          obj.matchChoices[item.dataset_index] = item.id
        }
        prevIndex = item.dataset_index
      } else {
        obj.matchItems = [...obj.matchItems, item]
      }
      return obj
    }, {matchItems: [], matchChoices: {}})
  }
  handleChoice (item) {
    this.setState(prevState => ({
      matchChoices: {
        ...prevState.matchChoices,
        [item.dataset_index]: item.id
      }
    }))
  }
  getExactCount () {
    return this.state.matchItems.filter(item => item.match_type === 'exact').length
  }
  getMultipleCount () {
    return this.state.matchItems.filter(item => (
      item.match_type === 'near' && this.state.matchChoices[item.dataset_index]
    )).length
  }
  getNoMatchesCount () {
    return this.state.matchItems.filter(item => item.match_type === 'no_match').length
  }
  saveChoices () {
    const {matchChoices} = this.state
    const {id} = this.props.match.params
    this.setState({isSaving: true})
    api.post(
      `/matches/${id}/save-choices`, {
        match_choices: matchChoices
      })
      .then(resp => this.setState({
        isSaving: false,
        isSaved: true
      }))
      .catch(_ => this.setState({
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
          backButton={
            <Button className='btn -back' onClick={this.props.history.goBack}>Back</Button>
          }
          nextButton={
            <Button className='btn' onClick={this.saveChoices.bind(this)}>Next</Button>
          }
        >
          <ol className='steps'>
            <li>Upload your data</li>
            <li>Prep your data</li>
            <li className='current'>
              <p>Review matches</p>
              <ul className='step-desc'>
                <li>For locations with more than one possible match, select the one you think is correct.</li>
                <li>If none of the candidates are the right match, please select "No correct match/Unsure."</li>
              </ul>
            </li>
            <li>Check new columns and export</li>
            <li>Give feedback</li>
          </ol>
        </Sidebar>
        <Cell width={9} className={this.props.className}>
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
                Out of the {this.state.matchItems.length} records in your dataset, <strong> {this.getMultipleCount()} </strong> need your review.
              </Instruction>
              <MatchesTable
                items={this.state.matchItems.filter(matchItem => matchItem.match_type === 'near')}
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
