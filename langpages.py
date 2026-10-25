#!/usr/bin/env python3
"""python3 langpages.py : one page per language (de/index.html, ru/index.html ...) from index.html, so every language has its own address that can be indexed.
Each page is index.html with: <html lang=..>, the translated title / description / intro text, <base href="../"> (so app.css, app.js, i18n.js, version.json stay the shared files in the root), canonical + hreflang links.
Also writes sitemap.xml and robots.txt, and refreshes the hreflang block and the English intro in index.html itself. Run it after bump.py (the ?v= of the files is copied from index.html)."""
import re,os
SITE='https://hracik.github.io/tb-stack-calculator/'
EN=dict(
 name='Total Battle stack calculator',
 desc="The most accurate Total Battle calculator: plan your army stacks to fight epic monsters or other players. Saves time, saves resources, free forever.",
 intro="Krappy Calculator is a free calculator for Total Battle. Enter your Leadership, Dominance, Authority and bonuses, and it shows which troops to send, how many of each and in which order, for a hit on an epic monster such as Shadow City, Arcanomancer or Doomsday, or on other players. Your tabs are saved in your browser, and you can sign in to keep them on every device.")
L={
'ru':('Калькулятор стеков Total Battle','Самый точный калькулятор для Total Battle: планируйте стеки армии для боёв с эпическими монстрами и другими игроками. Экономит время и ресурсы, бесплатно навсегда.','Krappy Calculator — бесплатный калькулятор для Total Battle. Введите Лидерство, Доминирование, Авторитет и бонусы, и он покажет, каких войск отправить, сколько каждого и в каком порядке, для удара по эпическому монстру, например Shadow City, Arcanomancer или Doomsday, или по другим игрокам. Ваши вкладки сохраняются в браузере, а войдя в аккаунт, вы получите их на каждом устройстве.'),
'de':('Total Battle Stack-Rechner','Der genaueste Total-Battle-Rechner: plane deine Armee-Stacks für Kämpfe gegen epische Monster oder andere Spieler. Spart Zeit, spart Ressourcen, für immer kostenlos.','Krappy Calculator ist ein kostenloser Rechner für Total Battle. Gib deine Führung, Dominanz, Autorität und Boni ein, und er zeigt, welche Truppen du schicken sollst, wie viele von jeder und in welcher Reihenfolge, für einen Angriff auf ein episches Monster wie Shadow City, Arcanomancer oder Doomsday oder auf andere Spieler. Deine Tabs werden in deinem Browser gespeichert, und mit einer Anmeldung hast du sie auf jedem Gerät.'),
'es':('Calculadora de stacks de Total Battle','La calculadora de Total Battle más precisa: planifica los stacks de tu ejército para luchar contra monstruos épicos u otros jugadores. Ahorra tiempo, ahorra recursos, gratis para siempre.','Krappy Calculator es una calculadora gratuita para Total Battle. Introduce tu Liderazgo, Dominio, Autoridad y bonificaciones, y te muestra qué tropas enviar, cuántas de cada una y en qué orden, para atacar a un monstruo épico como Shadow City, Arcanomancer o Doomsday, o a otros jugadores. Tus pestañas se guardan en tu navegador, y puedes iniciar sesión para tenerlas en todos tus dispositivos.'),
'fr':('Calculateur de stacks Total Battle','Le calculateur Total Battle le plus précis : planifiez les stacks de votre armée pour affronter les monstres épiques ou d\'autres joueurs. Gagne du temps, économise des ressources, gratuit pour toujours.','Krappy Calculator est un calculateur gratuit pour Total Battle. Saisissez votre Leadership, Domination, Autorité et vos bonus, et il indique quelles troupes envoyer, combien de chaque et dans quel ordre, pour attaquer un monstre épique comme Shadow City, Arcanomancer ou Doomsday, ou d\'autres joueurs. Vos onglets sont enregistrés dans votre navigateur, et vous pouvez vous connecter pour les retrouver sur chaque appareil.'),
'tr':('Total Battle yığın hesaplayıcı','En doğru Total Battle hesaplayıcısı: epik canavarlarla veya diğer oyuncularla savaşmak için ordu yığınlarını planla. Zaman kazandırır, kaynak kazandırır, sonsuza dek ücretsiz.','Krappy Calculator, Total Battle için ücretsiz bir hesaplayıcıdır. Liderlik, Hâkimiyet, Otorite ve bonuslarını gir; Shadow City, Arcanomancer veya Doomsday gibi bir epik canavara ya da diğer oyunculara vuruş için hangi birlikleri, her birinden kaç tane ve hangi sırayla göndereceğini gösterir. Sekmelerin tarayıcında saklanır, giriş yaparak her cihazda kullanabilirsin.'),
'pl':('Kalkulator stosów Total Battle','Najdokładniejszy kalkulator do Total Battle: zaplanuj stosy armii do walki z epickimi potworami lub innymi graczami. Oszczędza czas i zasoby, darmowy na zawsze.','Krappy Calculator to darmowy kalkulator do Total Battle. Wpisz swoje Przywództwo, Dominację, Autorytet i bonusy, a pokaże, jakie wojska wysłać, ile każdego i w jakiej kolejności, aby uderzyć w epickiego potwora, takiego jak Shadow City, Arcanomancer czy Doomsday, lub w innych graczy. Twoje karty są zapisywane w przeglądarce, a po zalogowaniu masz je na każdym urządzeniu.'),
'pt':('Calculadora de stacks de Total Battle','A calculadora de Total Battle mais precisa: planeje os stacks do seu exército para enfrentar monstros épicos ou outros jogadores. Economiza tempo, economiza recursos, grátis para sempre.','Krappy Calculator é uma calculadora gratuita para Total Battle. Digite sua Liderança, Domínio, Autoridade e bônus, e ela mostra quais tropas enviar, quantas de cada e em que ordem, para atacar um monstro épico como Shadow City, Arcanomancer ou Doomsday, ou outros jogadores. Suas abas ficam salvas no navegador, e você pode entrar na conta para tê-las em todos os dispositivos.'),
'id':('Kalkulator stack Total Battle','Kalkulator Total Battle paling akurat: rencanakan stack pasukan Anda untuk melawan monster epik atau pemain lain. Hemat waktu, hemat sumber daya, gratis selamanya.','Krappy Calculator adalah kalkulator gratis untuk Total Battle. Masukkan Kepemimpinan, Dominasi, Otoritas, dan bonus Anda, lalu kalkulator menunjukkan pasukan apa yang dikirim, berapa banyak masing-masing, dan dalam urutan apa, untuk menyerang monster epik seperti Shadow City, Arcanomancer, atau Doomsday, atau pemain lain. Tab Anda disimpan di browser, dan Anda bisa masuk ke akun agar tersedia di semua perangkat.'),
'ar':('حاسبة ستاك Total Battle','أدق حاسبة للعبة Total Battle: خطّط ستاك جيشك لمحاربة الوحوش الملحمية أو اللاعبين الآخرين. توفّر الوقت والموارد، ومجانية للأبد.','Krappy Calculator حاسبة مجانية للعبة Total Battle. أدخل القيادة والهيمنة والسلطة والمكافآت لديك، وستعرض لك أي القوات ترسل وكم من كل نوع وبأي ترتيب، لضرب وحش ملحمي مثل Shadow City أو Arcanomancer أو Doomsday، أو لضرب لاعبين آخرين. تُحفظ علامات تبويبك في متصفحك، ويمكنك تسجيل الدخول للاحتفاظ بها على كل جهاز.'),
'it':('Calcolatore di stack per Total Battle','Il calcolatore di Total Battle più preciso: pianifica gli stack del tuo esercito per combattere mostri epici o altri giocatori. Fa risparmiare tempo e risorse, gratis per sempre.','Krappy Calculator è un calcolatore gratuito per Total Battle. Inserisci Leadership, Dominanza, Autorità e bonus, e ti mostra quali truppe inviare, quante di ciascuna e in quale ordine, per colpire un mostro epico come Shadow City, Arcanomancer o Doomsday, oppure altri giocatori. Le tue schede vengono salvate nel browser e puoi accedere per averle su ogni dispositivo.'),
'nl':('Total Battle stackcalculator','De nauwkeurigste Total Battle-calculator: plan je legerstacks om te vechten tegen epische monsters of andere spelers. Bespaart tijd en grondstoffen, voor altijd gratis.','Krappy Calculator is een gratis calculator voor Total Battle. Vul je Leiderschap, Dominantie, Autoriteit en bonussen in, en hij laat zien welke troepen je moet sturen, hoeveel van elk en in welke volgorde, voor een aanval op een episch monster zoals Shadow City, Arcanomancer of Doomsday, of op andere spelers. Je tabbladen worden in je browser opgeslagen en met inloggen heb je ze op elk apparaat.'),
'no':('Total Battle stackkalkulator','Den mest nøyaktige Total Battle-kalkulatoren: planlegg hærstackene dine for å kjempe mot episke monstre eller andre spillere. Sparer tid og ressurser, gratis for alltid.','Krappy Calculator er en gratis kalkulator for Total Battle. Skriv inn Ledelse, Dominans, Autoritet og bonuser, så viser den hvilke tropper du skal sende, hvor mange av hver og i hvilken rekkefølge, for et angrep på et episk monster som Shadow City, Arcanomancer eller Doomsday, eller på andre spillere. Fanene dine lagres i nettleseren, og du kan logge inn for å ha dem på alle enheter.'),
'sv':('Total Battle stackkalkylator','Den mest exakta Total Battle-kalkylatorn: planera dina arméstackar för att slåss mot episka monster eller andra spelare. Sparar tid och resurser, gratis för alltid.','Krappy Calculator är en gratis kalkylator för Total Battle. Ange ditt Ledarskap, Dominans, Auktoritet och dina bonusar, så visar den vilka trupper du ska skicka, hur många av varje och i vilken ordning, för ett angrepp på ett episkt monster som Shadow City, Arcanomancer eller Doomsday, eller på andra spelare. Dina flikar sparas i webbläsaren, och du kan logga in för att ha dem på alla enheter.'),
'vi':('Máy tính stack Total Battle','Máy tính Total Battle chính xác nhất: lên kế hoạch stack quân để đánh quái vật epic hoặc người chơi khác. Tiết kiệm thời gian và tài nguyên, miễn phí mãi mãi.','Krappy Calculator là máy tính miễn phí cho Total Battle. Nhập Lãnh đạo, Thống trị, Uy quyền và các điểm thưởng của bạn, máy sẽ cho biết nên gửi quân nào, mỗi loại bao nhiêu và theo thứ tự nào, để đánh quái vật epic như Shadow City, Arcanomancer hay Doomsday, hoặc người chơi khác. Các tab được lưu trong trình duyệt, và bạn có thể đăng nhập để dùng chúng trên mọi thiết bị.'),
}
BRAND='Krappy Calculator'
def title(n):return BRAND+' – '+n
def url(l):return SITE if l=='en' else SITE+l+'/'
def block(cur):
    r=['<link rel="canonical" href="%s">'%url(cur)]
    for l in ['en']+list(L):r.append('<link rel="alternate" hreflang="%s" href="%s">'%(l,url(l)))
    r.append('<link rel="alternate" hreflang="x-default" href="%s">'%SITE)
    return '<!--hl-->'+''.join(r)+'<!--/hl-->'
