from icalendar_light.toolbox import Calendar
from datetime import datetime as dt
import datetime
import pygame as pg
import pygame
import time
import math
from datetime import date
from dateutil.relativedelta import relativedelta, SU
pg.init()
pg.font.init()

hw=2160
hh=3840

class CalSquare:
    def __init__(self,rect,date):
        self.rect=rect
        self.date=date

#w=360
#h=640
w = 1280
h=720
scalerh = h/hh
scalerw = w/hw

#cal pos
caldistfromxedge=50
percentdown = hh*(1-0.33333)

calulx=caldistfromxedge
caluly=hh-percentdown
callrx=hw-caldistfromxedge
callry=hh-20

calwid = callrx-calulx
calhei = callry-caluly
weekwid = calwid/7
weekhei = calhei/4
def GetPix(x,y):
    return int(math.ceil(x*scalerw)),int(math.ceil(y*scalerh))

def CreateRect(x1,y1,x2,y2):
    wid = x2-x1
    hi = y2-y1
    x = pg.Rect(GetPix(x1,y1),GetPix(wid,hi))
    return x

def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = rect
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]
    #print(fontHeight)

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    #return text
    return y-rect.top
rects = []

def get_last_sunday():
   
    today = date.today()
    last_sunday = today + relativedelta(weekday=SU(-1))
    return last_sunday
    #return last_monday.strftime("%Y-%m-%d")

print(get_last_sunday())
        
def UpdateCalSquares():
    calsquares = []
    tempvar1=calulx
    tempvar2=caluly
    datenum = 0
    last_sunday = get_last_sunday()
    for y in range(1,5):
        for x in range(1,8):
            rectval = CreateRect(tempvar1,tempvar2,tempvar1+weekwid,tempvar2+weekhei)
            #tempvar2=tempvar2+weekhei
            newdate = last_sunday + datetime.timedelta(days=datenum)
            temcal = CalSquare(rectval,newdate)
            datenum = datenum +1
            calsquares.append(temcal)
            tempvar1=tempvar1+weekwid
        tempvar2=tempvar2+weekhei
        tempvar1 = calulx


    tempvar2=caluly
    return calsquares




print(1920*scalerh)


print(GetPix(1080,1920))

white = (255,255,255)
black = (0,0,0)
screen=pg.display.set_mode([w, h])



font = pg.font.Font('freesansbold.ttf',32)
calfont = pg.font.Font("freesansbold.ttf",12)
text=font.render(str(dt.today().date()),True,black)
textRect=text.get_rect()
textRect.topleft=GetPix(0,0)


rects.append(CreateRect(calulx,caluly,callrx,callry))

today = dt.today().date()
for event in Calendar.iter_events_from_file('calc.ics'):
    if event[5].date() == today:
        print(" ")
        print(event[5].date())
        print(Calendar.event_stringify(event))


def GetCalTextForDay(date):
    text = ""
    for event in Calendar.iter_events_from_file('calc.ics'):
        if event[5].date()==date:
            if str(event[5].time())=="00:00:00" and str(event[6].time()) == "00:00:00":
                text = text + event[8] + "\n"
            else:
                text = text + (event[8]+":"+str(event[5].time()) + " - " +str(event[6].time()) + "\n")
    return text

def DrawCalData(screen,text,color,rect,font):
    y=0
    
    list = text.split("\n")
    for l in list:
        x = rect.x
        ry = rect.y
        w = rect.w
        h = rect.h
        ry = ry + y
        goodrect = pygame.Rect(x,ry,w,h)
        newy = drawText(screen,l,color,goodrect,font,aa=True)
        y = y + newy
        print(newy)
while True:
    screen.fill((0,255,0))
    screen.blit(text,textRect)

    for rect in rects:
        pg.draw.rect(screen,black,rect,width=1)
        #pg.

    cs = UpdateCalSquares()
    #print(cs)
    for square in cs:
        pg.draw.rect(screen,black,square.rect,width=1)
        #drawText(screen,GetCalTextForDay(square.date),black,square.rect,calfont,True)
        #drawText(screen,"aaa",black,square.rect,font)
        DrawCalData(screen,GetCalTextForDay(square.date),black,square.rect,calfont)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
    pg.display.update()
    time.sleep(1)
    text=font.render(str(dt.today()),True,black)
