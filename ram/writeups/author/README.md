# Write-up

## Prologue 
I would like to design a chal for Win 10 password crack as people don't update their tools. However, I found that the way that Windows stores user password has been changed since Win 10 1607 (Anniversary Update).

As a result, I have dump a Windows 10 1507 RAM image and ask for the participants to crack serval user password, which the NLTM hash result is already avaliable on web.

Using `volatility 2.6.1` can solve it.

## Replay
```
python vol.py -f '/home/test/Desktop/memory.dmp' imageinfo
python vol.py -f '/home/test/Desktop/memory.dmp' --profile=Win10x64 hivelist
python vol.py -f '/home/test/Desktop/memory.dmp' --profile=Win10x64 hashdump -s 0xffffc000bd496000 -y 0xffffc000bc63e000 > ../Desktop/pwhash.txt
```
Go to <https://crackstation.net/> and search for the NTLM hash. If you would like to use rockyou.txt to crack it, you may not be able to get all words.

## Epilogue
`hkcert{this_is_a_MD5_challenge}`
You cannot use `lsadump` as in OtterCTF as I did not save the password as default one. Plain-text password will not be showing up.

## Reference
<https://aio-forensics.com/recover-windows-passwords-Forensics>