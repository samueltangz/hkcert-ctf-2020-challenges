# JPG as Key

## Prologue
Just a normal secondary school trick to hide zip with known plaintext attack.

## Walk-through

### File Extraction
Extract the zip using the command below
```console
$ binwalk ./left_exit.jpg  --dd='.*'

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
51405         0xC8CD          Zip archive data, encrypted at least v2.0 to extract, compressed size: 3007, uncompressed size: 3048, name: flag.png
54450         0xD4B2          Zip archive data, encrypted at least v2.0 to extract, compressed size: 51376, uncompressed size: 51405, name: left_exit.jpg
106054        0x19E46         End of Zip archive, footer length: 22
```

Use the command below will extract the original pic. Otherwise, use 7zip split function.
I'm also seeing team using foremost to extract the pic but it's not necessary. Use binwalk wisely.
```console
$ binwalk ./left_exit.jpg -o 0 -l 51405 --dd='.*'

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
```

Rename `0` as `left_exit.jpg`, and zip it under 7zip. This move is to generate a zip matches the CRC value.

### Plain-text attack
After getting the plain text (`left_exit.jpg`), we can move on to attack stage. `pkzip` or `AZPK` should work.
Here I've use `bkzip`:

```console
$ ./bkcrack -C ~/Desktop/C8CD -c left_exit.jpg -P ~/Desktop/plain-text/left_exit.zip -p left_exit.jpg
Generated 4194304 Z values.
[13:04:10] Z reduction using 51356 bytes of known plaintext
100.0 % (51356 / 51356)
271 values remaining.
[13:04:19] Attack on 271 Z values at index 45903
13.3 % (36 / 271)
[13:04:19] Keys
3e96cca9 6c2a40c9 7c4d40e4 

$ ./bkcrack -C '/home/byronwai/Desktop/C8CD' -c flag.png -k 3e96cca9 6c2a40c9 7c4d40e4 -d ~/Desktop/deflate_flag
Wrote deciphered text.

$ ../tools/inflate.py < ~/Desktop/deflate_flag > ~/Desktop/flag.png
```

The flag is in QR code, scan and get the flag directly.

## Flag
`hkcert20{n0w_y0u_can_crack_z1p}`

## Epilogue
Solve: 11/81 (Tertiary)

There exist competitor(s) saying that ["its stupid to put native file format tricks into challenges"] (https://www.youtube.com/watch?v=VVdmmN0su6E&feature=youtu.be&t=690&ab_channel=LiveOverflow).
Yes, I admit that this chal is stupid but I expect having at least 20 solves.

## Refernce
<https://zhuanlan.zhihu.com/p/129855130>
