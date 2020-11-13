# HKCERT CTF Challenge 2020 Writeup
### Team: T0077 - HKUST
### Challenge Name: Tuning Keyboard 通靈字盤 (Misc, 482 points)

Solved by _Vincent_
Written by _Starry Miracle_

---

Flag format: `hkcert20{...}`

Description 描述：
* Username: Guest 帳號： 訪客
* Password: Guess 密碼： 猜測

---

Step 1. Look at the free hint! (isn't them cute?)

![](https://i.imgur.com/rd43vn3.jpg)

Step 2. Find out what is going on 

- Unzip the file. You should find `0.jpg`, `1.jpg`, `flag.jpg` and `yaminogemu.html`.
- Have a look at `yaminogemu.html` (after you find out that it is not a steganography challenge)
- There is a comment in line 52, how about changing it to `q.innerText += ''+ok+''+dk+''+ek+''+ak+''+tk+''+hk;`
- Some 1s and 0s shows up! Maybe this is the encoded flag?
- However, after restarting and get the value of `q` again, the result changed...
- It seems that `setTimeout` is not accurate enough to "get the frequency" of the challenge author

Step 3. Solving the challenge :)

- Write a solver that can simulate what the `setTimeout` in HTML
![](https://imgur.com/RMxw4YU.jpg)
- Since it is in group of 6, maybe the binarys are encoded in group of 6? (2^6 is ... 64!)
Converting the binary to base64 we get`aGtjZXJ0MjB7SEEqTkEqU0V9`, and decoding this we get the flag.

Flag: `hkcert20{HA*NA*SE}`