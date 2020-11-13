# USB (I): Disappeared file [25 pts]

8-11-2020 :: T0062 - CUHK
Solved on November 7th, 12:17:53 AM

```
Author 作者：ISOC

Description 描述：

It should have something more, the intel told us there is a file missing.

它應該還有更多內容，有些情報消失了
```
## Solution
We first check the image by `file usb.img`
```bash
usb.img: Linux rev 1.0 ext4 filesystem data, UUID=21b65b6a-89a1-4a9a-ba60-82f6f1a07fca (extents) (64bit) (large files) (huge files)
```
This is a normal ext4 filesystem, since it saids there is a file missing, that file is very likely to be deleted.

To recover the deleted files, `testdisk` is being used, looking inside the file structure looks like this
![Screenshot 2020-11-08 214342.png](https://www.dropbox.com/s/a88s3tkc287a2nx/Screenshot%202020-11-08%20214342.png?dl=0&raw=1)
The red highlighted text indicates the deleted files.

Digging around further, we saw something in the `Pictures` folder.![Screenshot 2020-11-08 214532.png](https://www.dropbox.com/s/80bxxa3hhwv9mzc/Screenshot%202020-11-08%20214532.png?dl=0&raw=1)
There was a `undelete-me.png`, but it have file size 0 so we can't recover we `testdisk`.
But a similar tool called `photorec` can be used to recover the PNG files
![Screenshot 2020-11-08 220606.png](https://www.dropbox.com/s/9jdgosns5gklwst/Screenshot%202020-11-08%20220606.png?dl=0&raw=1)
We recovered 9 files, take a look at them we notice there is a png looked like this
![f0019562.png](https://www.dropbox.com/s/qzhqa7n0ovdf6c1/f0019562.png?dl=0&raw=1)

```
flag: hkcert20{UND3L3T3_M3}
```

# USB (II): Hiding in plain sight USB [25 pts]

8-11-2020 :: T0062 - CUHK
Solved on November 6th, 8:21:06 PM

```
Author 作者：ISOC

Description 描述：

Every file in this USB has its reason to exists. Try dig out the flag from something looks ordinary

USB中的每個文件都有其存在的原因。 嘗試從一些看似平凡的東西中找出旗幟。
```
## Solution
Digging around we saw that `isochk` appears several time and in the `to-andrew.txt` mentioned
```
Hi Andrew,

I've put our code word into the file. the secret of getting the codeword is "isochk". Use our commonly used tool to extract it.

Carlos
```
This suggest `isochk` can be used as a passphrase somewhere, and the most common use for passphrase maybe at unzipping, decrypting or `steghide` which hides information in jpeg files and there is only one jpeg file in the USB called `images.jpeg`.
Using `steghide --extract -sf images.jpeg -p 'isochk'` reveals us a `steg.txt` file.
Open up and we get the flag.
```
flag: hkcert20{simple_steghide}
```

# USB (III): Unlock the key and Gain access USB [201 pts]

8-11-2020 :: T0062 - CUHK
Solved on November 8th, 11:50:12 AM

```
Author 作者：ISOC

Description 描述：

We intercepted network traffic between the image owner and tertiary.pwnable.hk over port 50002. Try to unlock the private key in the image and gain access to the machine.

我們發現USB手指的持有人和 tertiary.pwnable.hk 有經過 50002 port 的通訊。請嘗試找出 private key 的密碼然後登入 IP 地址。
```
## Solution
We first try to connect to `tertiary.pwnable.hk:50002` through browser, which obviously is not HTTP acessible. Also we notice there are a `.ssh` folder within the USB image, which suggest this might be a SSH server, attempting to connect to it by `ssh tertiary.pwnable.hk -p 50002` we got permission denied directly from the server side public key, so we need a private key. 
By examining files inside the USB, we know there is a file `private` under the folder `Keys` that when `binwalk` gives

```bash
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
15            0xF             OpenSSH RSA1 private key, version "zaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABBpW/Zf6l"
2610          0xA32           Ubiquiti firmware header, third party, ~CRC32: 0x0, version: "SSH PRIVATE KEY-----"
```
This may be the private key we are looking for (Notes: you may have come upon this when use run `binwalk` on `usb.img`), we first try to ssh by `ssh -i private tertiary.pwnable.hk -p 50002` and we were required a passphrase, `isochk` from the previous challenge didn't work and we are stucked. 
Brute forcing wouldn't be possible since the public key at `.ssh/id_rsa.pub` shows that the key pair is a 3072 bit RSA encrypted key which is impratical to brute force.
Later in the contest, a hint was added which was a mistake that the organizer forgot to add this file in the USB image.
```
# I no longer live in my village...
# do SHA256 1337 times of its name
```
The second line might be hinting the passphrase is a SHA256 digest of the village name the USB owner lived in 1337 times.
The photo `my-village.png` is indicating the village `Pak Sha Tsuen` and the spelling can be found in `villages.txt`.
To calculate the SHA256 we used a python script.
```python
import hashlib

s = b'Pak Sha Tsuen'
for i in range(2000):
    m = hashlib.sha256()
    m.update(s)
    s = m.digest()
    print(m.hexdigest())
```
Since we are unsure which hexdigest might be the passphrase, we ran the digest for 2000 times and output to a file called `list.txt` and attempts to test which will work by testing the passphrase locally with `ssh-keygen`. To automate this process a bash script is used.
```bash
while read -r line; do
  ssh-keygen -p -P "$line" -N "000000" -f private;
  echo "$line";
done < list.txt;
```
One side note, you maybe warned for `Permissions 0755 for 'private' are too open.`, this can be fixed by `chmod 700 private`
After waiting for a while, we know the passphrase is `387c3d44971e0a08075d1046904b396dce4e5469bbbd7cbba894dd702dfaabbd`.
Turns out the 1337-th SHA256 digest is the passphrase.
We can now ssh into the server, the annoucement made by the organizer also told us the username has to be root.
`ssh -i private root@tertiary.pwnable.hk -p 50002`
```bash
~$ ssh -i private root@tertiary.pwnable.hk -p 50002
Enter passphrase for key 'private':
Linux e5a79a338e1f 5.4.0-1029-aws #30-Ubuntu SMP Tue Oct 20 10:06:38 UTC 2020 x86_64
hkcert20{NEVERF0RG1V3}
Last login: Sun Nov  8 09:50:35 2020 from 219.78.244.8
This account is currently not available.
Connection to tertiary.pwnable.hk closed.
```
```
flag: hkcert20{NEVERF0RG1V3}
```