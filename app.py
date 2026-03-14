# ---------- ADVANCED DATASET ----------

family_name = "Sharma Family"

wallet_balance = 45230

members = [
{"name":"Rajesh","role":"Admin","limit":10000,"spent":7450,"balance":12000},
{"name":"Priya","role":"Spouse","limit":8000,"spent":5120,"balance":9000},
{"name":"Aryan","role":"Teen","limit":3000,"spent":2100,"balance":1800},
{"name":"Neha","role":"Child","limit":1500,"spent":900,"balance":700},
{"name":"Dadaji","role":"Elder","limit":4000,"spent":650,"balance":3500}
]

transactions = pd.DataFrame({

"Member":[
"Aryan","Aryan","Aryan","Priya","Priya","Priya","Rajesh","Rajesh","Rajesh","Neha",
"Neha","Neha","Dadaji","Dadaji","Dadaji","Aryan","Priya","Rajesh","Priya","Aryan",
"Rajesh","Priya","Aryan","Neha","Dadaji","Priya","Aryan","Rajesh","Priya","Aryan",
"Rajesh","Priya","Aryan","Neha","Dadaji","Aryan","Priya","Rajesh","Neha","Aryan",
"Rajesh","Priya","Aryan","Priya","Rajesh","Aryan","Neha","Dadaji","Priya","Aryan"
],

"Merchant":[
"Swiggy","Dominos","Zomato","Big Bazaar","Amazon","Flipkart","KSRTC","IRCTC","Uber","Apollo Pharmacy",
"Stationery Shop","Book Store","Medical Store","Apollo Pharmacy","Pharmacy Plus","Metro","Reliance Smart","Petrol Pump","Myntra","Swiggy",
"IRCTC","Amazon","Zomato","School Canteen","Medical Store","Big Bazaar","Uber","KSRTC","Flipkart","Dominos",
"Petrol Pump","Reliance Smart","Metro","Stationery Shop","Pharmacy Plus","Swiggy","Amazon","IRCTC","Book Store","Dominos",
"Uber","Big Bazaar","Zomato","Myntra","Petrol Pump","Swiggy","Stationery Shop","Medical Store","Flipkart","Zomato"
],

"Category":[
"Food","Food","Food","Shopping","Shopping","Shopping","Transport","Transport","Transport","Medical",
"Education","Education","Medical","Medical","Medical","Transport","Groceries","Transport","Shopping","Food",
"Transport","Shopping","Food","Food","Medical","Groceries","Transport","Transport","Shopping","Food",
"Transport","Groceries","Transport","Education","Medical","Food","Shopping","Transport","Education","Food",
"Transport","Groceries","Food","Shopping","Transport","Food","Education","Medical","Shopping","Food"
],

"Amount":[
250,420,310,1240,2200,1750,540,900,320,120,
220,450,500,300,1800,350,650,1500,1200,275,
700,1800,390,150,340,850,460,600,1350,290,
1100,730,410,210,1500,260,2000,780,340,310,
450,920,340,1400,1300,280,190,2000,1200,330
]

})
