from tkinter import *
master = Tk()
master.title('Coinjar Exchange')

import json
import requests
import urllib
from urllib.request import Request, urlopen
import time
from functools import partial

refresh = 3
invest = 1
def_percent = 10
token = ""
def readsettings():
	global refresh, invest, def_percent, token
	with open('cjsettings.txt') as json_file:  
		data = json.load(json_file)[0]
		refresh = data['refresh']
		invest = data['invest']
		def_percent = data['def_percent']
		token = data['token']


def writesettings():
	data = []
	data.append({
		'refresh':refresh,
		'invest':invest,
		'def_percent':def_percent,
		'token':token
		})
	with open('cjsettings.txt', 'w') as outfile:  
		json.dump(data, outfile)

try:
	readsettings()
except:
	writesettings()

if token == "":
	print ("No token found")
	exit()

headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Token token=%s' % token}

accounts = json.loads(urlopen(Request('https://api.exchange.coinjar.com/accounts', headers=headers)).read().decode('utf-8'))
products = json.loads(urlopen(Request('https://api.exchange.coinjar.com/products', headers=headers)).read().decode('utf-8'))
orders = json.loads(urlopen(Request('https://api.exchange.coinjar.com/orders/all?', headers=headers)).read().decode('utf-8'))


combos = []

for i in range(len(products)):
	combos.append(products[i]['id'])
spacer = range(len(products))[::6]
spacerb = range(len(products)+2)[0::8]


def update_invest():
	global invest
	invest = i1.get()
	print(invest)
	i1.delete(0,END)
	i1.insert(5, invest)
	writesettings()

def update_box():
	for t in range(4):
		LASTORDER = orders[t]['timestamp'], orders[t]['side'], orders[t]['product_id'], orders[t]['size'], orders[t]['price'], orders[t]['status']
		TEXTBOX.insert(END, LASTORDER)
		TEXTBOX.insert(END, '\n')

def popupmsg(FUNDS, DENOM):
    popup = Tk()
    popup.title("Error")
    Label(popup, text="NOT ENOUGH FUNDS").grid(row=0)
    sub = DENOM[:-3]; blah = "Requires minimum: %s %s" % (FUNDS, sub)
    Label(popup, text=blah).grid(row=1)
    Button(popup, text='OK', command=popup.destroy).grid(row=2, sticky=W, pady=4)
    popup.mainloop()

def buyproduct(X):
	for Z in range(len(products[X]['price_levels'])):
		if float(products[X]['price_levels'][Z]['price_min']) < float(lastask[X]) and float(products[X]['price_levels'][Z]['price_max']) > float(lastask[X]):
			tradesize = float(products[X]['price_levels'][Z]['trade_size'])
	if tradesize <= float(buy1[X].get())/float(lastask[X]):
		#print combos[X], lastask[X], float(buy1[X].get())/float(lastask[X])
		values = {"product_id": combos[X], "type": "LMT", "side": "buy", "price": str(float(lastask[X])), "size": str(float(buy1[X].get())/float(lastask[X])), "time_in_force": "GTC"}
		r = requests.post('https://api.exchange.coinjar.com/orders', data=json.dumps(values), headers=headers)
		if r.status_code == 200:
			print("Transaction OK")
		else:
			print("Some bogus error", r.reason)
			print(values)
		#print r.status_code, r.reason
	else:
		popupmsg(tradesize, combos[X])

def sellproduct(X):
	for Z in range(len(products[X]['price_levels'])):
		if float(products[X]['price_levels'][Z]['price_min']) < float(lastask[X]) and float(products[X]['price_levels'][Z]['price_max']) > float(lastask[X]):
			tradesize = float(products[X]['price_levels'][Z]['trade_size'])
	if tradesize <= float(sell1[X].get())/float(lastbid[X]):
		#print combos[X], lastask[X], float(buy1[X].get())/float(lastask[X])
		values = {"product_id": combos[X], "type": "LMT", "side": "sell", "price": str(float(lastbid[X])), "size": str(float(sell1[X].get())/float(lastbid[X])), "time_in_force": "GTC"}
		r = requests.post('https://api.exchange.coinjar.com/orders', data=json.dumps(values), headers=headers)
		if r.status_code == 200:
			print("Transaction OK")
		else:
			print("Some bogus error", r.reason)
			print(values)
		#print r.status_code, r.reason
	else:
		popupmsg(tradesize, combos[X])


