from pathlib import Path
import html,json,math
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"diagrams"
OUT.mkdir(parents=True,exist_ok=True)
W,H=2400,1900
C={"ink":"#142B43","muted":"#4D6277","power":"#B56E12","control":"#1666AC","result":"#197355","ground":"#667580","pale":"#F3F6F9","blue":"#EBF3FC","amber":"#FFF4E3","green":"#EDF7F2","purple":"#76529D","violet":"#F3EDF8","rule":"#D6DFE7"}
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
class Page:
    def __init__(self,num,title,subtitle):
        self.num=num;self.title=title;self.parts=[];self.records=[];self.edges=[];self.boxes={}
        self.im=Image.new("RGB",(W,H),"white");self.d=ImageDraw.Draw(self.im)
        self.text("NASA HERC 2027 TEAM BANGLADESH",80,36,22,C["control"],True)
        self.text(title,80,82,48,bold=True)
        self.text(subtitle,80,145,24,C["muted"])
        self.text(f"{num:02d} / 02",2320,42,22,C["muted"],align="right")
    def rect(self,x,y,w,h,fill="white",stroke=None,r=12,lw=2):
        self.d.rounded_rectangle((x,y,x+w,y+h),radius=r,fill=fill,outline=stroke,width=lw)
        border=f"border:{lw}px solid {stroke};" if stroke else ""
        self.parts.append(f'<div style="position:absolute;left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{fill};{border}border-radius:{r}px;box-sizing:border-box"></div>')
    def text(self,s,x,y,size=23,color=None,bold=False,align="left",width=None):
        color=color or C["ink"];f=font(size,bold);tw=self.d.textlength(s,font=f)
        if width and tw>width+1:raise ValueError(f"P{self.num} {tw:.1f}>{width}: {s}")
        px=x-tw/2 if align=="center" else x-tw if align=="right" else x
        if px<0 or px+tw>W or y+size>H:raise ValueError(f"Offpage {s}")
        self.d.text((px,y),s,font=f,fill=color,anchor="lt")
        self.parts.append(f'<div style="position:absolute;left:{px:.2f}px;top:{y}px;width:{tw+8:.2f}px;height:{size*1.32:.1f}px;font:{"700" if bold else "400"} {size}px Arial,sans-serif;line-height:1;color:{color};white-space:nowrap">{html.escape(s)}</div>')
        self.records.append({"text":s,"x":round(px,2),"y":y,"width":round(tw,2),"size":size})
    def line(self,pts,key="control",lw=3,dash=False,arrow=True,label=None):
        col=C.get(key,key)
        for (x1,y1),(x2,y2) in zip(pts,pts[1:]):
            assert x1==x2 or y1==y2
            if dash:
                dist=int(abs(x2-x1)+abs(y2-y1))
                for off in range(0,dist,15):
                    end=min(off+8,dist);sgn=1 if x2>x1 or y2>y1 else -1
                    seg=(x1,y1+sgn*off,x2,y1+sgn*end) if x1==x2 else (x1+sgn*off,y1,x1+sgn*end,y2)
                    self.d.line(seg,fill=col,width=lw)
            else:self.d.line((x1,y1,x2,y2),fill=col,width=lw)
            if x1==x2:sty=f'left:{x1-lw/2}px;top:{min(y1,y2)}px;width:0;height:{abs(y2-y1)}px;border-left:{lw}px {"dashed" if dash else "solid"} {col};'
            else:sty=f'left:{min(x1,x2)}px;top:{y1-lw/2}px;width:{abs(x2-x1)}px;height:0;border-top:{lw}px {"dashed" if dash else "solid"} {col};'
            self.parts.append(f'<div style="position:absolute;{sty}"></div>')
        if arrow:
            x,y=pts[-1];xp,yp=pts[-2];a=12
            if x>xp:
                tri=[(x,y),(x-a,y-a/2),(x-a,y+a/2)];sty=f"left:{x-a}px;top:{y-a/2}px;border-top:{a/2}px solid transparent;border-bottom:{a/2}px solid transparent;border-left:{a}px solid {col};"
            elif x<xp:
                tri=[(x,y),(x+a,y-a/2),(x+a,y+a/2)];sty=f"left:{x}px;top:{y-a/2}px;border-top:{a/2}px solid transparent;border-bottom:{a/2}px solid transparent;border-right:{a}px solid {col};"
            elif y>yp:
                tri=[(x,y),(x-a/2,y-a),(x+a/2,y-a)];sty=f"left:{x-a/2}px;top:{y-a}px;border-left:{a/2}px solid transparent;border-right:{a/2}px solid transparent;border-top:{a}px solid {col};"
            else:
                tri=[(x,y),(x-a/2,y+a),(x+a/2,y+a)];sty=f"left:{x-a/2}px;top:{y}px;border-left:{a/2}px solid transparent;border-right:{a/2}px solid transparent;border-bottom:{a}px solid {col};"
            self.d.polygon(tri,fill=col);self.parts.append(f'<div style="position:absolute;width:0;height:0;{sty}"></div>')
        self.edges.append({"points":pts,"kind":key,"arrow":arrow,"label":label})
    def box(self,id,x,y,w,h,head,body=(),kind="pale",hs=26,bs=23,lh=30):
        self.rect(x,y,w,h,C[kind],C["rule"])
        self.text(head,x+w/2,y+17,hs,bold=True,align="center",width=w-26)
        for i,s in enumerate(body):
            if y+56+i*lh+bs>y+h-9:raise ValueError(f"Box too short: {id} {s}")
            self.text(s,x+w/2,y+56+i*lh,bs,C["muted"],align="center",width=w-28)
        self.boxes[id]={"x":x,"y":y,"w":w,"h":h,"head":head,"body":list(body)}
    def legend(self,items):
        x=1510
        for label,key in items:
            self.line([(x,151),(x+40,151)],key,3,dash=key=="ground")
            self.text(label,x+50,137,20,C["muted"])
            x+=275
    def finish(self,notes):
        path=OUT/f"NASA-HERC-2027-Task-Block-Diagram-{self.num:02d}.png"
        self.im.save(path)
        return '<section data-document-role="page" data-label="'+html.escape(self.title,quote=True)+'" data-speaker-notes="'+html.escape(notes,quote=True)+'" style="position:relative;width:2400px;height:1900px;overflow:hidden;background:white">'+"".join(self.parts)+'</section>'
