How to use

Edit field "mac": "PASTE_YOUR_MAC_HERE", in config.json

    "interval": 2700000, #ms

    "timezone": 2, #UTC
    
    "ssh": {       #gateway
        "host": "192.168.0.1",
 
        "port": 22,
     
        "user": "root",
        
        "passwd": "password"
    },
    
    "subnets": [
    "192.168.0.1",
    "192.168.1.0"
    ], #empty [] or 192.168.2.0 etc
    
    "devices": [

How to run

pip3 install --upgrade pip

nohup python3 main.py --config config.json --ssh &

