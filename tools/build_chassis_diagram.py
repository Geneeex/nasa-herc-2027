from pathlib import Path
import html, json
from PIL import Image, ImageDraw, ImageFont

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"diagrams"
OUT.mkdir(parents=True, exist_ok=True)
W,H=1920,1400
im=Image.new("RGB",(W,H),"#FFFFFF")
d=ImageDraw.Draw(im)
parts=[]
records=[]
C={"ink":"#142B43","muted":"#4D6277","power":"#BA7417","control":"#1666AC","torque":"#197355","support":"#758390","pale":"#F3F6F9","blue":"#EBF3FC","amber":"#FFF4E3","green":"#EDF7F2","rule":"#D6DFE7"}
def font(size,bold=False):
    import os
    candidates = [
        Path(os.environ.get("ROVER_DIAGRAM_FONT_DIR", "C:/Windows/Fonts"))/("arialbd.ttf" if bold else "arial.ttf"),
        Path("/usr/share/fonts/truetype/liberation2")/("LiberationSans-Bold.ttf" if bold else "LiberationSans-Regular.ttf"),
        Path("/usr/share/fonts/truetype/dejavu")/("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists(): return ImageFont.truetype(str(candidate),size)
    raise RuntimeError("Install Arial or Liberation Sans, or set ROVER_DIAGRAM_FONT_DIR.")
def rect(x,y,w,h,fill="#FFFFFF",stroke=None,r=10,lw=2):
    d.rounded_rectangle((x,y,x+w,y+h), radius=r, fill=fill, outline=stroke, width=lw)
    border=f"border:{lw}px solid {stroke};" if stroke else ""
    parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{fill};{border}border-radius:{r}px;box-sizing:border-box;"></div>')
def text(s,x,y,size=23,color=None,bold=False,align="left",width=None):
    color=color or C["ink"]
    f=font(size,bold)
    tw=d.textlength(s,font=f)
    if width is not None and tw > width+1:
        raise ValueError(f"Text too wide {tw:.1f}>{width}: {s}")
    px=x-tw/2 if align=="center" else (x-tw if align=="right" else x)
    d.text((px,y),s,font=f,fill=color,anchor="lt")
    # Each text line has explicit position, retaining separate text elements on import.
    parts.append(f'<div style="position:absolute;left:{px:.2f}px;top:{y}px;width:{tw+6:.2f}px;height:{size*1.3:.1f}px;font:{"700" if bold else "400"} {size}px Arial,sans-serif;line-height:1;color:{color};white-space:nowrap;">{html.escape(s)}</div>')
    records.append({"text":s,"x":round(px,2),"y":y,"width":round(tw,2),"font_size":size})
def line(points,color,lw=3,dashed=False,arrow=False):
    for (x1,y1),(x2,y2) in zip(points,points[1:]):
        assert x1==x2 or y1==y2
        if dashed:
            dist=abs(x2-x1)+abs(y2-y1)
            for off in range(0,dist,13):
                end=min(off+7,dist)
                if x1==x2:
                    sign=1 if y2>y1 else -1
                    d.line((x1,y1+off*sign,x2,y1+end*sign),fill=color,width=lw)
                else:
                    sign=1 if x2>x1 else -1
                    d.line((x1+off*sign,y1,x1+end*sign,y2),fill=color,width=lw)
        else:
            d.line((x1,y1,x2,y2),fill=color,width=lw)
        if x1==x2:
            style=f'left:{x1-lw/2}px;top:{min(y1,y2)}px;width:0;height:{abs(y2-y1)}px;border-left:{lw}px {"dashed" if dashed else "solid"} {color};'
        else:
            style=f'left:{min(x1,x2)}px;top:{y1-lw/2}px;width:{abs(x2-x1)}px;height:0;border-top:{lw}px {"dashed" if dashed else "solid"} {color};'
        parts.append(f'<div style="position:absolute;{style}"></div>')
    if arrow:
        x,y=points[-1];xp,yp=points[-2];a=11
        if x>xp:
            tri=[(x,y),(x-a,y-a/2),(x-a,y+a/2)]
            sty=f"left:{x-a}px;top:{y-a/2}px;border-top:{a/2}px solid transparent;border-bottom:{a/2}px solid transparent;border-left:{a}px solid {color};"
        elif x<xp:
            tri=[(x,y),(x+a,y-a/2),(x+a,y+a/2)]
            sty=f"left:{x}px;top:{y-a/2}px;border-top:{a/2}px solid transparent;border-bottom:{a/2}px solid transparent;border-right:{a}px solid {color};"
        elif y>yp:
            tri=[(x,y),(x-a/2,y-a),(x+a/2,y-a)]
            sty=f"left:{x-a/2}px;top:{y-a}px;border-left:{a/2}px solid transparent;border-right:{a/2}px solid transparent;border-top:{a}px solid {color};"
        else:
            tri=[(x,y),(x-a/2,y+a),(x+a/2,y+a)]
            sty=f"left:{x-a/2}px;top:{y}px;border-left:{a/2}px solid transparent;border-right:{a/2}px solid transparent;border-bottom:{a}px solid {color};"
        d.polygon(tri,fill=color)
        parts.append(f'<div style="position:absolute;width:0;height:0;{sty}"></div>')
def box(x,y,w,h,head,body,kind="pale",headsize=25,bodysize=22):
    rect(x,y,w,h,C[kind],C["rule"])
    text(head,x+w/2,y+17,headsize,bold=True,align="center",width=w-20)
    for i,s in enumerate(body):
        text(s,x+w/2,y+52+i*27,bodysize,color=C["muted"],align="center",width=w-20)

# Identity and flow key
text("NASA HERC 2027 TEAM BANGLADESH",60,40,22,C["control"],True)
text("Chassis & drive system",60,80,48,bold=True)
text("Our four-wheel drive architecture",61,139,23,C["muted"])
for x,label,key in [(1080,"Power","power"),(1270,"Control","control"),(1470,"Torque","torque"),(1655,"Support","support")]:
    line([(x,100),(x+40,100)],C[key],3,key=="support",True)
    text(label,x+52,87,22,C["muted"])

# Electrical feed
text("DRIVE POWER",60,187,19,C["power"],True)
box(60,222,330,104,"3S drive battery",["11.1 V nominal | 5000 mAh","12.6 V fully charged"],"amber",25,21)
box(480,222,190,104,"Main fuse",["Rating to be verified"],"amber",25,18)
box(760,222,300,104,"Disconnect switch",["Accessible isolation"],"amber")
box(1150,222,440,104,"Power distribution",["Insulated positive and return wiring"],"amber",25,21)
for a,b in [(390,480),(670,760),(1060,1150)]:
    line([(a,274),(b,274)],C["power"],4,arrow=True)

# Main battery supply splits to each ESC; outside route avoids control wiring.
line([(1370,326),(1370,346),(35,346),(35,628),(220,628)],C["power"],4,arrow=True)
line([(1370,346),(1470,346),(1470,556)],C["power"],4,arrow=True)

# Radio control and its own handheld supply
box(230,400,350,107,"FlySky FS-i6X",["AA-powered handheld","Throttle + steering mixing"],"blue",25,21)
box(760,400,350,107,"FS-iA10B receiver",["Separate left / right commands"],"blue",25,20)
line([(580,450),(760,450)],C["control"],3,True,True)
text("Wireless RC",670,419,19,C["control"],align="center")

# Distinct PWM outputs
line([(840,507),(840,534),(610,534),(610,556)],C["control"],3,arrow=True)
text("Left PWM + ground",746,512,18,C["control"],align="center")
line([(1110,449),(1130,449),(1130,643),(1190,643)],C["control"],3,arrow=True)
text("Right PWM + ground",1155,523,18,C["control"])

# Two ESCs; controls enter independently from the power input.
box(220,556,470,144,"LEFT ESC",["New Rain brushed ESC","Controls both left motors"],"blue",29,23)
box(1190,556,470,144,"RIGHT ESC",["New Rain brushed ESC","Controls both right motors","BEC + insulated; signal ground retained"],"blue",29,20)
text("One compatible ESC BEC powers receiver",950,363,20,C["power"],align="center")
# Single BEC connection runs above the radio blocks, without joining main feed.
line([(300,556),(300,532),(190,532),(190,373),(740,373),(740,421),(760,421)],C["power"],3,arrow=True)
# BEC label placed above receiver with leader-free meaning carried by the line color.


text("Configured output cap + link-loss stopping",907,602,19,C["ink"],True,align="center",width=435)
text("Within the ESC / radio control settings",907,632,18,C["muted"],align="center",width=435)

# Parallel ESC output branches; each motor gets both reversible output wires.
xs=[310,640,1260,1590]
centers=[455,1425]
for mid,pair in zip(centers,[xs[:2],xs[2:]]):
    y=788
    line([(mid,700),(mid,y)],C["power"],4)
    line([(pair[0],y),(pair[1],y)],C["power"],4)
    for x in pair:
        line([(x,y),(x,816)],C["power"],4,arrow=True)
    text("Two motors in parallel",pair[0]-105,755,20,C["power"],True)

labels=["Front-left","Rear-left","Front-right","Rear-right"]
for x,label in zip(xs,labels):
    rect(x-94,816,188,49,C["amber"],C["rule"],8)
    text("Motor branch fuse",x,831,20,C["power"],True,align="center",width=177)
    line([(x,865),(x,898)],C["power"],4,arrow=True)
    box(x-139,898,278,96,label+" motor",["12 V | 200 RPM class"],"amber",24,21)
    line([(x,994),(x,1032)],C["torque"],4,arrow=True)
    box(x-153,1032,306,148,label+" wheel",["Clamping coupling","Bearing-supported spindle","PETG rim + TPU tyre"],"green",24,20)

# Shared mechanical supports. This is structural, not electrical.
line([(310,1206),(1590,1206)],C["support"],3,True)
for x in xs:
    line([(x,1206),(x,1180)],C["support"],3,True,True)
line([(949,1240),(949,1206)],C["support"],3,True)
box(171,1240,335,103,"6061-T6 chassis",["Aluminium structure"],"pale",24,22)
line([(506,1290),(610,1290)],C["support"],3,True,True)
box(610,1240,680,103,"4 arms | 8 springs | 4 dampers",
    ["Fixed-steering carriers  |  Secured pivots  |  Travel stops"],"pale",23,21)
box(1374,1240,365,103,"Wheel dimensions",["215 x 90 mm | 188 mm rim","13.5 mm rim-to-tread span"],"green",24,20)

# Footer statements are compact and accurate; no invented installed ratings.
text("Equal side commands: straight drive  |  Different side commands: skid steering",60,1354,19,C["ink"],True)
text("We verify below 8 km/h at full charge (12.6 V).",1855,1354,19,C["ink"],align="right")
# Detailed but concise implementation notes retained as editable Canva notes, avoiding a cluttered figure.
notes = """Our chassis and drive system block diagram.
Each ESC's two motors are connected in parallel, with an individual fuse on each motor branch.
Both motor wires connect to the reversible ESC output; neither motor terminal connects directly to battery ground.
Only one verified receiver-compatible BEC powers the receiver. Disconnect and insulate the other ESC's BEC positive/red lead, retaining both ESC PWM signal and ground connections.
We mount each motor and spindle-bearing support together to keep clamping couplings aligned throughout suspension travel.
One spring-and-damper unit plus one separate spring per wheel gives eight springs and four dampers. Combined wheel rate, preload and travel require loaded verification.
We will verify the supplied ESC voltage and current capability, proportional reverse, braking, fuse selection, neutral/endpoints, mixing, speed-limit configuration and link-loss stopping.
Wheel dimensions:215mm overall diameter,90mm width,188mm rim outer diameter,13.5mm radial tyre thickness including tread.
Equal left/right commands drive approximately straight; different side commands turn the rover. Opposite side directions allow a pivot turn where traction and torque permit.
The separate autonomous task-system architecture is included in two companion pages. This repository export reconciles the earlier local source with the later reviewed design; it does not edit the Canva original. Install one 100 nF suppression capacitor across each motor with short leads. All current and fuse ratings require acceptance testing.
"""
doc='<!doctype html><html><head><meta charset="utf-8"><title>NASA HERC 2027 TEAM BANGLADESH - Chassis and Drive System</title><style>*{box-sizing:border-box}body{margin:0;background:#fff}#page{position:relative;width:1920px;height:1400px;overflow:hidden;background:#fff}</style></head><body><section id="page" data-document-role="page" data-label="Chassis and drive system" data-speaker-notes="'+html.escape(notes,quote=True)+'">'+"".join(parts)+'</section></body></html>'
path=OUT/"NASA-HERC-2027-Chassis-Block-Diagram.html"
path.write_text(doc,encoding="utf-8")
im.save(OUT/"NASA-HERC-2027-Chassis-Block-Diagram.png")
(OUT/"Chassis-Diagram-Content.json").write_text(json.dumps({"size":[W,H],"text":records,"notes":notes},indent=2),encoding="utf-8")
print(path)
print(OUT/"NASA-HERC-2027-Chassis-Block-Diagram.png")

