import React from 'react'
import styled from 'styled-components'
import {Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Colors
import * as colors from './colors'

// Elements
import {Button, Instruction} from './elements'

// Layouts
import Page from './layouts/page'

// Components
import Sidebar from './components/sidebar'
import PreviewTable from './components/preview-table'

// API
import api from './api'

class Export extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      preview: null,
      isExported: null
    }
  }
  componentDidMount () {
    const {id} = this.props.match.params
    api.get(`/matches/${id}/preview`, {
      params: {
        'rowsShown': 5
      }
    })
      .then(resp => {
        this.setState({preview: resp.data})
      })
  }
  getFields () {
    const {fields} = this.state.preview.schema
    return fields.filter(field => field.name !== 'index')
  }
  getColumnHighlights () {
    return {
      'bgy_linksight': colors.green,
      'municity_linksight': colors.green,
      'prov_linksight': colors.green,
      'psgc_linksight': colors.green,
      'confidence_score_linksight': colors.green
    }
  }
  askFeedback () {
    this.setState({isExported: true})
  }
  renderColumns (match) {
    const columns = []
    switch (true) {
      case !!match.barangayCol:
        columns.push(
          <li key='bgy'><strong>bgy_linksight</strong> - Standardized barangay names.</li>
        )
      case !!match.cityMunicipalityCol:
        columns.push(
          <li key='municity'><strong>municity_linksight </strong> - Standardized municipality or city names.</li>
        )
      case !!match.provinceCol:
        columns.push(
          <li key='prov'><strong>prov_linksight </strong> - Standardized province names.</li>
        )
    }
    return columns
  }
  render () {
    if (!this.state.preview) {
      return null
    }
    if (this.state.isExported) {
      return <Redirect push to={`/feedback`} />
    }
    return (
      <Page>
        <Sidebar
          backButton={
            <Button className='btn -back' onClick={this.props.history.goBack}>Back</Button>
          }
          nextButton={
            <a href={`${this.state.preview.file.url}`}>
              <Button className='btn' onClick={this.askFeedback.bind(this)}>Export</Button>
            </a>
          }
        >
          <ol className='steps'>
            <li>Upload your data</li>
            <li>Prep your data</li>
            <li>Review matches</li>
            <li className='current'>
              <p>Check new columns and export</p>
              <p className='step-desc'>You may now export your expanded dataset in CSV. Check out the new columns containing the cleaned location names.</p>
            </li>
            <li>Give feedback</li>
          </ol>
        </Sidebar>
        <Cell width={9} className={this.props.className}>
          <div className='summary'>
            <Instruction>
              We've added the following new columns to your file:
            </Instruction>
            <ul>
              {this.renderColumns(this.state.preview.match)}
              <li><strong>psgc_linksight</strong> - Each location has a unique 9-digit ID number based on the PSGC.</li>
              <li><strong>confidence_score_linksight</strong> - Each match has a confidence score on a scale of 0 to 100. Exact matches are 100%.</li>
            </ul>
          </div>
          <PreviewTable
            preview={this.state.preview}
            columnHighlights={this.getColumnHighlights()}
          />
        </Cell>
      </Page>
    )
  }
}

export default styled(Export)`
  position: relative;
  background: ${colors.monochrome[0]};
  padding: 60px;
  box-sizing: border-box;
  overflow-y: auto;

  .summary {
    background: ${colors.monochrome[1]};
    border-radius: 7.5px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    padding: 20px 40px;
    margin-bottom: 20px;
  }

  .summary ul {
    margin-top: 10px;
    padding-left: 0;
    list-style: none;
  }
`
