bind = '0.0.0.0:8081'
worker_class = 'gevent'
daemon = False
timeout = 3600

loglevel = 'info'
errorlog = './log/error.log'
accesslog = './log/access.log'
