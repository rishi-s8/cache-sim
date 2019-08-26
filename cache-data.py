import string
import random 
from time import time

def get_random_byte():
    return random.choice(string.ascii_letters)

class direct:
    def __init__(self, sz, num_blocks):
        self.sz = sz
        self.num_blocks = num_blocks
        self.block_sz = sz//num_blocks
        self.miss_count = 0
        self.tag_memory = [None] * num_blocks
        self.cache = [None] * sz
        self.valid_bit = [False] * num_blocks

    
    def read(self, address):
        address = int(address, 16)
        main_memory_block = address // self.block_sz
        offset = address % self.block_sz
        block_no = main_memory_block % self.num_blocks
        if self.tag_memory[block_no] != main_memory_block or self.valid_bit[block_no] == False:
            self.miss_count += 1
            self.valid_bit[block_no] = True
            self.tag_memory[block_no] = main_memory_block
            for i in range(self.block_sz):
                self.cache[block_no * self.block_sz + i] = get_random_byte()
        return self.cache[block_no * self.block_sz + offset]


class set_associative:
    def __init__(self, sz, num_blocks):
        self.sz = sz
        self.num_blocks = num_blocks
        self.block_sz = sz//num_blocks
        self.blocks_per_set = 4
        self.set_count = self.num_blocks // self.blocks_per_set
        self.tag_memory = [[None for i in range(self.blocks_per_set)] for j in range(self.set_count)]
        self.cache = [[None for i in range(self.blocks_per_set * self.block_sz)] for j in range(self.set_count)]
        self.valid_bit = [[False for i in range(self.blocks_per_set)] for j in range(self.set_count)]
        self.counter = [[None for i in range(self.blocks_per_set)] for j in range(self.set_count)]
        self.miss_count = 0

    def read_fifo(self, address):
        address = int(address, 16)
        main_memory_block = address // self.block_sz
        set_no =  main_memory_block % self.set_count
        offset = address % self.block_sz

        found_empty = False
        empty_block = None

        for j in range(self.blocks_per_set):
            if self.valid_bit[set_no][j] == True and self.tag_memory[set_no][j] == main_memory_block:
                return self.cache[set_no][j*self.block_sz+offset]
            elif self.valid_bit[set_no][j] == False and found_empty == False:
                found_empty = True
                empty_block = j
        
        self.miss_count += 1

        if found_empty:
            for k in range(self.blocks_per_set):
                if self.valid_bit[set_no][k] == True:
                    self.counter[set_no][k]+=1
            self.counter[set_no][empty_block] = 0
            self.valid_bit[set_no][empty_block] = True
            self.tag_memory[set_no][empty_block] = main_memory_block
            for i in range(self.block_sz):
                self.cache[set_no][empty_block * self.block_sz + i] = get_random_byte()
            return self.cache[set_no][empty_block * self.block_sz + offset]
        
        else:
            fifo_block = 0
            for i in range(self.blocks_per_set):
                if self.counter[set_no][i] > self.counter[set_no][fifo_block]:
                    fifo_block = i

            for k in range(self.blocks_per_set):
                if self.valid_bit[set_no][k] == True:
                    self.counter[set_no][k]+=1

            self.counter[set_no][fifo_block] = 0
            self.tag_memory[set_no][fifo_block] = main_memory_block
            
            for i in range(self.block_sz):
                self.cache[set_no][fifo_block * self.block_sz + i] = get_random_byte()
            return self.cache[set_no][fifo_block * self.block_sz + offset]


    def read_lru(self, address):
        address = int(address, 16)
        main_memory_block = address // self.block_sz
        set_no =  main_memory_block % self.set_count

        found_empty = False
        empty_block = None
        offset = address % self.block_sz

        for j in range(self.blocks_per_set):
            if self.valid_bit[set_no][j] == True and self.tag_memory[set_no][j] == main_memory_block:
                for k in range(self.blocks_per_set):
                    if self.valid_bit[set_no][k] == True:
                        self.counter[set_no][k]+=1
                self.counter[set_no][j] = 0
                return self.cache[set_no][j*self.block_sz+offset]
            elif self.valid_bit[set_no][j] == False and found_empty == False:
                found_empty = True
                empty_block = j
        
        self.miss_count += 1

        if found_empty:
            for k in range(self.blocks_per_set):
                if self.valid_bit[set_no][k] == True:
                    self.counter[set_no][k]+=1
            self.counter[set_no][empty_block] = 0
            self.valid_bit[set_no][empty_block] = True
            self.tag_memory[set_no][empty_block] = main_memory_block
            for i in range(self.block_sz):
                self.cache[set_no][empty_block * self.block_sz + i] = get_random_byte()
            return self.cache[set_no][empty_block * self.block_sz + offset]
        
        else:
            lru_block = 0
            for i in range(self.blocks_per_set):
                if self.counter[set_no][i] > self.counter[set_no][lru_block]:
                    lru_block = i

            for k in range(self.blocks_per_set):
                if self.valid_bit[set_no][k] == True:
                    self.counter[set_no][k]+=1
            self.counter[set_no][lru_block] = 0
            self.tag_memory[set_no][lru_block] = main_memory_block
            for i in range(self.block_sz):
                self.cache[set_no][lru_block * self.block_sz + i] = get_random_byte()
            return self.cache[set_no][lru_block * self.block_sz + offset]



