import React from 'react'
import ReactDOM from 'react-dom'
import { Catalog, pageLoader } from 'catalog'

// Images
import logo from '../public/images/linksight-logo.png'

// Stylesheets
import typographyStyles from '../public/css/typography.css'
import toggleStyles from '../public/css/react-toggle.css'

// Colors
import * as colors from '../src/colors.js'

// Elements
import {
  Title,
  Button,
  PrimaryButton,
  Toggle
} from '../src/elements'

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
  }
]

const styles = [
  typographyStyles,
  toggleStyles
]

const imports = {
  ...colors,
  monochrome: colors.monochrome.map((c) => ({value: c})),
  Title,
  Button,
  PrimaryButton,
  Toggle
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
