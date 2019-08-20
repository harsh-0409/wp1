import logging

import mwclient

logger = logging.getLogger(__name__)
_ua = 'WP1.0Bot/3.0. Run by User:Audiodude. Using mwclient/0.9.1'

def get_credentials():
  try:
    from wp1.credentials import API_CREDS
    return API_CREDS
  except ImportError:
    # No credentials, probably in development environment.
    pass

site = None
def login():
  global site
  try:
    api_creds = get_credentials()
    print(repr(api_creds))
    if api_creds is None:
      logger.warning('Not creating site, no credentials')
      return
    site = mwclient.Site('en.wikipedia.org', clients_useragent=_ua)
    print(repr(site))
    site.login(api_creds['user'], api_creds['pass'])
  except mwclient.errors.LoginError:
    logger.exception('Exception logging into wikipedia')


# Global login on startup.
login()

def get_page(name):
  if not site:
    logger.error('Could not get page %s because api site is not defined', name)
    return None

  return site.pages[name]

def save_page(page, wikicode, msg):
  if not site:
    logger.error('Could not save page %s because api site is not defined', page)
    return False

  try:
    page.save(wikicode, msg)
  except mwclient.errors.AssertUserFailedError as e:
    logger.warning('Got login exception, retrying login')
    login()
    page.save(wikicode, msg)
  return True
