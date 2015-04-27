import ConfigParser
from Singleton import Singleton

@Singleton
class Config():
  """Wrapper class around the python ConfigParser, made as a singleton"""
  
  def __init__(self):
    self.config = ConfigParser.RawConfigParser()
    self.file_name="config.conf"
    self.config.read(self.file_name)
    
  def get(self, header, field):
    """Gets the value of a field for a particular header form the config file"""
    return self.config.get(header, field)