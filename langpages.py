#!/usr/bin/env python3
"""python3 langpages.py : one page per language (de/index.html, ru/index.html ...) from index.html, so every language has its own address that can be indexed.
Each page is index.html with: <html lang=..>, the translated title / description / intro text, <base href="../"> (so app.css, app.js, i18n.js, version.json stay the shared files in the root), canonical + hreflang links.
Also writes sitemap.xml and robots.txt, and refreshes the hreflang block and the English intro in index.html itself. Run it after bump.py (the ?v= of the files is copied from index.html)."""
import re,os
SITE='https://hracik.github.io/tb-stack-calculator/'
EN=dict(
 name='Total Battle stack calculator',
 desc="The most accurate Total Battle calculator: plan your army stacks to fight epic monsters or other players. Saves time, saves resources, free forever.",
 intro="Krappy Calculator is the most efficient stacking calculator for the game Total Battle. Save time, save resources, free to use forever. Fight even more epic monsters and players with Krappy stacks.")
L={
'ru':('Калькулятор стеков Total Battle','Самый точный калькулятор для Total Battle: планируйте стеки армии для боёв с эпическими монстрами и другими игроками. Экономит время и ресурсы, бесплатно навсегда.','Krappy Calculator — самый эффективный калькулятор стеков для игры Total Battle. Экономьте время, экономьте ресурсы, пользуйтесь бесплатно навсегда. Побеждайте ещё больше эпических монстров и игроков со стеками Krappy.'),
'de':('Total Battle Stack-Rechner','Der genaueste Total-Battle-Rechner: plane deine Armee-Stacks für Kämpfe gegen epische Monster oder andere Spieler. Spart Zeit, spart Ressourcen, für immer kostenlos.','Krappy Calculator ist der effizienteste Stacking-Rechner für das Spiel Total Battle. Spare Zeit, spare Ressourcen, für immer kostenlos nutzbar. Besiege noch mehr epische Monster und Spieler mit Krappy-Stacks.'),
'es':('Calculadora de stacks de Total Battle','La calculadora de Total Battle más precisa: planifica los stacks de tu ejército para luchar contra monstruos épicos u otros jugadores. Ahorra tiempo, ahorra recursos, gratis para siempre.','Krappy Calculator es la calculadora de apilado más eficiente para el juego Total Battle. Ahorra tiempo, ahorra recursos, uso gratuito para siempre. Derrota a aún más monstruos épicos y jugadores con los stacks de Krappy.'),
'fr':('Calculateur de stacks Total Battle','Le calculateur Total Battle le plus précis : planifiez les stacks de votre armée pour affronter les monstres épiques ou d\'autres joueurs. Gagne du temps, économise des ressources, gratuit pour toujours.',"Krappy Calculator est le calculateur d'empilement le plus efficace pour le jeu Total Battle. Gagnez du temps, économisez des ressources, gratuit pour toujours. Battez encore plus de monstres épiques et de joueurs avec les stacks Krappy."),
'tr':('Total Battle yığın hesaplayıcı','En doğru Total Battle hesaplayıcısı: epik canavarlarla veya diğer oyuncularla savaşmak için ordu yığınlarını planla. Zaman kazandırır, kaynak kazandırır, sonsuza dek ücretsiz.','Krappy Calculator, Total Battle oyunu için en verimli istifleme hesaplayıcısıdır. Zaman kazan, kaynak kazan, sonsuza dek ücretsiz kullan. Krappy yığınlarıyla daha da fazla epik canavarı ve oyuncuyu yen.'),
'pl':('Kalkulator stosów Total Battle','Najdokładniejszy kalkulator do Total Battle: zaplanuj stosy armii do walki z epickimi potworami lub innymi graczami. Oszczędza czas i zasoby, darmowy na zawsze.','Krappy Calculator to najskuteczniejszy kalkulator układania stosów do gry Total Battle. Oszczędzaj czas, oszczędzaj zasoby, korzystaj za darmo na zawsze. Pokonuj jeszcze więcej epickich potworów i graczy ze stosami Krappy.'),
'pt':('Calculadora de stacks de Total Battle','A calculadora de Total Battle mais precisa: planeje os stacks do seu exército para enfrentar monstros épicos ou outros jogadores. Economiza tempo, economiza recursos, grátis para sempre.','Krappy Calculator é a calculadora de empilhamento mais eficiente para o jogo Total Battle. Economize tempo, economize recursos, uso gratuito para sempre. Derrote ainda mais monstros épicos e jogadores com os stacks do Krappy.'),
'id':('Kalkulator stack Total Battle','Kalkulator Total Battle paling akurat: rencanakan stack pasukan Anda untuk melawan monster epik atau pemain lain. Hemat waktu, hemat sumber daya, gratis selamanya.','Krappy Calculator adalah kalkulator penumpukan paling efisien untuk game Total Battle. Hemat waktu, hemat sumber daya, gratis digunakan selamanya. Kalahkan lebih banyak monster epik dan pemain dengan stack Krappy.'),
'ar':('حاسبة ستاك Total Battle','أدق حاسبة للعبة Total Battle: خطّط ستاك جيشك لمحاربة الوحوش الملحمية أو اللاعبين الآخرين. توفّر الوقت والموارد، ومجانية للأبد.','Krappy Calculator هي أكفأ حاسبة تكديس للعبة Total Battle. وفّر الوقت ووفّر الموارد، واستخدمها مجانًا للأبد. اهزم المزيد من الوحوش الملحمية واللاعبين بستاك Krappy.'),
'it':('Calcolatore di stack per Total Battle','Il calcolatore di Total Battle più preciso: pianifica gli stack del tuo esercito per combattere mostri epici o altri giocatori. Fa risparmiare tempo e risorse, gratis per sempre.','Krappy Calculator è il calcolatore di stacking più efficiente per il gioco Total Battle. Risparmia tempo, risparmia risorse, gratis per sempre. Sconfiggi ancora più mostri epici e giocatori con gli stack Krappy.'),
'nl':('Total Battle stackcalculator','De nauwkeurigste Total Battle-calculator: plan je legerstacks om te vechten tegen epische monsters of andere spelers. Bespaart tijd en grondstoffen, voor altijd gratis.','Krappy Calculator is de meest efficiënte stackingcalculator voor het spel Total Battle. Bespaar tijd, bespaar grondstoffen, voor altijd gratis te gebruiken. Versla nog meer epische monsters en spelers met Krappy-stacks.'),
'no':('Total Battle stackkalkulator','Den mest nøyaktige Total Battle-kalkulatoren: planlegg hærstackene dine for å kjempe mot episke monstre eller andre spillere. Sparer tid og ressurser, gratis for alltid.','Krappy Calculator er den mest effektive stackingkalkulatoren for spillet Total Battle. Spar tid, spar ressurser, gratis å bruke for alltid. Slå enda flere episke monstre og spillere med Krappy-stacks.'),
'sv':('Total Battle stackkalkylator','Den mest exakta Total Battle-kalkylatorn: planera dina arméstackar för att slåss mot episka monster eller andra spelare. Sparar tid och resurser, gratis för alltid.','Krappy Calculator är den mest effektiva stackingkalkylatorn för spelet Total Battle. Spara tid, spara resurser, gratis att använda för alltid. Besegra ännu fler episka monster och spelare med Krappy-stacks.'),
'vi':('Máy tính stack Total Battle','Máy tính Total Battle chính xác nhất: lên kế hoạch stack quân để đánh quái vật epic hoặc người chơi khác. Tiết kiệm thời gian và tài nguyên, miễn phí mãi mãi.','Krappy Calculator là máy tính xếp chồng hiệu quả nhất cho game Total Battle. Tiết kiệm thời gian, tiết kiệm tài nguyên, miễn phí sử dụng mãi mãi. Đánh bại nhiều quái vật epic và người chơi hơn với các stack Krappy.'),
}
BRAND='Krappy Calculator'
def title(n):return BRAND+' – '+n
def url(l):return SITE if l=='en' else SITE+l+'/'
def block(cur):
    r=['<link rel="canonical" href="%s">'%url(cur)]
    for l in ['en']+list(L):r.append('<link rel="alternate" hreflang="%s" href="%s">'%(l,url(l)))
    r.append('<link rel="alternate" hreflang="x-default" href="%s">'%SITE)
    return '<!--hl-->'+''.join(r)+'<!--/hl-->'
def intro(t,own=False):return '<!--intro--><section class="seo"'+(' data-notr' if own else '')+'><p>'+t+'</p></section><!--/intro-->'      # footer text; the root page lets i18n translate it (a key in i18n.js), a language page has it written in its language already
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
    h=re.sub(r'<!--intro-->.*?<!--/intro-->',lambda _:intro(i,True),h,flags=re.S)
    os.makedirs(l,exist_ok=True);open(l+'/index.html','w').write(h)
sm='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
for l in ['en']+list(L):
    sm+='<url><loc>%s</loc>'%url(l)+''.join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>'%(k,url(k)) for k in ['en']+list(L))+'</url>\n'
open('sitemap.xml','w').write(sm+'</urlset>\n')
open('robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: '+SITE+'sitemap.xml\n')
print('pages',len(L)+1)
