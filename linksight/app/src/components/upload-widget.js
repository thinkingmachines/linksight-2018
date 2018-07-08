import styled from 'styled-components'
import {FilePond} from 'react-filepond'

export default styled(FilePond)`
  z-index: 0;
  font-family: Barlow, sans-serif;
  .filepond--drop-label label {
    font-size: 15px;
    padding-top: 0;
    padding-bottom: 5px;
  }
  .filepond--drop-label label .requirements {
    font-size: 12px;
  }
`
