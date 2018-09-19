module.exports = {
  use: [
    [
      '@neutrinojs/standardjs',
      {
        eslint: {
          rules: {
            'babel/object-curly-spacing': ['error', 'never']
          }
        }
      }
    ],
    [
      '@neutrinojs/react',
      {
        html: {
          title: 'LinkSight',
          appMountId: 'app-root',
          appMountIds: ['modal-root'],
          baseHref: '/',
          googleAnalytics: {
            trackingId: 'UA-123415402-1'
          },
          links: [
            'https://fonts.googleapis.com/css?family=Barlow:400,400i,700',
            '/static/css/base.css',
            '/static/css/typography.css',
            '/static/css/react-toggle.css',
            {rel: 'manifest', href: '/static/manifest.json'},
            {rel: 'short icon', href: '/static/favicon.ico'}
          ],
          scripts: [
            'https://static.airtable.com/js/embed/embed_snippet_v1.js'
          ],
          window: {
            API_HOST: process.env.PUBLIC_URL || 'http://localhost:8000'
          }
        },
        devServer: {
          port: 3000
        },
        manifest: true
      }
    ],
    '@neutrinojs/jest'
  ]
}
