module.exports = {
  apps: [
    {
      name: 'web',
      cwd: 'app',
      script: 'npm',
      args: 'start',
      autorestart: false
    },
    {
      name: 'api',
      script: 'manage.py',
      args: 'runserver',
      interpreter: 'venv/bin/python',
      autorestart: false
    },
    {
      name: 'worker',
      script: 'venv/bin/celery',
      args: '-A linksight worker -P gevent --loglevel INFO',
      interpreter: 'venv/bin/python',
      autorestart: false
    },
    {
      name: 'flower',
      script: 'venv/bin/flower',
      args: 'venv/bin/flower -A linksight --conf=linksight/flower.py',
      interpreter: 'venv/bin/python',
      autorestart: false
    }
  ]
}