p=Page(1,"Task system: power and hardware","Our dedicated task battery supplies four separate power branches.")
p.legend([("Power","power"),("Data / control","control"),("Ground return","ground")])
p.box("battery",80,235,420,122,"Task battery",["3S LiPo | 2200 mAh","11.1 V nominal | 12.6 V full"],"amber",27,23,29)
p.box("mainfuse",605,235,270,122,"7.5 A main fuse*",["Close to battery positive"],"amber",27,21)
p.box("switch",980,235,305,122,"Master switch",["Task power isolation"],"amber")
p.box("distribution",1390,235,400,122,"P+ distribution",["Switched battery positive","Four parallel fused branches"],"amber",27,22,29)
for a,b in [(500,605),(875,980),(1285,1390)]:p.line([(a,295),(b,295)],"power",4)
p.box("alarm",1920,235,400,122,"Per-cell voltage alarm",["Balance connector only","Audible warning; no Pi signal"],"violet",26,22,29)
p.line([(395,235),(395,198),(2120,198),(2120,235)],"purple",2,dash=True)
p.text("Separate battery balance lead",1480,174,19,C["purple"])
centers=[320,880,1440,2000];lefts=[80,640,1200,1760]
p.line([(1590,357),(1590,398)],"power",4,arrow=False)
p.line([(320,398),(2000,398)],"power",4,arrow=False)
for cx in centers:p.line([(cx,398),(cx,442)],"power",4)
fuses=["5 A branch fuse*","3 A branch fuse*","1 A branch fuse*","1 A branch fuse*"]
reg=[("EP-0225 Pi power board",["9-24 V DC input; one input only","USB-C PD: 5.15 V / 5 A"]),
     ("Hobbywing UBEC 3A",["Output set to 5 V","Pan servo + PWM buffer supply"]),
     ("DFR0379 converter 1",["Output set to 5.2 V","Dedicated LiDAR supply"]),
     ("DFR0379 converter 2",["Output set to 5.2 V","Dedicated tilt-servo supply"])]
loads=[("Raspberry Pi 5 - 8 GB",["Powers camera and USB devices","PCA9685 logic: Pi 3.3 V","64 GB microSD + active cooler","RTC battery retains the clock"]),
       ("MG996R + SN74AHCT125",["Pan servo and PWM buffer","Buffer supply remains at 5 V","Not powered from the Pi"]),
       ("TF03-100 LiDAR",["UART/CAN version: SEN0328","Revision-matched power cable","USB adapter VCC disconnected"]),
       ("FS90 tilt servo",["Positional FS90; not FS90R","Balanced, bearing-supported tilt","Separate from the pan supply"])]