e1 = Entry(master)
e1.insert(5, refresh)
e1.grid(row=0, column=1)
Label(master, text="Refresh rate:").grid(row=0)

Label(master, text="Default Trade:").grid(row=0, column=2)
p1 = Entry(master)
p1.insert(5, def_percent)
p1.grid(row=0, column=3)

i1 = Entry(master)
i1.insert(5, invest)
i1.grid(row=142, column=3)
Label(master, text="Invested:").grid(row=142, column=2)
Label(master, text="Profit:").grid(row=143, column=2)
Button(master, text='update', command=update_invest).grid(row=142, column=4, sticky=W, pady=4)



#non refresh text
Label(master, text="Prices:", font='bold').grid(row=1)
Label(master, text="Accounts:", font='bold').grid(row=113)
Label(master, text="Account Name", font='bold').grid(row=114); Label(master, text="Currency", font='bold').grid(row=114, column=1); Label(master, text="Amount", font='bold').grid(row=114, column=2); Label(master, text="Value", font='bold').grid(row=114, column=3)

amount = []
amounttext = []
value0 = []
valuetext0 = []
for i in range(len(accounts)):
	Label(master, text=accounts[i]['number']).grid(row=(i+120)); Label(master, text=accounts[i]['asset_code']).grid(row=(i+120), column=1)
	amounttext.append(StringVar())
	amount.append(Label(master, textvariable=amounttext[i]).grid(row=(i+120), column=2))
	valuetext0.append(StringVar())
	value0.append(Label(master, textvariable=valuetext0[i]).grid(row=(i+120), column=3))
portfoliotext = StringVar(); profittext = StringVar()
Label(master, textvariable=portfoliotext).grid(row=140, column=3)
Label(master, textvariable=profittext, font='bold').grid(row=143, column=3)

for U in spacerb:
	Label(master, text='ASK').grid(row=2+U)
	Label(master, text='BID').grid(row=3+U)
	Label(master, text='Trade Percent').grid(row=4+U)
lastbid = [0 for i in range(len(combos))]; lastask = [0 for i in range(len(combos))]
s_combo = [IntVar(value=1) for i in range(len(combos))]
buy1 = [Entry(master) for i in range(len(combos))]
sell1 = [Entry(master) for i in range(len(combos))]
t1 = [Entry(master) for i in range(len(combos))]

ask0 = []
asktext0 = []
bid0 = []
bidtext0 = []
for j in range(len(combos)):
	spacerrow = 0
	for k in range(len(spacer)):
		if j >= spacer[k]:
			spacerrow = spacerb[k]
			spacercol = spacer[k]
	asktext0.append(StringVar()); ploy = Label(master, textvariable=asktext0[j]); ploy.grid(row=2+spacerrow, column=j+1-spacercol); ploy.config(fg='black'); ask0.append(ploy)
	bidtext0.append(StringVar()); ploy = Label(master, textvariable=bidtext0[j]); ploy.grid(row=3+spacerrow, column=j+1-spacercol); ploy.config(fg='black'); bid0.append(ploy)
	Checkbutton(master, text=combos[j], variable=s_combo[j]).grid(row=1+spacerrow, column=j+1-spacercol)
	t1[j].insert(5, def_percent)
	t1[j].grid(row=4+spacerrow, column=j+1-spacercol)
	Button(master, text='Buy', command=partial(buyproduct, j)).grid(row=5+spacerrow, column=j+1-spacercol, sticky=W, pady=4)
	buy1[j].grid(row=6+spacerrow, column=j+1-spacercol)
	sell1[j].grid(row=8+spacerrow, column=j+1-spacercol)
	Button(master, text='Sell', command=partial(sellproduct, j)).grid(row=7+spacerrow, column=j+1-spacercol, sticky=W, pady=4)


