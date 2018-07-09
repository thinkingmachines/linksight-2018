import React from 'react'

class About extends React.Component {
  render () {
    return (
      <React.Fragment>
        <h1>LinkSight</h1>
        <p>Many Philippine NGOs and grassroots organizations collect, encode, analyze and derive insights from their data. However, this process is usually done manually and the data they get is only limited to what they can physically gather.</p>
        <p>They want to learn more about their communities so they more effectively target their programs and projects. Unfortunately, Philippine Census statistics are often hard to find and hard to use.</p>
        <p>LinkSight will be a repository of ready-to-use Philippine geospatial data and socioeconomic indicators that anyone can merge with their own location datasets to expand their data point of view.</p>
        <p>If you're interested in contributing or learning more about the project, you can contact us at <a href='mailto:linksight@thinkingmachin.es'>linksight@thinkingmachin.es</a></p>
      </React.Fragment>
    )
  }
}

export default About
