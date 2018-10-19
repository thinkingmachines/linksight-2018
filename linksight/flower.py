import environ

env = environ.Env()
env.read_env('.env')

auth = '.*@thinkingmachin\.es'
oauth2_key = env('GOOGLE_OAUTH2_KEY')
oauth2_secret = env('GOOGLE_OAUTH2_SECRET')
oauth2_redirect_uri = env('FLOWER_OAUTH2_REDIRECT_URI')
