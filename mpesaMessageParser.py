from TransactionOutcome import TransactionOutcome
from TransactionType import TransactionType
import re
import unicodedata

def parse(message):
  
  """The result will have the fields 'receipt', 'amount', 'name', 'time', 'balance', 'transaction_type', 'transaction_outcome'"""
  """The phone number is only there for certain fields"""
  
  result = {}
  message = message.replace('\\n', '\n')
  
  if message.find("You have received") > 0:
    
    result['transaction_type'] = TransactionType.PAYMENT_RECEIVED
    result['transaction_outcome'] = TransactionOutcome.MONEY_IN
    
    expres = '([A-Z0-9]+) Confirmed\.[\\s\\n]+You have received Ksh([0-9\.\,]+) from[\\s\\n]+([A-Z ]+) ([0-9]+)[\\s\\n]+on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M)[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)'
    temp = re.findall(expres, message)
    print temp
    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][1]
    result['name'] = temp[0][2]
    result['phone'] = temp[0][3]
    result['time'] = temp[0][4]+temp[0][5]
    result['balance'] = temp[0][6]
    
  elif re.match("/sent to .+ for account/", message):
    
    result['transaction_type'] = TransactionType.PAYBILL_PAID
    result['transaction_outcome'] = TransactionOutcome.MONEY_OUT
    
    expr = "([A-Z0-9]+) Confirmed\.[\\s\\n]+Ksh([0-9\.\,]+) sent to[\\s\\n]+(.+)[\\s\\n]+for account (.+)[\\s\\n]+on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M)[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)"
    # Example s = '4R Confirmed.\nKsh3.4 sent to\n203902323\nfor account *0o2c{p.6-8\non 86/3/43 at 03:67 AM\nNew M-PESA balance is Ksh.3.0'
    temp = re.findall(expr, message)
     
    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][1]
    result['name'] = temp[0][2]
    result['phone'] = temp[0][3]
    result['time'] = temp[0][4]+temp[0][5]
    result['balance'] = temp[0][6]
  
  elif re.match("/Ksh[0-9\.\,]+ paid to /", message):

    result['transaction_type'] = TransactionType.BUY_GOODS
    result['transaction_outcome'] = TransactionOutcome.MONEY_OUT

    expr = "([A-Z0-9]+) Confirmed\.[\\s\\n]+Ksh([0-9\.\,]+) paid to[\\s\\n]+([.]+)[\\s\\n]+on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M)[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)"

    temp = re.findall(expr, message)

    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][1]
    result['name'] = temp[0][2]
    result['time'] = temp[0][3]+temp[0][4]
    result['balance'] = temp[0][5]
    
  
  elif re.match("/sent to .+ on/", message):
    expr = "/([A-Z0-9]+) Confirmed\.[\\s\\n]+Ksh([0-9\.\,]+) sent to ([A-Z ]+) ([0-9]+) on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M)[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)"

    result['transaction_type'] = TransactionType.PAYMENT_SENT
    result['transaction_outcome'] = TransactionOutcome.MONEY_OUT

    temp = re.findall(expr, message)

    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][1]
    result['name'] = temp[0][2]
    result['phone'] = temp[0][3]
    result['time'] = temp[0][4]+temp[0][5]
    result['balance'] = temp[0][6]
    
    
  elif re.match("/Give Ksh[0-9\.\,]+ cash to/", message):
    expr = "/([A-Z0-9]+) Confirmed\.[\\s\\n]+on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M)[\\s\\n]+Give Ksh([0-9\.\,]+) cash to (.+)[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)"

    result['transaction_type'] = TransactionType.DEPOSIT
    result['transaction_outcome'] = TransactionOutcome.MONEY_IN

    temp = re.findall(expr, message)

    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][3]
    result['name'] = temp[0][4]
    result['time'] = temp[0][1]+temp[0][2]
    result['balance'] = temp[0][5]
    
  elif re.match("/Withdraw Ksh[0-9\.\,]+ from/", message):
    expr = "/([A-Z0-9]+) Confirmed\.[\\s\\n]+on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M)[\\s\\n]+Withdraw Ksh([0-9\.\,]+) from (.+)[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)"
    
    result['transaction_type'] = TransactionType.WITHDRAW
    result['transaction_outcome'] = TransactionOutcome.MONEY_OUT
    
    temp = re.findall(expr, message)
    
    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][3]
    result['name'] = temp[0][4]
    result['time'] = temp[0][1]+temp[0][2]
    result['balance'] = temp[0][5]
    
  elif re.match("/Ksh[0-9\.\,]+ withdrawn from/", message):
    
    result['transaction_type'] = TransactionType.WITHDRAW_ATM
    result['transaction_outcome'] = TransactionOutcome.MONEY_OUT
    
    expr = "/([A-Z0-9]+) Confirmed[\\s\\n]+on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M).[\\s\\n]+Ksh([0-9\.\,]+) withdrawn from (\d+) - AGENT ATM\.[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)"
    
    temp = re.findall(expr, message)
    
    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][3]
    result['name'] = temp[0][4]
    result['time'] = temp[0][1]+temp[0][2]
    result['balance'] = temp[0][5]
    
    
  elif re.match("/You bought Ksh[0-9\.\,]+ of airtime on/",message):
    result['transaction_type'] = TransactionType.AIRTIME_YOU
    result['transaction_outcome'] = TransactionOutcome.MONEY_OUT
    expr = "/([A-Z0-9]+) confirmed\.[\\s\\n]+You bought Ksh([0-9\.\,]+) of airtime on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M)[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)"
    temp = re.findall(expr, message)
    
    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][1]
    result['name'] = "Safaricom"
    result['time'] = temp[0][2]+temp[0][3]
    result['balance'] = temp[0][4]
    
  elif re.match("/You bought Ksh[0-9\.\,]+ of airtime for (\d+) on/", message):
    
    result['transaction_type'] = TransactionType.AIRTIME_OTHER
    result['transaction_outcome'] = TransactionOutcome.MONEY_OUT
    
    expr = "/([A-Z0-9]+) confirmed\.[\\s\\n]+You bought Ksh([0-9\.\,]+) of airtime for (\d+) on (\d\d?\/\d\d?\/\d\d) at (\d\d?:\d\d [AP]M)[\\s\\n]+New M-PESA balance is Ksh([0-9\.\,]+)(?:...)"
    temp = re.findall(expr, message)
    
    result['receipt'] = temp[0][0]
    result['amount'] = temp[0][1]
    result['name'] = temp[0][2]
    result['time'] = temp[0][3]+temp[0][4]
    result['balance'] = temp[0][5]
  else:
    result['transaction_type'] = TransactionType.UNKNOWN
    result['transaction_outcome'] = TransactionOutcome.NEUTRAL
  print result
  return result
      
if __name__ == "__main__":
  parse("DT123FR3 Confirmed.\nYou have received Ksh20.00 from\nX KHAN 254713223757\non 26/7/13 at 3:10 PM\nNew M-PESA balance is Ksh24.00.Save & get a loan on Mshwari")