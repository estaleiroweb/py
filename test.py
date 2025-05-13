import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
print(find_dotenv())
print(os.environ['XPTO'])
