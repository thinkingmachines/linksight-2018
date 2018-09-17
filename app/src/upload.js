import React from 'react'
import {renderToString} from 'react-dom/server'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Colors
import * as colors from './colors'

// Elements
import Instruction from './elements'

// Layouts
import Page from './layouts/page'

// Components
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
          <Grid columns={12} gap='15px' height='100%' className='upload-bg'>
            <Cell width={8} left={3} alignContent='center' middle>
              <UploadWidget
                name='file'
                server={{
                  url: `${window.API_HOST}/api/datasets/`,
                  process: {withCredentials: true}
                }}
                allowRevert={false}
                onprocessfile={this.handleProcessFile.bind(this)}
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
      </Page>
    )
  }
}

export default styled(Upload)`
  position: relative;
  .dot {
    position: relative;
  }
  .dot:before {
    content: ' ';
    display: block;
    position: absolute;
    width: 0.25em;
    height: 0.25em;
    border-radius: 50%;
    background-color: ${colors.yellow};
    top: 0.2em;
    left: 0;
  }
  .instruction {
    display: inline-block;
    line-height: 20px;
  }
  .hero-copy {
    color: ${colors.monochrome[0]};
  }
  .hero-copy h2,
  .hero-copy p {
    margin-bottom: 20px;
  }
  .hero-copy ol {
    padding-left: 0;
  }
  .hero-copy li strong {
    border-bottom: 2px solid ${colors.yellow};
  }
  .hero-copy li {
    margin-bottom: 10px;
  }
`
