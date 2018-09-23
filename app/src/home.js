import React from 'react'
import styled from 'styled-components'
import {Grid, Cell} from 'styled-css-grid'

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

const GoogleIcon = () => (
  <svg viewBox='0 0 46 46'>
    <g fill='none' fillRule='evenodd'>
      <path d='M31.64 23.205c0-.639-.057-1.252-.164-1.841H23v3.481h4.844a4.14 4.14 0 0 1-1.796 2.716v2.259h2.908c1.702-1.567 2.684-3.875 2.684-6.615z' fill='#4285F4' />
      <path d='M23 32c2.43 0 4.467-.806 5.956-2.18l-2.908-2.259c-.806.54-1.837.86-3.048.86-2.344 0-4.328-1.584-5.036-3.711h-3.007v2.332A8.997 8.997 0 0 0 23 32z' fill='#34A853' />
      <path d='M17.964 24.71a5.41 5.41 0 0 1-.282-1.71c0-.593.102-1.17.282-1.71v-2.332h-3.007A8.996 8.996 0 0 0 14 23c0 1.452.348 2.827.957 4.042l3.007-2.332z' fill='#FBBC05' />
      <path d='M23 17.58c1.321 0 2.508.454 3.44 1.345l2.582-2.58C27.463 14.891 25.426 14 23 14a8.997 8.997 0 0 0-8.043 4.958l3.007 2.332c.708-2.127 2.692-3.71 5.036-3.71z' fill='#EA4335' />
      <path d='M14 14h18v18H14V14z' />
    </g>
  </svg>
)

class Home extends React.Component {
  constructor (props) {
    super(props)
    this.state = {unapproved: false}
  }
  componentDidMount () {
    const unapproved = new window.URLSearchParams(window.location.search)
      .get('unapproved')
    this.setState({unapproved})
  }
  render () {
    return (
      <Page withHeader>
        <Header />
        <Cell width={12} className={this.props.className}>
          <Grid columns={12} gap='15px' height='100%' alignContent='center'>
            <Cell width={4} left={2} center middle>
              <img width='100%' src={tablemap} alt='map with pins' />
            </Cell>
            <Cell width={4} left={7} className='hero-copy'>
              <Title>
                Messy Philippine place names?
              </Title>
              <br />
              <h2>
                Automatically standardize the names of barangays,
                municipalities, cities, and provinces.
              </h2>
              <br />
              <a href={`${window.API_HOST}/login/google-oauth2`} className='sign-in'>
                <GoogleIcon />
                <span>Sign in with Google</span>
              </a>
              <br />
              <div className='request'>
                {this.state.unapproved ? (
                  <p className='-register'>
                    <strong>{this.state.unapproved}</strong> doesn't have access to LinkSight yet.<br />
                    Sign up by answering&nbsp;
                    <a
                      className='-link'
                      href='https://thinkingmachines.typeform.com/to/Am40jZ'
                      target='_blank'
                    >
                      this form.
                    </a>
                  </p>
                ) : null}
              </div>
            </Cell>
          </Grid>
        </Cell>
      </Page>
    )
  }
}

export default styled(Home)`
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
  .sign-in {
    display: inline-flex;
    background: #4285F4;
    color: white;
    text-decoration: none;
    align-items: center;
  }
  .sign-in svg {
    background: ${colors.monochrome[0]};
    height: 3em;
  }
  .sign-in span {
    margin: 0 15px;
  }
  .request .-register,
  .request .-link {
    margin: 20px 0;
    color: ${colors.monochrome[0]};
  }
`
