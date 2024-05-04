import yfinance as yf

msft = yf.Ticker("MSFT")

# get all stock info
msft.info

# get historical market data
hist = msft.history(period="1mo")
# print(hist)

# # show meta information about the history (requires history() to be called first)
# print(msft.history_metadata)

# # show actions (dividends, splits, capital gains)
# msft.actions
# msft.dividends
# msft.splits
# msft.capital_gains  # only for mutual funds & etfs

# # show share count
# msft.get_shares_full(start="2022-01-01", end=None)

# show financials:
# - income statement
# print(msft.income_stmt)
# msft.quarterly_income_stmt
# - balance sheet
# print(msft.balance_sheet)
# msft.quarterly_balance_sheet
# - cash flow statement
print(msft.cashflow)
# msft.quarterly_cashflow
# see `Ticker.get_income_stmt()` for more options