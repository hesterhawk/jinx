jinx.py
=============

ROP gadgets finder for GDB

### Usage

```bash
 ~$ gdb something
...
gef➤ source jinx.py
gef➤ jx
____________ Jinx ____________

usage: jx <option> ..
```

### During work

```bash
gef➤ jx mips-tail
+updwtmp found !!!!11111..
['move t9,s1']
['lw ra,36(sp)', 'lw ra,36(sp)']
jr t9
+xdr_callhdr found !!!!11111..						<--------!!!!!
['move t9,s2', 'move t9,s2', 'move t9,s2']
['lw ra,36(sp)', 'lw ra,36(sp)']
jr t9
+xdr_rejected_reply found !!!!11111..
['move t9,s2']
['lw ra,36(sp)', 'lw ra,36(sp)']
jr t9
+xdr_accepted_reply found !!!!11111..
['move t9,s2']
['lw ra,36(sp)', 'lw ra,36(sp)', 'lw ra,36(sp)', 'lw ra,36(sp)']
jr t9
```

### Results

```bash
gef➤ disassemble xdr_callhdr
...
0x77f0af1c <+176>: move t9,s2
0x77f0af20 <+180>: lw ra,36(sp)
0x77f0af24 <+184>: lw s2,32(sp)
0x77f0af28 <+188>: lw s1,28(sp)
0x77f0af2c <+192>: lw s0,24(sp)
0x77f0af30 <+196>: jr t9
...
```

Plugin was inspired by this IDA Plugin [Links](https://github.com/devttys0/ida/tree/master/plugins/mipsrop). Really thank you Craig Heffner.