for i,(x,cx) in enumerate(zip(lefts,centers)):
    p.box("branchfuse"+str(i),x,442,480,70,fuses[i],(),"amber",25)
    p.line([(cx,512),(cx,550)],"power",4)
    p.box("reg"+str(i),x,550,480,120,reg[i][0],reg[i][1],"amber",25,22,29)
    p.line([(cx,670),(cx,714)],"power",4)
    p.box("load"+str(i),x,714,480,187,loads[i][0],loads[i][1],"blue",25,22,29)
    p.line([(cx,901),(cx,951)],"ground",3,arrow=False)
p.line([(180,951),(2315,951)],"ground",4,arrow=False)
p.text("G_LOAD: task, USB and signal grounds",380,918,21,C["ground"],True)
p.box("battneg",80,1031,430,105,"Task battery negative",["Same battery shown above"],"pale",26,22)
p.box("kemo",845,1015,760,140,"Kemo M148A - switched negative return",["LOAD - to protected ground; BATTERY - to raw negative","Positive reference connects to P+; backup cutoff only"],"pale",26,23,30)
p.line([(2315,951),(2315,1080),(1605,1080)],"ground",4)
p.line([(845,1080),(510,1080)],"ground",4)
p.text("LOAD -",1690,1044,22,C["ground"],True)
p.text("BATTERY -",610,1044,22,C["ground"],True)
p.text("We isolate G_LOAD from raw battery negative, the chassis and drive-system ground.",80,1173,23,C["ground"],True)
p.text("* All five fuse ratings are provisional: verify load, inrush and wiring. Keep regulated positives separate.",80,1208,21,C["muted"])
p.text("SIGNAL CONNECTIONS",80,1261,22,C["control"],True)
p.text("Repeated device names below identify the same installed units shown above.",780,1264,21,C["muted"])
# Interfaces: transport labels are placed above each connector.
p.box("sdr",80,1320,420,90,"VHF antenna + RTL-SDR",["144-148 MHz receive only"],"blue",24,21)
p.box("pi-radio",675,1320,380,90,"Raspberry Pi 5",["rtl_fm + Dire Wolf"],"blue",25,21)
p.line([(500,1365),(675,1365)],"control",3)
p.text("USB",585,1324,21,C["control"],align="center")
p.box("camera",1280,1320,410,90,"Camera Module 3",["CSI camera interface"],"blue",25,21)
p.box("pi-camera",1920,1320,400,90,"Raspberry Pi 5",["Image capture / autofocus"],"blue",25,21)
p.line([(1690,1365),(1920,1365)],"control",3)
p.line([(1920,1380),(1690,1380)],"control",2)
p.text("CSI",1805,1324,21,C["control"],align="center")
p.box("pi-pwm",80,1450,320,90,"Raspberry Pi 5",["3.3 V logic"],"blue",25,21)
p.box("pca",565,1450,480,90,"PCA9685",["VCC and I2C pull-ups: 3.3 V"],"blue",25,21)
p.box("buffer",1300,1450,480,90,"SN74AHCT125",["3.3 V input to 5 V PWM output"],"blue",25,21)
p.box("mg",1960,1450,360,90,"MG996R",["Shared-platform pan"],"blue",25,21)
p.line([(400,1495),(565,1495)],"control",3);p.text("I2C",482,1453,21,C["control"],align="center")
p.line([(1045,1495),(1300,1495)],"control",3);p.text("3.3 V PWM",1170,1453,21,C["control"],align="center")
p.line([(1780,1495),(1960,1495)],"control",3);p.text("5 V PWM",1870,1453,21,C["control"],align="center")
p.box("pca-tilt",80,1580,420,90,"PCA9685 - second channel",["Same servo update frequency"],"blue",23,21)
p.box("fs",675,1580,380,90,"FS90",["LiDAR elevation"],"blue",25,21)
p.line([(500,1625),(675,1625)],"control",3);p.text("3.3 V PWM",585,1584,19,C["control"],align="center")
p.box("tf-data",1280,1580,330,90,"TF03-100",["Range frames"],"blue",25,21)
p.box("cp-data",1750,1580,300,90,"CP2102",["3.3 V logic"],"blue",25,21)
p.box("pi-range",2180,1580,140,90,"Pi 5",["USB"],"blue",25,21)
p.line([(1610,1625),(1750,1625)],"control",3)
p.line([(1750,1640),(1610,1640)],"control",2)
p.text("UART",1680,1584,20,C["control"],align="center")
p.line([(2050,1625),(2180,1625)],"control",3);p.text("USB",2115,1584,20,C["control"],align="center")
p.box("pi-display",80,1710,420,90,"Raspberry Pi 5",["Local results viewer"],"blue",25,21)
p.box("display",675,1710,520,90,"Onboard HDMI touchscreen",["HDMI video; USB touch and power"],"blue",25,21)
p.line([(500,1755),(675,1755)],"control",3)
p.line([(675,1770),(500,1770)],"control",2)
p.text("USB touch",585,1782,18,C["control"],align="center")
p.text("HDMI / USB",585,1714,19,C["control"],align="center")
p.text("UART: 115200 baud, 8N1; cross TX/RX and join G_LOAD.",1280,1720,23,C["muted"])
p.text("Keep separate servo positives off the PCA9685 shared V+ bus.",1280,1755,23,C["muted"])
p.text("We verify 5 A PD negotiation, USB/fan draw and loaded supply stability before use.",80,1840,23,C["ink"],True)
p.text("Power / interface architecture",2320,1840,21,C["muted"],align="right")
notes1="""Task-system power and interfaces, based on the reviewed task-process description and Tasks_Final_Purchase_List.docx.
One installed 3S 2200 mAh LiPo task battery (24.42 Wh nominal), separate from drive battery.
Main and four input-branch fuses: 7.5 A, 5 A, 3 A, 1 A, 1 A, all provisional pending measured load/inrush and wiring checks.
Kemo M148A switches the negative return. Its LOAD- terminal is G_LOAD; BATTERY- is raw task battery negative. Its positive reference/common positive terminals connect as the manufacturer specifies to the switched positive supply. G_LOAD must not be bypassed through chassis, drive wiring, USB shields or externally connected equipment.
Per-cell alarm connects only to the battery balance connector and provides audible warning. No automatic Pi shutdown signal is assumed. Guard cutoff is pack-level backup, not individual-cell protection or orderly shutdown. Save promptly, prove endurance through PER, shut the Pi down in software before removing supply.
EP-0225 uses DC input only; confirm 5 A USB-PD negotiation and the combined 1.6 A USB/fan limit where applicable. The RTC battery retains time and is not Pi operating power.
Hobbywing UBEC set to 5 V feeds MG996R and SN74AHCT125. DFR0379 converters independently supply TF03 and FS90 at 5.2 V. Servo positives do not join through the PCA9685 V+ bus.
PCA9685 uses Pi 3.3 V VCC and I2C pullups. A common servo frequency serves both channels. AHCT125 buffer powered at 5 V; define enable/unused inputs and fit bypass capacitor. FS90 accepts 3.3 V control; verify actual delivered servo. FS90 is positional, not FS90R.
TF03 is the UART/CAN SEN0328 variant with revision-matched wiring, 3.3 V UART and 115200 8N1. Adapter TX to sensor RX, RX to sensor TX, ground to G_LOAD, VCC left unconnected. Use firmware-specific frame validation, not a different sensor's error thresholds.
Repeated Pi/PCA names in interface rows represent the same installed devices, not additional units.
Sources: https://wiki-md.52pi.com/docs/EP-0225 ; https://www.kemo-electronic.de/en/Car/Modules/M148A-Battery-guard-12-V-DC.php ; https://wiki.dfrobot.com/sen0328/ ; https://wiki.dfrobot.com/sen0328/docs/21565 ; https://www.ti.com/product/SN74AHCT125 ; https://www.pololu.com/product/2818 ; https://www.raspberrypi.com/documentation/computers/raspberry-pi.html
"""
pages=[p];sections=[p.finish(notes1)]