if __name__ == "__main__":
    f = open("address.txt", 'r')
    addresses = f.readlines()
    f.close()
    ans = {'direct':{1024:{16:None, 32:None}, 2048:{16:None, 32:None}, 4096: {16:None, 32:None}, 8192:{16:None, 32:None}}, 'set_associative': {1024:{16:{'lru':None, 'fifo': None}, 32:{'lru':None, 'fifo': None}}, 2048:{16:{'lru':None, 'fifo': None}, 32:{'lru':None, 'fifo': None}}, 4096: {16:{'lru':None, 'fifo': None}, 32:{'lru':None, 'fifo': None}}, 8192:{16:{'lru':None, 'fifo': None}, 32:{'lru':None, 'fifo': None}}}}
    sizes  = [1024, 2048, 4096, 8192]
    block_sizes = [16,32]
    tic = time()
    for block_size in block_sizes:
        for sz in sizes:
            num_blocks = sz//block_size
            
            L1 = direct(sz, num_blocks)
            read_count = 0
            for i in addresses:
                L1.read(i)
                read_count += 1
            print("Cache Size: {}, Block Size: {}, Block Count: {}, Miss ratio = {}/{}".format(sz, block_size, num_blocks, L1.miss_count,read_count))
            ans['direct'][sz][block_size] = "{}/{}".format(L1.miss_count, read_count)
            
            L2 = set_associative(sz, num_blocks)
            read_count = 0
            for i in addresses:
                L2.read_fifo(i)
                read_count += 1
            print("Cache Size: {}, Block Size: {}, Block Count: {}, Miss ratio = {}/{}".format(sz, block_size, num_blocks, L2.miss_count,read_count))
            ans['set_associative'][sz][block_size]['fifo'] = "{}/{}".format(L2.miss_count, read_count)

            L3 = set_associative(sz, num_blocks)
            read_count = 0
            for i in addresses:
                L3.read_lru(i)
                read_count += 1
            print("Cache Size: {}, Block Size: {}, Block Count: {}, Miss ratio = {}/{}".format(sz, block_size, num_blocks, L3.miss_count,read_count))
            ans['set_associative'][sz][block_size]['lru'] = "{}/{}".format(L3.miss_count, read_count)

    print("\nBlock Size: 16 Bytes")
    print("-"*145)
    print("|{:>79}|{:>63}|".format("Direct mapping", "4-way set associative"))
    print("-"*145)
    print("|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format("Cache Size", 1024, 2048, 4096, 8192, 1024, 2048, 4096, 8192))
    print("-"*145)
    print("|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format("LRU", ans['direct'][1024][16], ans['direct'][2048][16], ans['direct'][4096][16], ans['direct'][8192][16], ans['set_associative'][1024][16]['lru'], ans['set_associative'][2048][16]['lru'], ans['set_associative'][4096][16]['lru'], ans['set_associative'][8192][16]['lru']))
    print("|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format("FIFO", ans['direct'][1024][16], ans['direct'][2048][16], ans['direct'][4096][16], ans['direct'][8192][16], ans['set_associative'][1024][16]['fifo'], ans['set_associative'][2048][16]['fifo'], ans['set_associative'][4096][16]['fifo'], ans['set_associative'][8192][16]['fifo']))
    print("-"*145)
    print("\nBlock Size: 32 Bytes")
    print("-"*145)
    print("|{:>79}|{:>63}|".format("Direct mapping", "4-way set associative"))
    print("-"*145)
    print("|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format("Cache Size", 1024, 2048, 4096, 8192, 1024, 2048, 4096, 8192))
    print("-"*145)
    print("|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format("LRU", ans['direct'][1024][32], ans['direct'][2048][32], ans['direct'][4096][32], ans['direct'][8192][32], ans['set_associative'][1024][32]['lru'], ans['set_associative'][2048][32]['lru'], ans['set_associative'][4096][32]['lru'], ans['set_associative'][8192][32]['lru']))
    print("|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|{:>15}|".format("FIFO", ans['direct'][1024][32], ans['direct'][2048][32], ans['direct'][4096][32], ans['direct'][8192][32], ans['set_associative'][1024][32]['fifo'], ans['set_associative'][2048][32]['fifo'], ans['set_associative'][4096][32]['fifo'], ans['set_associative'][8192][32]['fifo']))
    print("-"*145)
    
    print("Time: {}".format(time()-tic))