# HKCERT CTF Challenge 2020 Writeup
### Team: T0077 - HKUST
### Challenge Name: RAM 拉姆 (Misc, 450 points)

Solved by _Vincent_

---

Objective: Get user passwords from `memory.dmp` of RAM image

Flag format: `hkcert20{(pw of flag01)_(pw of flag02)_(pw of flag03)_(pw of flag04)_(pw of flag05)}`

---

Reference: OtterCTF 2018 Memory Forensics Write-up (Part I)
https://medium.com/@sbasu7241/otterctf-2018-memory-forensics-write-up-part-1-ea27a144a5d4

Simply follow the steps of the above write-up :)

1. Install `volatility`
2. Identify the correct profile for the memory image using `imageinfo`, verify with `kdbgscan`

![](https://i.imgur.com/EgUAOCu.png)

![](https://i.imgur.com/mikpokj.png)

3. Get the passwords using `hashdump`

![](https://i.imgur.com/xPlTlLn.png)

We now have all the passwords, hashed:

```1
flag01:1678ac6f5380c60363a91082d0699c74
flag02:40e43aee94115e12541624221019423b
flag03:186cb09181e2c2ecaac768c47c729904
flag04:5c3b27ff63ae1e7e1b3221b19f00183c
flag05:1597f8e3b872d5348767416f6921d346
```

Final step: crack the hashes

![](https://i.imgur.com/OhE37Cw.png)

Flag: `hkcert20{this_is_a_MD5_challenge}`