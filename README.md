How to use
"interval": 2700000, #ms
<br>
    "timezone": 2, #UTC
    </br>
    <br>
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
python3 main.py --config config.json --ssh
