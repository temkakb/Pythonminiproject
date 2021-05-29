import json
# import requests
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# headers = {"Content-type": "application/json", "Accept": "text/plain","Authorization":"Token 65ea19f781f704f77f6aa5f4610b4b443ed43068"}
with open("D:\data\data-2.json","r", encoding="utf-8") as data_json:
    importjason = json.load(data_json)

# print(type(data))
# url="https://localhost:9000/machines/6c96136/receive_data/"
# r = requests.post(url, json=data,headers=headers,verify=False)
# print(r.text)
# def rearrange_json(importjason):
def excuteconvert (listkeycheck,oldata,new_lv1_json,listwallet=None):
	if listwallet==None:
		for key in oldata:
				data=oldata[key]
				if type(data) == dict:
					new_lv1_json[key]= {}
				elif key=="wallet_balances":
					continue
				elif type(data) == list:
					new_lv1_json[key]= []
				else:
					new_lv1_json[key]=data


		for key in listkeycheck:
			
				if(key=="wallet_ballances"):
					new_lv1_json[key]=[]
				if key not in new_lv1_json:
					if type(listkeycheck[key])==int:
						new_lv1_json[key]=0
					if type(listkeycheck[key])==str:
						new_lv1_json[key]="No infomation"
					if type(listkeycheck[key])==bool:
						new_lv1_json[key]=False
					if type(listkeycheck[key])==dict:
						new_lv1_json[key]={}
					if type(listkeycheck[key])==list:
						new_lv1_json[key]=[]

	else:
		pass
	return new_lv1_json		


def rearrange_json(importjason):
	newjson = {}
	keycheck_farmstat={
      "farmer_running":True,
      "farmed_amount":0,
      "farmer_reward_amount":0,
      "fee_amount":0,
      "last_height_farmed":0,
      "pool_reward_amount":0,
      "plot_number":0,
      "plots_space_string":"",
      "network_space_string":"",
      "estimated_time_to_win_in_minutes":0
   }
	keycheck_fullnode={"difficulty":0,
      "genesis_challenge_initialized":True,
      "mempool_size":0,
      "space":0,
      "sub_slot_iters":0,
      "sync":{
         "sync_mode":False,
         "sync_progress_height":0,
         "sync_tip_height":0,
         "synced":False
      }
      }
	keycheck_walletsumanry={
      "address_prefix":"",
      "height_info":0,
      "sync_status":False,
      "wallet_ballances":[
         {
            "wallet_id":0,
            "name":"Chia Wallet",
            "type":0,
            "balance":{
               "confirmed_wallet_balance":0,
               "max_send_amount":0,
               "pending_change":0,
               "spendable_balance":0,
               "unconfirmed_wallet_balance":0
            }
         }
      ]
   }
	try:
		farm_stat=importjason["farm_stat"]
	except Exception as es:
		farm_stat=None
	try:
		full_node=importjason["blockchain_state"]
	except Exception as es:
		full_node=None
	try:
		average_block_time=importjason["average_block_time"]
	except Exception as es:
		average_block_time=0
	try:
		wallet_summary=importjason["wallet_summary"]
	except Exception as e:
		wallet_summary=None
	try:
		wallet=importjason["wallet"]
	except Exception as e:
		wallet=None
	if farm_stat:
		# print(farm_stat)
		newjson["farm_stat"]={}
		newjson["farm_stat"]=excuteconvert(listkeycheck=keycheck_farmstat,oldata=farm_stat,new_lv1_json=newjson["farm_stat"])
	
	if full_node:
		newjson["blockchain_state"]={}
		newjson["blockchain_state"]= excuteconvert(listkeycheck=keycheck_fullnode,oldata=full_node,new_lv1_json=newjson["blockchain_state"])

		try:
			oldata=full_node["sync"]
		except Exception as es:
			oldata=None

		if oldata is not None:
			newjson["blockchain_state"]["sync"]=excuteconvert(listkeycheck=keycheck_fullnode["sync"],oldata=oldata,new_lv1_json=newjson["blockchain_state"]["sync"])
	
		
	if average_block_time:
		newjson["average_block_time"]=average_block_time
	else:
		newjson["average_block_time"]=0
	if wallet_summary:
		newjson["wallet_summary"]={}
		newjson["wallet_summary"]=excuteconvert(listkeycheck=keycheck_walletsumanry,oldata=wallet_summary,new_lv1_json=newjson["wallet_summary"])
		try:
			listwallet=wallet_summary["wallet"]
		except Exception as es:
			listwallet=None
		try:
			balances=wallet_summary["wallet_balances"]
		except Exception as es:
			balances=None
		if listwallet and balances is not None: # balance  va wallet deu co 
			for wallet in listwallet:
				for balance in balances:
					if wallet["id"]==balance["wallet_id"]:
						try :
							balance["name"]=wallet["name"] # balance   ko co
						except Exception as e:	
							balance["name"]="No infomation"
						try :
							balance["type"]=wallet["type"]
						except Exception as e:	
							balance["type"]=0
						try :
							balance['balance']=balance['wallet_balance'] # balance   ko co
							del balance['wallet_balance']
						except Exception as e:
							balance['balance']={}

						
						newjson["wallet_summary"]["wallet_ballances"].append(balance)
		else:
			if balances is not None: # balance  co nhung wallet khong co
				for balance in balances:
					balance["name"]="No infomation"
					balance["type"]=0
					try :
						balance['balance']=balance['wallet_balance']  # balance   ko co
					except Exception as e:
						balance['balance']={}
					newjson["wallet_summary"]["wallet_ballances"].append(balance)
					# load blance or default
		
		for i in range(0,len(newjson["wallet_summary"]['wallet_ballances'])):
			newjson["wallet_summary"]['wallet_ballances'][i]['balance']=excuteconvert(listkeycheck=keycheck_walletsumanry['wallet_ballances'][0]['balance'],
				oldata=newjson["wallet_summary"]['wallet_ballances'][i]['balance'],new_lv1_json={}
				)
	print(json.dumps(newjson))
	return(json.dumps(newjson))	
		




rearrange_json(importjason)