p=Page(2,"Task system: autonomous command flow","We execute NASA's live commands and save each result on the rover.")
p.legend([("Live commands","control"),("Action / result","result"),("Next command","ground")])
p.box("manual",80,235,420,148,"We position and align",["Set the starting camera reference","Check the date, time and battery","Manual setup ends before the task"],"pale",25,21,29)
p.box("broadcast",630,235,420,148,"NASA VHF broadcast",["NASA channel within 144-148 MHz","30-second broadcast intervals","No radio transmission from us"],"blue",25,21,29)
p.box("receiver",1160,235,510,148,"RTL-SDR + rtl_fm",["Receive RF and demodulate FM","Receiver runs while actions execute"],"blue",26,22,30)
p.box("decoder",1780,235,540,148,"Dire Wolf",["Live 1200-baud AX.25/APRS decode","Local decoded packets to the Pi"],"blue",26,22,30)
p.line([(1050,301),(1160,301)],"control",4)
p.line([(1670,301),(1780,301)],"control",4)
p.box("armed",80,446,420,116,"Task controller ready",["Wait for the live begin command","No stored competition sequence"],"pale",25,21,29)
p.line([(290,383),(290,446)],"ground",3,dash=True)
p.box("dispatcher",680,438,900,145,"Execute the next received command",["Sequence status | commanded bearing | active filter","One stateful controller on our Raspberry Pi 5"],"blue",31,25,33)
p.box("parser",1780,446,540,129,"NASA-format parser + queue",["Accept valid commands in received order","Handle framing and repeats as specified"],"blue",26,21,29)
p.line([(2050,383),(2050,446)],"control",4)
p.line([(1780,508),(1580,508)],"control",4)
p.line([(500,504),(680,504)],"ground",3,dash=True)
p.text("One matching branch per received command.",1300,608,24,C["control"],True)
xs=[60,448,836,1224,1612,2000];cw=340;cs=[x+cw/2 for x in xs]
p.line([(1150,583),(1150,661)],"control",4,arrow=False)
p.line([(cs[0],661),(cs[-1],661)],"control",4,arrow=False)
for cx in cs:p.line([(cx,661),(cx,705)],"control",4)
heads=[("AAA","Begin sequence"),("B / C","Turn view"),("E / F / G","Select filter"),("D","Take picture"),("H","Distance to target"),("ZZZ","End sequence")]
for i,(x,(code,label)) in enumerate(zip(xs,heads)):
    p.box("cmd"+str(i),x,705,cw,115,code,[label],"blue",36,23)
    p.line([(x+cw/2,820),(x+cw/2,858)],"result",4)
