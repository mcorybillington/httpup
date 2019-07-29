# httpup

httpup is a fast, lightweight port scanner designed for quickly determining if a machine is up or down. It runs 
optimally with a few key ports selected, and can be tuned by tweaking the timeout setting. It doesn't use any packages
outside of the python standard library. I wrote this to aid in checking to see if machines were up on large scope bug bounties.

### Usage

`python httpup.py [-h] [-p P] [-t T] [--no-error] host`

Ports can be specified as comma separated values, or as a range:  
Ports example for comma separated: `-p 22,80,443,445`  
Ports example for range: `-p 80-90`  

Timeout is in seconds:  
`-t 0.5` will wait for a response for 0.5 seconds  
`--no-error` will simply return a `1` and will not output any error messages.

### Output

Three possible outcomes:  
`0` - Host is up on one of the ports specified  
`1` - Host is down  
`Invalid Host: < host >` - Address resolution failed for the specified host 