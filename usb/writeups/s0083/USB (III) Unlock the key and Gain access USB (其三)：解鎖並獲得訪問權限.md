# Forensics 電腦鑑證 / USB (III) Unlock the key and Gain access USB 

## Challenges - 250 Pts(Init: 250 Pts) - 0 Solved

```
Author 作者：ISOC

Description 描述：

We intercepted network traffic between the image owner and secondary.pwnable.hk over port 50002. Try to unlock the private key in the image and gain access to the machine.

我們發現USB手指的持有人和 secondary.pwnable.hk 有經過 50002 port 的通訊。請嘗試找出 private key 的密碼然後登入 IP 地址。
```
File: [usb.img](File/USB_3/usb.img) | [hint](File/USB_3/hint)

## Solve: 

so here we need to get the private key passphrase, from the hint
 ```
# I no longer live in my village...
# do SHA256 1337 times of its name
```
we can know that we have to do SHA256 for 1337 times with his '_village_', and from 'USB/Pictures' we can see that

![my-village.png](File/USB_3/Pictures/my-village.png)

seem '_village_' is **"Pak Sha Tsuen"**, so here my script to solve:
```python
# goal: SHA256 1337 tim to message "Pak Sha Tsuen"
import hashlib
import sys
import os
import time



data = "Pak Sha Tsuen".encode('utf-8')
a = 1337
s = hashlib.sha256()
s.update(data)
h = s.digest()
print("First hash: " + str(s.digest()))

for a in range(a):
    # time.sleep(0.01)
    sys.stdout.write("\r\n")
    s = hashlib.sha256()
    
    s.update(h)
    h = s.digest()
    sys.stdout.write("running... " + str(a) + " | PWN--> "+ h.hex())
    sys.stdout.flush()
    if a == 1335:
        sys.stdout.write("\n Done: " + str(a) + " | Solve: " + h.hex())
        break

```
and by running it, we will get:
```
......
running... 1330 | PWN--> 879fc283e43378826f70efd20568428898d010989b472302e6914e031ba4f1d0
running... 1331 | PWN--> f9d1389625cbe81eb6330b2cae811daa05829e34ee7b776293fa0595c4c8a088
running... 1332 | PWN--> 0f8cd30104bb4053f61220a6735f253c99f8bb3d99b907eaa9108cc21bb6511a
running... 1333 | PWN--> 4ffbd16233b088cbca10a4f429b5fbd76736d4f5de92ef2f2f209ed29b16481a
running... 1334 | PWN--> be59ffccb6254ba9de43ee65c9922474d0095d435378782654e45df8d7f7da9d
Done: 1335 | Solve: 387c3d44971e0a08075d1046904b396dce4e5469bbbd7cbba894dd702dfaabbd
```
and that the solve! by connecting it to secondary.pwnable.hk:50002, we got this:
```
# RedTeaDev at Flag in ~\Downloads\usb\Keys on git:(unknown) ≢ [3:13:59]
➜ ssh root@secondary.pwnable.hk -p 50002 -i private
Enter passphrase for key 'private': 387c3d44971e0a08075d1046904b396dce4e5469bbbd7cbba894dd702dfaabbd
Linux cba418faf194 5.4.0-1029-aws #30-Ubuntu SMP Tue Oct 20 10:06:38 UTC 2020 x86_64
hkcert20{NEVERF0RG1V3}
Last login: Tue Nov 10 16:51:46 2020 from ***.***.***.***
This account is currently not available.
Connection to secondary.pwnable.hk closed.
```
that the flag!
## Flags:
hkcert20{NEVERF0RG1V3}
