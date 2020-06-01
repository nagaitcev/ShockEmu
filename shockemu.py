import string, sys

letters = 0, 11, 8, 2, 14, 3, 5, 4, 34, 38, 40, 37, 46, 45, 31, 35, 12, 15, 1, 17, 32, 9, 13, 7, 16, 6
nums = 29, 18, 19, 20, 21, 23, 22, 26, 28, 25

keys = dict(
	escape=53,
	f1=107, f2=113, f3=160, f4=131, f5=96, f6=97, f7=98, f8=100, f9=101, f10=109, f11=103, f12=111,
	f13=105, f14=107, f15=113, f16=106, f17=64, f18=79, f19=80, f20=90,
	d1=18, d2=19, d3=20, d4=21, d5=23, d6=22, d7=26, d8=28, d9=25, d0=29,
	backtick=50, minus=27, plus=24, delete=51,
	q=12, w=13, e=14, r=15, t=17, y=16, u=32, i=34, o=31, p=35, openBrace=33, closeBrace=30,
	a=0, s=1, d=2, f=3, g=5, h=4, j=38, k=40, l=37, colon=41, quote=39,
	z=6, x=7, c=8, v=9, b=11, n=45, m=46, comma=43, period=47, slash=44, backslash=42,
	tab=48, capslock=57,
	leftShift=56, rightShift=60,
	leftControl=59, rightControl=62, leftOption=58, rightOption=61, command=55,
	space=49,
	enter=76,
	up=126, down=125, left=123, right=124,
	home=115, end=119, pageUp=116, pageDown=121,
	num1=83, num2=84, num3=85, num4=86, num5=87, num6=88, num7=89, num8=91, num9=92, num0=82,
	numAsterisk=67, numSlash=75, numPlus=69, numMinus=78, numEq=81, numPeriod=65, numClear=71,
)

buttons = 'dpadUp dpadLeft dpadRight dpadDown X O square triangle PS touchpad options share L1 L2 L3 R1 R2 R3'.split(' ')

axes = 'leftX- leftX+ leftY- leftY+ rightX- rightX+ rightY- rightY+'.split(' ')

for i, x in enumerate(letters):
	keys[chr(ord('a') + i)] = x
for i, x in enumerate(nums):
	keys[str(i)] = x

def parse(data):
	lines = (line.split('#', 1)[0].strip() for line in data.split('\n'))
	return dict(map(string.strip, line.split('=', 1)) for line in lines if line)

with open('mapKeys.h', 'w') as fp:
	keysticks = []
	mouseLook = None
	for k, v in parse(open(sys.argv[1]).read()).items():
		if k in keys or k == 'leftMouse' or k == 'rightMouse':
			if k in keys:
				k = 'DOWN(%i)' % keys[k]
			if v in buttons:
				print(fp, '%s = %s;' % (v, k))
			elif v in axes:
				stick = v[:-2]
				if stick not in keysticks:
					print(fp, '%sX = %sY = 0;' % (stick, stick))
					keysticks.append(stick)
				print(fp, 'if(%s) %s %s= 1;' % (k, v[:-1], v[-1]))
			else:
				print('Unknown button: {0}'.format(v))
		elif k.startswith('mouseLook.'):
			if mouseLook is None:
				mouseLook = dict(type='linear', deadZone='.1', decay='10', multX='1', multY='1', stick='right')
			mouseLook[k.split('.', 1)[1]] = v
		else:
			print('Unknown key: {0}'.format(k))

	if mouseLook is not None:
		if mouseLook['type'] == 'linear':
			print(fp,
					'''if(mouseMoved) {{
						{stick}X = -mouseAccelX;
						{stick}Y = mouseAccelY;
						mouseMoved = false;
					}} else {{
						{stick}X /= {decay};
						{stick}Y /= {decay};
						if(fabs({stick}X) > {deadZone} || fabs({stick}Y) > {deadZone}) {{
							NSLog(@"Still decaying... %f %f", {stick}X, {stick}Y);
							[self decayKick];
						}} else
							{stick}X = {stick}Y = 0;
					}}'''.format(**mouseLook))
		else:
			print('Unknown mouseLook type:'.format(mouseLook))
