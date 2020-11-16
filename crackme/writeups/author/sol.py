from z3 import *
s=[Int('serial%d' % i) for i in range(26)]
solver = Solver()

solver.add(s[0] + s[1] - s[2] == 112)
solver.add(s[1] + s[2] - s[3] == 105)
solver.add(s[2] + s[3] - s[4] == 86)
solver.add(s[3] + s[4] - s[5] == 99)
solver.add(s[4] + s[5] - s[6] == 180)
solver.add(s[5] + s[6] - s[7] == 118)
solver.add(s[6] + s[7] - s[8] == -25)
solver.add(s[7] + s[8] - s[9] == 74)
solver.add(s[8] + s[9] - s[10] == 106)
solver.add(s[9] + s[10] - s[11] == 160)
solver.add(s[10] + s[11] - s[12] == 70)
solver.add(s[11] + s[12] - s[13] == 25)
solver.add(s[12] + s[13] - s[14] == 168)
solver.add(s[13] + s[14] - s[15] == 52)
solver.add(s[14] + s[15] - s[16] == 70)
solver.add(s[15] + s[16] - s[17] == 95)
solver.add(s[16] + s[17] - s[18] == 97)
solver.add(s[17] + s[18] - s[19] == 183)
solver.add(s[18] + s[19] - s[20] == 54)
solver.add(s[19] + s[20] - s[21] == 56)
solver.add(s[20] + s[21] - s[22] == 118)
solver.add(s[21] + s[22] - s[23] == 76)
solver.add(s[22] + s[23] - s[24] == 166)
solver.add(s[23] + s[24] - s[25] == 48)
solver.add(s[24] + s[25] - s[0] == 72)
solver.add(s[25] + s[0] - s[1] == 122)


print(solver.check())
answer=solver.model()
print(answer)

tidy_answer = ""
for each in s :
	tidy_answer += str(chr(int(str(answer[each]))))

print(tidy_answer)