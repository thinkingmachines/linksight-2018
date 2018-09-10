import styled from 'styled-components'
import {FilePond} from 'react-filepond'

export default styled(FilePond)`
  z-index: 0;
  font-family: Barlow, sans-serif;
  margin-bottom: 0;
  .filepond--drop-label label {
    font-size: 15px;
    padding-top: 0;
    padding-bottom: 5px;
  }
  .filepond--drop-label label .note {
    font-size: 12px;
    margin-top: 5px;
  }
`
