p = {}

def gen_xor(*args):
    return '^'.join([f'{_}' for _ in args])

def gen_cat(*args):
    return '.'.join([f'({_})' for _ in args])

def gen_fun(fname, arg):
    return f'({fname})({arg})'

p['INF5'] = '('+'5'*309+').(5)'

p[5] = '5' # numeric 5
p[0] = '5^5'
p[8] = '(55).(.5)^555^5' # 550 ^ 558
p[1] = '(555^55).(5)^(5).(5)^(5).(5)^55' # "54055"[:2] ^ 55
p[4] = '(555^55).(5)^(5).(5)^(5).(5)^55^5'
p[3] = '(5^5).(5555^555)^(5).(5)^(5).(5)^5' # "06040"[:2] ^ 5
p[6] = '(5^5).(5555^555)^(5).(5)^(5).(5)^.5' 
p[7] = '(55555^55).(5)^(55).(5)^(55).(5)^555' # "556045"[:3] ^ 555
p[2] = '(55555^55).(5)^(55).(5)^(55).(5)^555^5'
p[9] = '(55).(.5)^555^5^((555^55).(5)^(5).(5)^(5).(5)^55)' # p[8] ^ p[1]

p['55'] = '(5).(5)'
p['0.5'] = '.5'

p['01'] = gen_cat(p[0],p[1])
p['05'] = gen_cat(p[0],p[5])
p['23'] = gen_cat(p[2],p[3])
p['41'] = gen_cat(p[4],p[1])
p['56'] = gen_cat(p[5],p[6])
p['65'] = gen_cat(p[6],p[5])
p['70.5'] = gen_cat(p[7],'.5') #70.5 is same as 70
p['85'] = gen_cat(p[8],p[5])
p['88'] = gen_cat(p[8],p[8])

p['tr'] = gen_xor(p['INF5'], p['55'], p['88'], p['01'])
p['IM'] = gen_xor(p['INF5'], p['55'], p['56'])
p['trIM'] = gen_cat(p['tr'],p['IM'])
p['5'] = gen_fun(p['trIM'],p[5]) # string 5

p['CH'] = gen_xor(p['INF5'], p['85'], p['23'])
p['r'] = gen_xor(p['INF5'], p['85'], p['65'], p['5'])
p['CHr'] = gen_cat(p['CH'],p['r'])

p['pr'] = gen_xor(p['INF5'], p['55'], p['88'], p['41'])
p['IN'] = gen_xor(p['INF5'], p['55'], p['55'])
p['t'] = gen_xor(p['INF5'], p['85'], p['05'], p['5'])
p['F'] = gen_fun(p['CHr'], p['70.5'])
p['prINtF'] = gen_cat(p['pr'], p['IN'], p['t'], p['F'])


# flag
p['67'] = gen_cat(p[6],p[7])
p['99'] = gen_cat(p[9],p[9])
p['101'] = gen_cat(p[1],p[0],p[1])
p['104'] = gen_cat(p[1],p[0],p[4])
p['107'] = gen_cat(p[1],p[0],p[7])
p['185'] = gen_cat(p[1],p[8],p[5])
p['280'] = gen_cat(p[2],p[8],p[0])
p['060.5'] = gen_cat(p[0],p[6],'.5')

p['h'] = gen_fun(p['CHr'], p['104'])
p['k'] = gen_fun(p['CHr'], p['107'])
p['c'] = gen_fun(p['CHr'], p['99'])
p['e'] = gen_fun(p['CHr'], p['101'])
p['rt'] = gen_xor(p['INF5'], p['55'], p['88'], p['67'])
p['24'] = gen_cat(p[2],p[4])
p['{vv'] = gen_xor(p['INF5'], p['280'])
p['H@C'] = gen_xor(p['INF5'], p['185'], p['060.5'])
p['KKX.'] = gen_xor(p['INF5'], '(55).(.5)', p['70.5'])

p['12'] = gen_cat(p[1],p[2])
p['53'] = gen_cat(p[5],p[3])
p['58'] = gen_cat(p[5],p[8])
p['MD5'] = gen_cat(gen_xor(p['INF5'], p['58'], p['12']),5)
p['|}'] = gen_xor(p['INF5'], p['53'])

FLAG = gen_cat(p['h'],p['k'],p['c'],p['e'],p['rt'],p['24'],p['{vv'],p['H@C'],p['KKX.'],
               gen_fun(p['MD5'],55555), p['|}'])
print(gen_fun(p['prINtF'],FLAG))

###
# 金 ^
# 木 5
# 水 .
# 火 (
# 土 )
# 5555th: 木 => 炎木鈢森鈢林桂; 5 => (( 5 ^5 555 ^5 55 5)) 
