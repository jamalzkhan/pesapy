from flask import Flask, request
from syncsms import SyncSMS
import mpesaMessageParser

app = Flask(__name__)
syncsms_parser = SyncSMS.Instance()

@app.route("/")
def index():
    return "This is a sample application for the pythonpesa API"
    
@app.route("/syncsms", methods=["GET", "POST"])
def syncsms():
  if request.method == 'GET':
    return "GET request"
  else:
    data, status, message = syncsms_parser.process_request(request.form)
    if status == False:
      return message, status
    else:
      transaction = mpesaMessageParser.parse(data["message"])
      # Now you can do whatever you want with the message!
      return str(transaction)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)