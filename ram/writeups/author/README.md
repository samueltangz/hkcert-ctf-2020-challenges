# Write-up

## Prologue 

(Skipped)

## Steps

### Install Volatility

Quite a number of participants said that they cannot run hivelist, this is because of missing dependency for volatility plugins. Thus I'll show my installation steps for volatility 2.6.1 on Kali in this section.

```bash
sudo apt install build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev zlib1g-dev python2-dev -y
curl -LO https://bootstrap.pypa.io/get-pip.py
sudo python2 get-pip.py
rm -f https://bootstrap.pypa.io/get-pip.py
python2 -m pip install distorm3==3.4.4 pycryptodome
git clone https://github.com/volatilityfoundation/volatility.git
```

### Reading NTML Hash from RAM

OtterCTF has quite a number of challenges regarding Windows RAM. I see that there are teams taking reference from it. However, `lsadump` will not work here as I didn't set any default password inside Windows.

```bash
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