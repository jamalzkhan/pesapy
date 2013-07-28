from Singleton import Singleton
from Config import Config

@Singleton
class SyncSMS:
  """Class used to parse SMS from the SyncSMS service"""

  def __init__(self):
    print 'Singleton created'
    self.secret_field = 'secret'
    self.fields = ['from', 'message', self.secret_field, 'sent_timestamp']
    self.config = Config.Instance()
    
    
  def process_request(self, data):
    """Main method used for processing a request"""
    fields, status, message = self.parse_post_request(data)
    if status:
      if not self.check_secret(fields):
        status = False
        message = "The secrets do not match"
    return fields, status, message
    
  def check_secret(self, data):
    return data[self.secret_field] == self.config.get('syncsms', self.secret_field)

  def parse_post_request(self, data):
    """Takes POST data from a request and returns a dictionary and tuple"""
    """Returns (_, True) if all the data in self.fields present, (_, False) otherwise"""
    fields={}
    for i in self.fields:
      if data.has_key(i):
        fields[i] = data[i]
      else:
        return (fields, False, "All the fields from SyncSMS are not included")
    return (fields, True, "Success")

if __name__ == "__main__":
  s  = SyncSMS()