Label(master, text='Portfolio:').grid(row=140, column=2)

TEXTBOX = Text(master, height=4)
TEXTBOX.grid(row=200, columnspan=20, sticky=W)
update_box()

#refreshed info
def update_price():
	global invest, lastbid, lastask, s_combo, AT
	try:
		accounts = json.loads(urlopen(Request('https://api.exchange.coinjar.com/accounts', headers=headers)).read().decode('utf-8'))
		orders = json.loads(urlopen(Request('https://api.exchange.coinjar.com/orders/all?', headers=headers)).read().decode('utf-8'))
	except:
		time.sleep(10)
		pass

	#Show prices
	for j in range(len(combos)):
		spacerrow = 0
		spacercol = 0
		for k in range(len(spacer)):
			if j >= spacer[k]:
				spacerrow = spacerb[k]
				spacercol = spacer[k]
			#ASSET2 = accounts[j]['asset_code']
		url = "https://data.exchange.coinjar.com/products/%s/ticker" % combos[j]
		#print(json.loads(urlopen(Request(url)).read().decode('utf-8')))
		try:
			b = json.loads(urlopen(Request(url)).read().decode('utf-8'))
		except:
			time.sleep(10)
			pass
		if float(b['ask']) > lastask[j] and lastask[j] !=0:
			ask0[j].config(fg='green')
		if float(b['ask']) < lastask[j] and lastask[j] !=0:
			ask0[j].config(fg='red')
		if float(b['bid']) > lastbid[j] and lastbid[j] !=0:
			bid0[j].config(fg='green')
		if float(b['bid']) < lastbid[j] and lastbid[j] !=0:
			bid0[j].config(fg='red')
		lastask[j]=float(b['ask']); lastbid[j]=float(b['bid']); asktext0[j].set(b['ask']); bidtext0[j].set(b['bid'])

		for t in range(len(accounts)):
			if accounts[t]['asset_code'] == str(combos[j][-3:]):
				supply = accounts[t]['settled_balance']
		buy_percent = round(float(supply)*((float(t1[j].get())/100)), 8)
		buy1[j].delete(0,END)
		buy1[j].insert(5, buy_percent)
		for t in range(len(accounts)):
			if accounts[t]['asset_code'] == str(combos[j][:3]):
				supply = accounts[t]['settled_balance']
		sell_percent = round(float(supply)*((float(t1[j].get())/100))*float(b['bid']), 8)
		sell1[j].delete(0,END)	
		sell1[j].insert(5, sell_percent)

	#Show accounts
	portfolio = 0
	for i in range(len(accounts)):
		ASSET = accounts[i]['asset_code']
		if ASSET != 'AUD':
			url = "https://data.exchange.coinjar.com/products/%sAUD/ticker" % ASSET
			try:
				b= json.loads(urlopen(Request(url)).read().decode('utf-8'))
			except:
				time.sleep(10)
				pass
			CURPRICE = float(b['bid'])*float(accounts[i]['settled_balance'])
		else:
			CURPRICE = accounts[i]['settled_balance']
		portfolio = portfolio+float(CURPRICE)
		amounttext[i].set(accounts[i]['settled_balance']); valuetext0[i].set(round(float(CURPRICE), 2))
	portfoliotext.set(round(portfolio, 2)); profittext.set(round(portfolio-float(invest), 2))
	TEXTBOX.delete(END, END)
	update_box()
	master.after((refresh*1000), update_price)




if __name__ == '__main__':
	update_price()
Button(master, text='Quit', command=master.destroy).grid(row=0, column=6, sticky=W, pady=4)
mainloop()