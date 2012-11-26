cpf = "05671039940"

i = 0
multiplicador = 10
somador = 0
for i in range(9):
	somador = int(cpf[i])*multiplicador + somador
	multiplicador -= 1
	if (somador%11) < 2:
		d1 = 0
	else:
		d1 = 11 - (somador%11)
if d1 != int(cpf[9]):
	print "Invalido"
print d1
i = 0
multiplicador = 11
somador = 0

for i in range(10):
	somador = int(cpf[i])*multiplicador + somador
	multiplicador -= 1
	if (somador%11) < 2:
		d2 = 0
	else:
		d2 = 11 - (somador%11)

if d2 != int(cpf[10]):
	print "Invalido"
print d2