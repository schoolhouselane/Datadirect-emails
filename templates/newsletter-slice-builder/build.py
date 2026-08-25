import base64
from PIL import Image
SLD="slices"
FULL=[  # (name, link, alt)
 ("s1","https://www.datadirect.ie/products","Your month in DataDirect — welcome. Explore the store."),
 ("s4",None,"Our winners: World Cup Top 4 and F1 Prize Draw. Our partners. Where we've been."),
 ("s5",None,"An afternoon with Kensington."),
 ("s6",None,"What we learned this month."),
 ("s7","https://www.datadirect.ie/it-solutions","Got a tricky problem? See examples of our work."),
 ("s8",None,"Fun fact — Merlin the Duck, Team Mexico's unofficial World Cup mascot."),
 ("s9",None,"More competitions; webinars and supplier visits."),
 ("s10","https://www.linkedin.com/company/data-direct/","Coming to our shop — something worth waiting for. Follow on LinkedIn."),
 ("s11",None,"Launching September — big deals on the way."),
 ("s12","mailto:sales@datadirect.ie","Over to you — we'd love to hear from you. Tell us what you think."),
 ("s13",None,"Thanks for reading. DataDirect."),
]
PCOLS=[("p1","https://www.datadirect.ie/product-details?productId=CQ00959","Apple iPhone Air 256GB, EUR 1058, view product"),
       ("p2","https://www.datadirect.ie/product-details?productId=CP28492","HP EliteBook 6 G1ah 16-inch, EUR 989, view product"),
       ("p3","https://www.datadirect.ie/product-details?productId=CQ00952","Samsung Galaxy Tab, EUR 156, view product")]
SEQ=["s1","PRODUCTS","s4","s5","s6","s7","s8","s9","s10","s11","s12","s13"]
def dh(n):
    w,h=Image.open(f"{SLD}/{n}.png").size; return round(h/2)
def dw(n):
    w,h=Image.open(f"{SLD}/{n}.png").size; return round(w/2)
def fullrow(n,link,alt,src):
    img=f'<img src="{src(n)}" width="600" height="{dh(n)}" alt="{alt}" style="display:block;width:100%;max-width:600px;height:auto;border:0;" />'
    if link: img=f'<a href="{link}" target="_blank" style="display:block;line-height:0;">{img}</a>'
    return f'<tr><td style="padding:0;font-size:0;line-height:0;">{img}</td></tr>'
def products(src):
    head=f'<tr><td style="padding:0;font-size:0;line-height:0;"><img src="{src("p-head")}" width="600" height="{dh("p-head")}" alt="Products of the week" style="display:block;width:100%;max-width:600px;height:auto;border:0;" /></td></tr>'
    tds=""
    for nm,url,alt in PCOLS:
        wpct=f'{Image.open(f"{SLD}/{nm}.png").size[0]/1200*100:.2f}%'
        img=f'<img src="{src(nm)}" width="{dw(nm)}" height="{dh(nm)}" alt="{alt}" style="display:block;width:100%;height:auto;border:0;" />'
        tds+=f'<td width="{wpct}" valign="top" style="padding:0;font-size:0;line-height:0;"><a href="{url}" target="_blank" style="display:block;line-height:0;">{img}</a></td>'
    row=f'<tr><td style="padding:0;font-size:0;line-height:0;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="width:100%;"><tr>{tds}</tr></table></td></tr>'
    return head+row
def body(src):
    d={n:(l,a) for n,l,a in FULL}
    out=[]
    for it in SEQ:
        if it=="PRODUCTS": out.append(products(src))
        else: l,a=d[it]; out.append(fullrow(it,l,a,src))
    return "\n".join(out)
def page(inner):
    return f'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "https://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head>
<meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Your Month in DataDirect</title>
<style>html,body{{margin:0!important;padding:0!important}}body{{background:#efe9f2}}img{{border:0;display:block;-ms-interpolation-mode:bicubic}}table{{border-collapse:collapse!important}}</style>
</head><body style="margin:0;padding:0;background:#efe9f2;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;color:#efe9f2;font-size:1px;">Your month in DataDirect — products of the week, winners, a fun fact, and what's coming next.</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#efe9f2;"><tr><td align="center" style="padding:0;">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" border="0" style="width:100%;max-width:600px;">
{inner}
</table></td></tr></table></body></html>'''
import sys
if __name__=="__main__":
    open("index.html","w").write(page(body(lambda n:f"slices/{n}.png")))
    print("wrote index.html")
