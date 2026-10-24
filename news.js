(function(){
var ul=document.getElementById('news');if(!ul)return;
var FB=[{"source": "SEBI", "title": "Commodity derivatives: new penalty formula and position limits", "summary": "Revises the penalty formula for position limit breaches, the definition of “Broad Commodity” and client-level position limits.", "url": "https://www.sebi.gov.in", "date": "2026-09-09"}, {"source": "SEBI", "title": "ETF price band circular: deadline moved to 7 September", "summary": "Implementation of the 15 June 2026 circular on ETF base price, price bands and pre-open call auction was pushed from 1 to 7 September.", "url": "https://www.sebi.gov.in", "date": "2026-08-28"}, {"source": "SEBI", "title": "FPIs can sign powers of attorney to custodians digitally", "summary": "Digital signatures under the IT Act are accepted, so notarisation, apostille and consularisation are no longer required.", "url": "https://www.sebi.gov.in", "date": "2026-08-20"}, {"source": "SEBI", "title": "Privately placed municipal bonds: face value and escrow norms", "summary": "Sets ₹1 lakh and ₹10,000 face value norms, adds SPV escrow rules and extends financial result filing deadlines.", "url": "https://www.sebi.gov.in", "date": "2026-08-11"}, {"source": "SEBI", "title": "Digital accessibility audits: deadline extended to 31 October 2026", "summary": "Regulated entities get more time to complete accessibility audits and fix the findings. Other obligations are unchanged.", "url": "https://www.sebi.gov.in", "date": "2026-07-31"}, {"source": "SEBI", "title": "GARUDA mechanism lets AIFs launch schemes faster", "summary": "AIF schemes can launch without waiting for SEBI’s PPM review, using merchant banker certification or self-certification.", "url": "https://www.sebi.gov.in", "date": "2026-07-30"}, {"source": "RBI", "title": "Amendment directions on matters to be placed before bank boards", "summary": "Amends the directions on what banks must put before their boards, effective 1 October 2026.", "url": "https://www.rbi.org.in", "date": "2026-07-15"}, {"source": "SEBI", "title": "Custodian fee moves from annual to monthly", "summary": "Replaces the annual fee with a monthly fee payable within 15 days of month-end, effective 1 October 2026.", "url": "https://www.sebi.gov.in", "date": "2026-07-03"}, {"source": "GST & Customs", "title": "Notification 21/2026-Customs (T): duty exemption for tariff item 26020010", "summary": "Amends Notification 62/2022-Customs to exempt goods under this tariff item from basic customs duty.", "url": "https://www.cbic.gov.in", "date": "2026-06-09"}, {"source": "GST & Customs", "title": "Notification 01/2026-Central Tax (Rate): beverage rates aligned", "summary": "Updates the list of goods with specific GST rates to match the Finance Act 2026.", "url": "https://www.cbic.gov.in", "date": "2026-04-30"}];
var ch=document.getElementById('chips'),up=document.getElementById('upd'),more=document.getElementById('more'),cur='all',step=12,lim=step,cap=+ul.dataset.cap||0;
function fmt(d){var x=new Date(d);return isNaN(x)?'':x.toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})}
function apply(){if(ch)Array.prototype.forEach.call(ch.children,function(b){b.setAttribute('aria-pressed',b.dataset.s===cur)});
 var n=0;Array.prototype.forEach.call(ul.children,function(l){var m=cur==='all'||l.dataset.k===cur;if(m)n++;l.hidden=!m||(!cap&&n>lim)});
 if(more)more.hidden=n<=lim}
function render(items,upd){
 if(cap)items=items.slice(0,cap);
 ul.textContent='';cur='all';lim=step;
 items.forEach(function(i){var li=document.createElement('li');li.dataset.k=i.source;
  li.innerHTML='<time></time><div><small></small><h3></h3><p></p></div><a>Official source</a>';
  li.querySelector('time').textContent=fmt(i.date);li.querySelector('small').textContent=i.source;
  li.querySelector('h3').textContent=i.title;li.querySelector('p').textContent=i.summary||'';
  if(/^https?:\/\//.test(i.url))li.querySelector('a').href=i.url;
  ul.appendChild(li)});
 if(ch){ch.textContent='';
  ['all'].concat(items.map(function(i){return i.source}).filter(function(v,j,a){return a.indexOf(v)===j})).forEach(function(v){
   var b=document.createElement('button');b.type='button';b.dataset.s=v;b.textContent=v==='all'?'All':v;
   b.onclick=function(){cur=v;lim=step;apply()};ch.appendChild(b)})}
 if(up&&upd&&fmt(upd))up.textContent=fmt(upd);apply()}
if(more)more.onclick=function(){lim+=step;apply()};
render(FB);
fetch('updates.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():Promise.reject()}).then(function(d){
 if(d&&d.items&&d.items.length)render(d.items,d.updated)}).catch(function(){});
})();
