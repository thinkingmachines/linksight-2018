accesslog = '/deploy/gunicorn-access.log'
errorlog = '/deploy/gunicorn-error.log'
proc_name = 'linksight'
daemon = True
pidfile = '/deploy/gunicorn.pid'
workers = 2
timeout = 360
