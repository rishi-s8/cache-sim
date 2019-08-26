# Cache Simulator

This repository contains a python-based simulator for cache memory. The addresses in ```address.txt``` are to be fetched from main memory. The tool supports different ```cache size```, ```block size```, ```mapping functions``` and ```replacement policies```.

```cache-data.py``` emulates copying the whole data into the memory along with hits and misses.
```cache-no-data.py``` emulates only hits and misses and doesn't copy the whole data into the memory.
This is done to throw light on the time taken to copy the blocks.

This was developed as part of the CS-201P Computer Organization Lab.