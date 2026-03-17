def p(d,t):
 r=[]
 for i in d:
  if t=="a":
   if i["b"]>1000 and i["s"]=="active":
    x=i["b"]*0.05
    if i["ty"]=="premium":
     x=i["b"]*0.08
    i["b"]=i["b"]+x
    r.append(i)
  elif t=="b":
   if i["b"]<0:
    print(f"WARNING: {i['n']} has negative balance: {i['b']}")
    i["f"]=True
    r.append(i)
  elif t=="c":
   total=0
   for j in i["tr"]:
    if j["type"]=="credit":
     total+=j["amount"]
    elif j["type"]=="debit":
     total-=j["amount"]
   i["calc_balance"]=total
   if abs(total-i["b"])>0.01:
    i["discrepancy"]=True
    r.append(i)
 return r

def gen_rep(accounts,start,end):
 res={"total_accounts":0,"total_balance":0,"premium":0,"standard":0,"flagged":0,"avg":0}
 fl=[]
 for a in accounts:
  if a.get("created"):
   from datetime import datetime
   d=datetime.strptime(a["created"],"%Y-%m-%d")
   if d>=datetime.strptime(start,"%Y-%m-%d") and d<=datetime.strptime(end,"%Y-%m-%d"):
    res["total_accounts"]+=1
    res["total_balance"]+=a["b"]
    if a["ty"]=="premium":res["premium"]+=1
    else:res["standard"]+=1
    if a.get("f"):res["flagged"]+=1;fl.append(a["n"])
 if res["total_accounts"]>0:res["avg"]=res["total_balance"]/res["total_accounts"]
 res["flagged_names"]=fl
 return res

def val(email,phone,date):
 import re
 errors=[]
 if not re.match(r"[^@]+@[^@]+\.[^@]+",email):errors.append("bad email")
 if not re.match(r"^\+?[0-9]{10,15}$",phone):errors.append("bad phone")
 try:
  from datetime import datetime
  datetime.strptime(date,"%Y-%m-%d")
 except:errors.append("bad date")
 if len(errors)>0:return False,errors
 return True,[]

DATA=[
 {"n":"Eli","b":5000,"s":"active","ty":"premium","f":False,"created":"2025-01-15","tr":[{"type":"credit","amount":5000},{"type":"debit","amount":200}]},
 {"n":"Leyla","b":1200,"s":"active","ty":"standard","f":False,"created":"2025-03-20","tr":[{"type":"credit","amount":1500},{"type":"debit","amount":300}]},
 {"n":"Tural","b":-50,"s":"active","ty":"standard","f":False,"created":"2025-06-10","tr":[{"type":"credit","amount":100},{"type":"debit","amount":150}]},
 {"n":"Nigar","b":8500,"s":"inactive","ty":"premium","f":False,"created":"2025-02-28","tr":[{"type":"credit","amount":9000},{"type":"debit","amount":500}]},
 {"n":"Rashad","b":3200,"s":"active","ty":"premium","f":False,"created":"2025-08-05","tr":[{"type":"credit","amount":3000},{"type":"debit","amount":100}]},
]
