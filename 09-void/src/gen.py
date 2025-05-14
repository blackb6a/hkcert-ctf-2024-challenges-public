code = '''
const flag = document.getElementById('flag');
flag.focus();

handleKeyPress = event => event.key === 'Enter' && check();

function check() {
    if (flag.value === 'hkcert24{j4v4scr1p7_1s_n0w_alm0s7_y3t_4n0th3r_wh173sp4c3_pr09r4mm1n9_l4ngu4g3}') {
        flag.disabled = true;
        flag.classList.add('correct');
    } else {
        flag.classList.add('wrong');
        setTimeout(() => flag.classList.remove('wrong'), 500);
    }
}
'''.strip()

print('''
<!DOCTYPE html>
<html>

<head>
  <meta charset="UTF-8">
  <title>Codeless</title>
  <link rel="stylesheet" href="style.css">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@300..700&family=Playfair+Display:ital,wght@0,400..900;1,400..900&display=swap" rel="stylesheet">
</head>

<body>
    <div class="container">
        <input type="text" id="flag" placeholder="What is the flag?" onkeydown="handleKeyPress(event)">
    </div>
</body>

<script>
'''.strip())

print('with (ㅤ`` ) {')
for c in code.encode().hex() + '00':
    print('ㅤ'*(int(c, 16)+1))
print('}')

print('''
// https://x.com/aemkei/status/1843756978147078286
function \\u3164(){return f="",p=[]  
,new Proxy({},{has:(t,n)=>(p.push(
n.length-1),2==p.length&&(p[0]||p[
1]||eval(f),f+=String.fromCharCode
(p[0]<<4|p[1]),p=[]),!0)})}//aem1k
</script>
</html>

'''.strip() + '\n')