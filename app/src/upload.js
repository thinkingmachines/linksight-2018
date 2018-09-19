import React from 'react'
import {renderToString} from 'react-dom/server'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Colors
import * as colors from './colors'

// Elements
import {Instruction} from './elements'

// Layouts
import Page from './layouts/page'

// Components
import Sidebar from './components/sidebar'
import DatasetCard from './components/dataset-card'
import UploadWidget from './components/upload-widget'

class Upload extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      datasetId: null
    }
  }
  handleProcessFile (err, file) {
    if (err) {
      return
    }
    let datasetId = JSON.parse(file.serverId).id
    this.setState({datasetId})
  }
  renderDatasetCards () {
    return (
      <Grid columns={1} gap='15px'>
        {this.state.datasets.map((dataset, i) => (
          <Cell key={i}>
            <DatasetCard {...dataset} />
          </Cell>
        ))}
      </Grid>
    )
  }
  renderInstruction () {
    return renderToString(
      <Instruction className='instruction'>
        Drag your file or <span className='filepond--label-action'>Browse</span>
      </Instruction>
    )
  }
  render () {
    if (this.state.datasetId) {
      return <Redirect push to={`/datasets/${this.state.datasetId}/preview`} />
    }
    return (
      <Page>
        <Cell width={9} className={this.props.className}>
          <Grid columns={12} gap='15px' height='100%' className='upload'>
            <Cell width={6} left={4} alignContent='center' middle>
              <UploadWidget
                name='file'
                maxFileSize='5MB'
                server={{
                  url: `${window.API_HOST}/api/datasets/`,
                  process: {
                    withCredentials: true,
                    onerror: JSON.parse
                  }
                }}
                allowRevert={false}
                onprocessfile={this.handleProcessFile.bind(this)}
                labelFileProcessingError={error => error.body.file[0]}
                labelIdle={`
                  ${this.renderInstruction()}
                `}
              />
              <div className='upload-desc'>
                <p className='note reqs'>File requirements:</p>
                <ul className='note reqs'>
                  <li>CSV file</li>
                  <li>Maximum 3000 rows</li>
                  <li>Barangay, Municipality or City, or Province (whichever is available) should be in separate columns.</li>
                </ul>
                <br />
                <p className='note -important'><strong>Important</strong>: Linksight needs to save a copy of your data to process it. The copy will be deleted from our system within 24 hours of upload.</p>
              </div>
            </Cell>
          </Grid>
        </Cell>
        <Sidebar>
          <ol className='steps'>
            <li className='current'>
              <p>Upload your data</p>
              <p className='step-desc'>
                Upload a dataset that meets the file requirements.
              </p>
            </li>
            <li>Prep your data</li>
            <li>Review matches</li>
            <li>Check new columns and export</li>
            <li>Give feedback</li>
          </ol>
        </Sidebar>
      </Page>
    )
  }
}

export default styled(Upload)`
  position: relative;
  background: ${colors.monochrome[0]};
  .instruction {
    display: inline-block;
    line-height: 20px;
  }
  .upload {
    padding: 30px;
    box-sizing: border-box;
    overflow-y: auto;
  }
  .upload-desc {
    margin: 20px;
  }
  .upload-desc .note {
    color: ${colors.monochrome[4]};
  }
`