def intro(t):return '<!--intro--><section class="seo" data-notr><p>'+t+'</p></section><!--/intro-->'
def esc(x):return x.replace('&','&amp;').replace('"','&quot;')
def rep(h,a,b):
    assert a in h,a[:40];return h.replace(a,b)
src=open('index.html').read()
root=src
# the markers are added once; after that they are only refreshed
if '<!--hl-->' not in root:
    root=rep(root,'<meta name="twitter:card"',block('en')+'\n<meta name="twitter:card"')
if '<!--intro-->' not in root:
    root=rep(root,'<footer class="ft">',intro(EN['intro'])+'\n<footer class="ft">')
root=re.sub(r'<!--hl-->.*?<!--/hl-->',lambda _:block('en'),root,flags=re.S)
root=re.sub(r'<!--intro-->.*?<!--/intro-->',lambda _:intro(EN['intro']),root,flags=re.S)
open('index.html','w').write(root)
for l,(n,d,i) in L.items():
    h=root
    h=rep(h,'<html lang="en">','<html lang="%s"%s data-pl="1">'%(l,' dir="rtl"' if l=='ar' else ''))
    h=h.replace(title(EN['name']),title(n)).replace(esc(EN['desc']),esc(d))
    h=rep(h,'<meta charset="utf-8">','<meta charset="utf-8"><base href="../">')
    h=re.sub(r'<!--hl-->.*?<!--/hl-->',lambda _:block(l),h,flags=re.S)
    h=re.sub(r'<!--intro-->.*?<!--/intro-->',lambda _:intro(i),h,flags=re.S)
    os.makedirs(l,exist_ok=True);open(l+'/index.html','w').write(h)
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for l in ['en']+list(L):
    sm+='<url><loc>%s</loc>'%url(l)+''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>'%(k,url(k)) for k in ['en']+list(L))+'</url>\n'
open('sitemap.xml','w').write(sm+'</urlset>\n')
open('robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: '+SITE+'sitemap.xml\n')
print('pages',len(L)+1)
