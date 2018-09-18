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
        'rowsShown': 100
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
      'PSGC': colors.green,
      'Population': colors.orange,
      'Administrative Level': colors.orange
    }
  }
  askFeedback () {
    this.setState({isExported: true})
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
        <Cell width={9} className={this.props.className}>
          <div className='summary'>
            <Instruction>
              <p>We've added the following new columns to your file:</p>
              <ul>
                <li><strong>Barangay_Linksight</strong> - Standardized barangay names.</li>
                <li><strong>MuniCity_Linksight </strong> - Standardized municipality or city names.</li>
                <li><strong>Province_Linksight </strong> - Standardized province names.</li>
                <li><strong>PSG_Code</strong> - Each location has a unique 9-digit ID number based on the PSGC.</li>
                <li><strong>Confidence Score</strong> - Each match has a confidence score on a scale of 0 to 100. Exact matches are 100%.</li>
              </ul>
            </Instruction>
          </div>
          <PreviewTable
            preview={this.state.preview}
            columnHighlights={this.getColumnHighlights()}
          />
        </Cell>
        <Sidebar
          backButton={
            <Button className='btn -back' onClick={this.props.history.goBack}>Back</Button>
          }
          nextButton={
            <a href={`${window.API_HOST}${this.state.preview.file.url}`}>
              <Button className='btn' onClick={this.askFeedback.bind(this)}>Export</Button>
            </a>
          }
        >
          <ol className='steps'>
            <li>Upload your data</li>
            <li>Prep your data</li>
            <li>Review matches</li>
            <li className='current'>Check new columns and export</li>
            <p className='step-desc'>You may now export your expanded dataset in CSV. Check out the new columns containing the cleaned location names.</p>
            <li>Give feedback</li>
          </ol>
        </Sidebar>
      </Page>
    )
  }
}

export default styled(Export)`
  position: relative;
  background: ${colors.monochrome[0]};
  padding: 60px;
  box-sizing: border-box;
  .summary {
    background: ${colors.monochrome[1]};
    border-radius: 7.5px;
    display: flex;
    justify-content: center;
    flex-direction: column;
    padding: 20px 40px;
    margin-bottom: 20px;
  }
`
