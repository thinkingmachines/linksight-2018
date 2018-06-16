import React from 'react'
import styled from 'styled-components'
import { Grid, Cell } from 'styled-css-grid'

// Images
import tablemap from './images/tablemap.svg'

// Colors
import * as colors from './colors'

// Elements
import {Title} from './elements'

// Components
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
          iconUrl: require('./images/public-datasets/public-dataset-icon-population.svg')
        },
        {
          name: 'Disaster Risk Dataset',
          description: 'Risk factor per barangay (as of October 2017)',
          iconUrl: require('./images/public-datasets/public-dataset-icon-disaster.svg')
        },
        {
          name: 'Barangay Competitiveness Dataset',
          description: 'Competitiveness score per barangay',
          iconUrl: require('./images/public-datasets/public-dataset-icon-competitiveness.svg')
        }
      ]
    }
  }
  handleProcessFile (err, file) {
    if (err) {
      window.alert(err)
      return
    }
    window.alert(JSON.parse(file.serverId).id)
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
    return (
      <div className={this.props.className}>
        <Grid columns={12} gap='15px' className='page'>
          <Cell width={4} left={2} center middle>
            <img width='100%' src={tablemap} />
            <UploadWidget
              name='file'
              server='http://localhost:8000/api/datasets/'
              allowRevert={false}
              onprocessfile={this.handleProcessFile}
            />
          </Cell>
          <Cell width={4} left={7}>
            <Title className='-light'>Expand your<br />data po<span className='dot'>i</span>nt of v<span className='dot'>i</span>ew</Title>
            <br />
            <p className='subtitle -light'>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua connect to public datasets:</p>
            <br />
            {this.renderDatasetCards()}
          </Cell>
        </Grid>
      </div>
    )
  }
}

export default styled(Upload)`
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
