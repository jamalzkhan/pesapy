import enum

TransactionType = enum.enum(
  "PAYMENT_RECEIVED",
  "PAYMENT_SENT",
  "DEPOSIT",
  "WITHDRAW",
  "WITHDRAW_ATM",
  "PAYBILL_PAID",
  "BUY_GOODS",
  "AIRTIME_YOU",
  "AIRTIME_OTHER",
  "UNKNOWN")