handlers=[
("Begin the run",["Open the sequence record","Use NASA-defined start rules","Log the received commands"]),
("Pan the platform",["B: 30 degrees right","C: 30 degrees left","PCA9685 to PWM buffer","MG996R rotates the platform","Wait for movement to settle","Update commanded bearing"]),
("Replace active filter",["E: Red","F: Blue","G: Unfiltered / normal colour","Replace the previous filter","No stacked filter effects"]),
("Capture a fresh frame",["Wait for movement and autofocus","Acquire a new Camera 3 frame","Apply the current filter","Record capture date and time","Save the timestamped image"]),
("Measure intended target",["Use target in commanded view","Aim using calibrated alignment","Wait for aiming to settle","Validate fresh TF03 frames","Apply agreed reference correction","Divide corrected cm by 30.48","Retry within a set time limit","Restore commanded view","Save range or flag invalid data"]),
("Close the sequence",["Finish and retain the run record","Keep images and distances","Prepare the onboard results view","No editing or pit processing"])]
for i,(x,(head,body)) in enumerate(zip(xs,handlers)):
    p.box("action"+str(i),x,858,cw,353,head,body,"green",24,20,31)
    p.line([(x+cw/2,1211),(x+cw/2,1280)],"result",4)
p.box("record",60,1280,2280,138,"Our microSD run record",["Timestamped photographs | distances and target association | received commands | valid / error status","We save results as the commands complete; ZZZ closes the sequence."],"green",31,25,33)
# Completed nonterminal commands return to the dispatcher. The path never implies a preset sequence.
p.line([(550,1418),(550,1463),(28,1463),(28,625),(710,625),(710,583)],"ground",3,True)
p.text("While the sequence is active: wait for the next received command",70,1478,23,C["ground"],True)
p.line([(1880,1418),(1880,1545)],"result",4)
p.text("After ZZZ",1930,1465,24,C["result"],True)
p.box("checks",60,1550,1215,177,"We verify before accepting the system",["NASA message format, maximum pan travel and distance reference","Target alignment, fresh captures, valid range frames and timestamps","Power stability, USB load, RF interference and endurance through PER"],"pale",27,23,33)
p.box("per",1390,1545,950,184,"Onboard HDMI touchscreen",["Our pilots show the image gallery and distance log at PER","Results are ready locally; no return to the pit","We shut down the Pi before switching off its battery"],"green",29,24,33)
p.text("TEST TARGETS",60,1781,21,C["control"],True)
p.text("4 ft x 4 ft white boards | red circle: 12 in diameter | blue square: 12 in side | green triangle: 12 in height",245,1780,23,C["ink"])
p.text("Up to 50 ft from the starting point; shapes at least 1 ft above ground. G means no filter.",60,1820,23,C["muted"])
p.text("Process architecture - not a pre-programmed run sequence",2340,1860,20,C["muted"],align="right")
notes2="""Autonomous task execution; hardware and separate task-power rails are on page 1 of this same design.
After manual positioning/alignment, all task operations execute onboard without further pilot aiming, filtering, triggering or distance entry. Radio reception continues independently while movement, autofocus, capture, ranging and storage run.
Live path: NASA 144-148 MHz receive-only signal -> RTL-SDR Blog V3 -> rtl_fm FM audio -> Dire Wolf 1200-baud AX.25/APRS decoder -> NASA-format parser and ordered command queue -> Raspberry Pi task controller.
Branch fanout means one matching action per received command, not a fixed order AAA/B/C/E/F/G/D/H/ZZZ. Thirty seconds describes NASA broadcast timing, not a timer that creates onboard commands. Packet framing, transmitter identity, start-state behavior and handling of repeated transmissions follow NASA's published format; do not globally deduplicate commands by letter.
AAA begins sequence; B/C move commanded field of view 30 degrees right/left; E/F/G replace active filter with red/blue/unfiltered; D acquires a fresh timestamped image after motion and autofocus settle; H ranges the target associated with the commanded view; ZZZ closes the sequence and leaves results available.
The controller retains commanded bearing, filter and sequence state. No assumed AAA reset of bearing/filter. B/C cumulative travel must fit the actual delivered MG996R Robot 180 positional servo and cable travel; NASA maximum travel is still to be confirmed.
D: avoid queued pre-command frames. Map capture metadata to the checked Pi calendar clock; RTC backup does not establish correct time by itself. Apply the selected filter onboard and save the photograph with capture date/time. Processing is completed before PER.
H: use the unfiltered camera view to validate the intended target, compensate camera/LiDAR parallax through calibration, aim and wait for settling. Read only fresh TF03 frames, validate checksum and firmware-specific status/error values, and reject stale/invalid/background measurements. CP2102 link is 3.3 V TTL, 115200 8N1, with adapter VCC disconnected. Centimetres divided by 30.48 gives feet. Raw sensor-to-surface range is not automatically horizontal distance from the ground start mark. NASA's RC measurement reference/tolerance must be confirmed before the final correction is accepted; HP's 3-foot allowance must not be assumed. Retry the same target within a defined limit when acquisition or reading validation fails. Preserve the active filter; restore commanded view after temporary H aiming on success or failure. The retry is recovery, not a validated alternate range sensor.
Every received command and result updates the local run record. Nonterminal actions return to the queue; ZZZ closes the run for the onboard touchscreen gallery and distance log. Pilots may show the ready results at PER without pit return or subsequent processing. The audible per-cell alarm does not automatically tell the Pi to shut down.
Reference targets: 4-by-4-foot white boards, filled red circle diameter12in; blue square side12in; green equilateral triangle height12in, not side12in. Shapes at least1ft above ground; targets no farther than50ft from startingpoint.
Sources: NASA2027HERC Handbook printed pages40-42, https://www.nasa.gov/wp-content/uploads/2026/08/2027-herc-handbook-layout-aug6-508-1.pdf ; https://github.com/wb2osz/direwolf ; https://datasheets.raspberrypi.com/camera/picamera2-manual.pdf ; https://wiki.dfrobot.com/sen0328/docs/21565
"""
pages.append(p);sections.append(p.finish(notes2))
doc='<!doctype html><html><head><meta charset="utf-8"><title>NASA HERC 2027 TEAM BANGLADESH - Autonomous Task System</title><style>*{box-sizing:border-box}body{margin:0;background:white}</style></head><body>'+"\n".join(sections)+'</body></html>'
dest=OUT/"NASA-HERC-2027-Task-Block-Diagram.html"
dest.write_text(doc,encoding="utf-8")
(OUT/"Task-Diagram-Content.json").write_text(json.dumps({"page_size":[W,H],"pages":[{"number":pg.num,"title":pg.title,"text":pg.records,"boxes":pg.boxes,"edges":pg.edges} for pg in pages],"notes":[notes1,notes2]},ensure_ascii=False,indent=2),encoding="utf-8")
print(str(dest))
for pg in pages:print(str(OUT/f"NASA-HERC-2027-Task-Block-Diagram-{pg.num:02d}.png"))



