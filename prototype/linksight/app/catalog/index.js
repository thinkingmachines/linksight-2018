import React from 'react'
import ReactDOM from 'react-dom'
import { Catalog, pageLoader } from 'catalog'

// Stylesheets
import typographyStyles from '../src/css/typography.css'
import toggleStyles from '../src/css/react-toggle.css'
import filepondStyles from 'filepond/dist/filepond.min.css'

// Images
import logo from '../src/images/linksight-logo.png'
import datasetCardIconUrl from '../src/images/public-datasets/public-dataset-icon-population.svg'

// Colors
import * as colors from '../src/colors.js'

// Elements
import * as elements from '../src/elements'

// Components
import DatasetCard from '../src/components/dataset-card'
import UploadWidget from '../src/components/upload-widget'
import PreviewTable from '../src/components/preview-table'
import LocationColumn from '../src/components/location-column'

const pages = [
  {
    title: 'Branding',
    pages: [
      {
        path: '/',
        title: 'Logo',
        content: pageLoader(() => import('./branding/logo.md'))
      },
      {
        path: '/colors',
        title: 'Colors',
        content: pageLoader(() => import('./branding/colors.md'))
      },
      {
        path: '/typography',
        title: 'Typography',
        content: pageLoader(() => import('./branding/typography.md'))
      }
    ]
  },
  {
    path: '/elements',
    title: 'Elements',
    content: pageLoader(() => import('./elements.md'))
  },
  {
    title: 'Components',
    pages: [
      {
        path: '/components',
        title: 'UploadWidget',
        content: pageLoader(() => import('./components/upload-widget.md'))
      },
      {
        path: '/components/dataset-card',
        title: 'DatasetCard',
        content: pageLoader(() => import('./components/dataset-card.md'))
      },
      {
        path: '/components/preview-table',
        title: 'PreviewTable',
        content: pageLoader(() => import('./components/preview-table.md'))
      },
      {
        path: '/components/location-column',
        title: 'LocationColumn',
        content: pageLoader(() => import('./components/location-column.md'))
      }
    ]
  }
]

const styles = [
  typographyStyles,
  toggleStyles,
  filepondStyles
]

const imports = {
  ...colors,
  monochrome: colors.monochrome.map((c) => ({value: c})),
  ...elements,
  DatasetCard,
  datasetCardIconUrl,
  UploadWidget,
  PreviewTable,
  LocationColumn
}

ReactDOM.render(
  <Catalog
    title='LinkSight'
    logoSrc={logo}
    pages={pages}
    styles={styles}
    imports={imports}
    useBrowserHistory
  />,
  document.getElementById('catalog')
)
