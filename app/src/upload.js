import React from 'react'
import {renderToString} from 'react-dom/server'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Images
import tablemap from './images/tablemap.svg'

// Colors
import * as colors from './colors'

// Elements
import {Title, Instruction} from './elements'

// Layouts
import Page from './layouts/page'

// Components
import Header from './components/header'
import DatasetCard from './components/dataset-card'
import UploadWidget from './components/upload-widget'
import UploadNotice from './components/upload-notice'

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
      <Page withHeader>
        <Header />
        <Cell width={12} className={this.props.className}>
          <Grid columns={12} gap='15px' height='100%' alignContent='center'>
            <Cell width={4} left={2} center middle>
              <img width='100%' src={tablemap} alt='map with pins' />
              <UploadNotice>
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
                    <p class='note'>
                      Locations file requirements:
                      CSV file type, max 1000 rows with Barangay, City/Municipality, Province in separate columns
                    </p>
                    <p class='note -muted'>
                      We need to temporarily save a copy of your data to process it.
                      The copy will be deleted from our system within 24 hours of upload.
                    </p>
                  `}
                />
              </UploadNotice>
            </Cell>
            <Cell width={4} left={7} className='hero-copy'>
              <Title>
                Clean up messy Philippine place names
              </Title>
              <br />
              <h2>
                LinkSight matches barangay, city, municipality, and provincial names with their closest-matching items in the Philippine Standard Geographic Code (PSGC).
              </h2>
              <p>How to use it:</p>
              <ol>
                <li><strong>Upload</strong> a CSV that has separate columns for each administrative level: barangay, municipality or city, and province. For now we only take CSVs with fewer than 1000 rows.</li>
                <li><strong>Preview</strong> the first 10 rows of your dataset. Indicate which columns refer to which administrative level.</li>
                <li><strong>Match</strong> with the PSGC and view the results. For places that have more than one possible PSGC, select the best match from among the candidates presented. We use fuzzy matching and record linkage techniques to rank the closest matches, despite spelling differences.</li>
                <li><strong>Export</strong> the dataset as a CSV file.</li>
              </ol>
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
