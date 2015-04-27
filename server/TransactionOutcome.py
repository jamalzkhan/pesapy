import enum

TransactionOutcome = enum.enum(
  "MONEY_OUT",
  "MONEY_IN",
  "NEUTRAL")