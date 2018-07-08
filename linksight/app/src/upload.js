import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'
import {Redirect} from 'react-router-dom'

// Images
import tablemap from './images/tablemap.svg'

// Colors
import * as colors from './colors'

// Elements
import {Title} from './elements'

// Layouts
import Page from './layouts/page'

// Components
import Header from './components/header'
import DatasetCard from './components/dataset-card'
import UploadWidget from './components/upload-widget'

class Upload extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      datasets: [
        {
          name: 'PSA Population Dataset',
          description: 'Population per barangay (as of August 2015)',
          iconUrl: require('./images/public-datasets/public-dataset-icon-population.svg'),
          defaultChecked: true,
          disabled: true
        },
        {
          name: 'Disaster Risk Dataset',
          description: <em>Coming soon</em>,
          iconUrl: require('./images/public-datasets/public-dataset-icon-disaster.svg'),
          defaultChecked: false,
          disabled: true
        },
        {
          name: 'Barangay Competitiveness Dataset',
          description: <em>Coming soon</em>,
          iconUrl: require('./images/public-datasets/public-dataset-icon-competitiveness.svg'),
          defaultChecked: false,
          disabled: true
        }
      ]
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
              <img width='100%' src={tablemap} />
              <UploadWidget
                name='file'
                server={`${window.API_HOST}/api/datasets/`}
                allowRevert={false}
                onprocessfile={this.handleProcessFile.bind(this)}
              />
            </Cell>
            <Cell width={4} left={7}>
              <Title className='-light'>Expand your<br />data po<span className='dot'>i</span>nt of v<span className='dot'>i</span>ew</Title>
              <br />
              <p className='subtitle -light'>Combine a list of locations with any of the following barangay-level datasets:</p>
              <br />
              {this.renderDatasetCards()}
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
`
