# JPG as Key [300 pts]

8-11-2020 :: T0062 - CUHK
Solved on November 7th, 11:52:37 PM

```
Author 作者：blackb6a

Description 描述：

The flag is hide in the jpg. Can you get it?

旗藏相片中。你明白嗎？
```
![left_exit.jpg](https://www.dropbox.com/s/635rgfekwme4st5/left_exit.jpg?dl=0&raw=1)
## Solution
First step of the tasks is to see if any files are hidden in the JPG. Using `binwalk` before stepping further helps most of the time.
```
$ binwalk left_exit.jpg

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
51405         0xC8CD          Zip archive data, encrypted at least v2.0 to extract, compressed size: 3007, uncompressed size: 3048, name: flag.png
54450         0xD4B2          Zip archive data, encrypted at least v2.0 to extract, compressed size: 51376, uncompressed size: 51405, name: left_exit.jpg
106054        0x19E46         End of Zip archive, footer length: 22
```
There was a zip file hidden, lets extract just the original image which would be useful later in the task and also the zip by using `foremost left_exit.jpg`, the image only part is at `./output/jpg/00000000.jpg` and the zip is at `./output/zip/00000100.zip`.

Looking inside the zip, we can see another `left_exit.jpg` and our desired `flag.png` but they are password encrypted.

If we attempt to brute force for the password, it is possible we could never find one so this suggest there may be other solutions.

Notice that the `left_exit.jpg` has the same CRC32 value as the `00000000.jpg` from `foremost` which is `803598ED`, this suggests they are indeed the same image and the zip is opened to a **"Known Plaintext Attack"**.

`pkcrack` from https://github.com/keyunluo/pkcrack is the tool used for the attack which supports both Linux and Windows platform. We put our `00000000.jpg` into a zip called `un.zip`, put the `00000100.zip` in the same directory and launch the attack by 
`pkcrack -C 00000100.zip -c left_exit.jpg -P un.zip -p 00000000.jpg -d flag.zip -a`

After waiting for a while, 

```
Files read. Starting stage 1 on Sun Nov  8 21:24:29 2020
Generating 1st generation of possible key2_51375 values...done.
Found 4194304 possible key2-values.
Now we're trying to reduce these...
Lowest number: 910 values at offset 46648
Lowest number: 888 values at offset 46644
<---cliped--->
Lowest number: 232 values at offset 45925
Done. Left with 232 possible Values. bestOffset is 45925.
Stage 1 completed. Starting stage 2 on Sun Nov  8 21:25:29 2020
Ta-daaaaa! key0=3e96cca9, key1=6c2a40c9, key2=7c4d40e4
Probabilistic test succeeded for 5455 bytes.
Strange... had a false hit.
Strange... had a false hit.
Stage 2 completed. Starting zipdecrypt on Sun Nov  8 21:25:33 2020
Decrypting flag.png (b9f713ff662c9f0bef514404)... OK!
Decrypting left_exit.jpg (f76a749f3370d11ff9288b80)... OK!
Finished on Sun Nov  8 21:25:33 2020
```

We obtained the unencrypted zip as `flag.zip`, open up the `flag.png` inside we get a QR code.
![flag.png](https://www.dropbox.com/s/dij5cv7zyr6a5xk/flag.png?dl=0&raw=1)

Decoding it directly gives us the flag.
```
flag: hkcert20{n0w_y0u_can_crack_z1p}
```
