"""Builds the troop icon sheets: one PNG per class (Guardsmen, Specialists, Engineers, Monsters, Mercenaries, Scouts).
Every cell: the report icon (ICD) of the troop, its name, class + tier + category (+ type). Use it to tell which troop is which in a battle report.
Run: python3 tools/troop_sheets.py   (writes tools/troop_sheets/*.png and troop_sheets/index.html)"""
import os,sys
from playwright.sync_api import sync_playwright
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(ROOT,'tools','troop_sheets')
JS=r"""()=>{
const TRset=new Set(TR.map(t=>t.name)),mercs=new Set(MERC.map(m=>m[2])),scouts=new Set(SCOUTS);
const all=Object.values(TRN);
const grp={Guardsmen:t=>t.cls=='G'&&TRset.has(t.name)&&!scouts.has(t.name),Specialists:t=>t.cls=='S'&&TRset.has(t.name)&&!scouts.has(t.name)&&t.cat!='Scout',Engineers:t=>t.cls=='E'&&TRset.has(t.name),Monsters:t=>t.cls=='M'&&TRset.has(t.name),Mercenaries:t=>mercs.has(t.name),Scouts:t=>scouts.has(t.name)||(t.cat=='Scout'&&TRset.has(t.name))};
const ci=c=>['Melee','Ranged','Mounted','Flying'].indexOf(c);
let h='<style>body{margin:0;background:#fff;font:13px Arial,sans-serif;color:#111}.sec{display:inline-block;padding:14px;background:#fff}.sec h2{margin:0 0 8px;font-size:18px}.row{display:flex;gap:8px;margin-bottom:8px;align-items:flex-start}.tl{width:46px;font-weight:700;font-size:15px;padding-top:30px}.c{width:118px;text-align:center}.c img{width:84px;height:84px;object-fit:contain;background:#2a2f38;border-radius:8px;display:block;margin:0 auto 3px}.c b{display:block;font-size:12px;line-height:1.15}.c i{font-style:normal;color:#555;font-size:11px}</style>';
const out={};
for(const [g,f] of Object.entries(grp)){
  const L=all.filter(f).sort((a,b)=>b.tier-a.tier||ci(a.cat)-ci(b.cat)||a.name.localeCompare(b.name));
  if(!L.length)continue;out[g]=L.length;
  const tiers=[...new Set(L.map(t=>t.tier))];
  h+='<div class="sec" id="s_'+g+'"><h2>'+g+' ('+L.length+')</h2>'+tiers.map(T=>'<div class="row"><div class="tl">T'+T+'</div>'+L.filter(t=>t.tier==T).map(t=>'<div class="c"><img src="'+(ICD[t.name]||IC[t.name]||'')+'" alt=""><b>'+t.name+'</b><i>'+t.cls+t.tier+' · '+t.cat+(t.type?' · '+t.type:'')+(t.beast&&!t.type?' · Beast':'')+'</i></div>').join('')+'</div>').join('')+'</div><br>';
}
document.body.innerHTML=h;return out}"""
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1500,'height':900})
    pg.route('**/*',lambda r:r.continue_() if r.request.url.startswith('file:') else r.abort())
    pg.goto('file://'+os.path.join(ROOT,'index.inline.html'));pg.wait_for_timeout(800)
    out=pg.evaluate(JS);pg.wait_for_timeout(500)
    os.makedirs(OUT,exist_ok=True)
    for g in out:
        pg.locator('#s_'+g).screenshot(path=os.path.join(OUT,'troops_'+g+'.png'))
    open(os.path.join(OUT,'index.html'),'w').write('<!doctype html><meta charset="utf-8"><title>Troop icons</title>'+pg.evaluate("()=>document.documentElement.outerHTML"))
    print(out)
