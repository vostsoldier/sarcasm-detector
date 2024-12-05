import nltk
import ssl
import certifi

ssl._create_default_https_context = ssl._create_unverified_context
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

nltk.download('words', download_dir='/tmp/nltk_data')
