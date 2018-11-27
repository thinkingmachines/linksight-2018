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
      cwd: 'api',
      script: 'manage.py',
      args: 'runserver',
      interpreter: 'venv/bin/python',
      autorestart: false
    },
    {
      name: 'worker',
      cwd: 'api',
      script: 'venv/bin/celery',
      args: '-A api worker -P gevent --loglevel INFO',
      interpreter: 'venv/bin/python',
      autorestart: false
    },
    {
      name: 'flower',
      cwd: 'api',
      script: 'venv/bin/flower',
      args: 'venv/bin/flower -A api --conf=flower.py',
      interpreter: 'venv/bin/python',
      autorestart: false
    }
  ]
}
