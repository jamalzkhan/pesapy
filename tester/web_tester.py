#!/usr/bin/python
import ConfigParser, requests, time

class WebTester:
    """Class used to wrap up the whole web server"""

    def __init__(self, url, end_point, secret_key):
        self.url = url
        self.end_point = end_point
        self.secret_key = secret_key

    def send_request( self, message ):
        payload = { "message": message }
        url = "http://" + self.url + "/" + self.end_point
        r = requests.post(url, message)
        print(r.text)

class DummyMessage:
    """Class used to hold example messages and their description"""

    def __init__( self, desc, message ):
        self.desc = desc
        self.message = message

def main():

    config = ConfigParser.RawConfigParser()
    config.read( './config.conf' )

    server_url  = config.get( 'web server', 'server_url' )
    end_point   = config.get( 'web server', 'end_point' )

    device_id   = config.get( 'device', 'device_id' )
    secret_key  = config.get( 'device', 'secret_key' )
    sender      = config.get( 'device', 'sender')
    timestamp   = time.time()

    examples = []

    for i in range(1, 15):
        example_key = 'example '+str(i)
        example_desc = config.get( example_key, 'desc')
        example_message = config.get( example_key, 'message')

        example = DummyMessage( example_desc, example_message )
        examples.append( example )

    # Interpreter loop here (for the user to choose the example they want)

    w = WebTester( server_url, end_point, secret_key )
    message = examples[1].message
    params = { "message" : message, "from" : sender, "secret": "secret_testing", "sent_timestamp" : 123 }
    w.send_request( params )

    # Start the parsing section here now

if __name__ == "__main__":
    main()
