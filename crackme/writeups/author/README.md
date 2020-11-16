# Crackme

## Prologue 

Trying to design a chal with medium level for secondary school.

## Walk-through

Use `dex-tool` to convert APK to jar.
![](./img/01.PNG)

Use `jd-gui` for decompiling jar, you may see the logic handling flag checking
![](./img/02.PNG)

Use `z3` to solve the SMT, or it's simple enough to do it by hand. Check out `sol.py` for z3 usage.
![](./img/03.PNG)

## Flag
`hkcert20{ar3_y0u_us1ng_z3}`

## Epilogue
Solve: 13/84 (Secondary)
Solve: 34/81 (Tertiary)

Unlike Doom, you can really run the apk on device with Andriod 7.0+. Why are you expecting that the chals can be run on machines?

## Reference
<https://github.com/Z3Prover/z3>

