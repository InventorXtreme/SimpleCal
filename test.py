from icalendar_light.toolbox import Calendar
from datetime import datetime as dt
import datetime
import pygame as pg
import pygame
import time
import math
from datetime import date
import urllib.request
import os
import random
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
#w = 1280
#h=720

w=1920
h=1080
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
global event_extras
event_extras = []

def DrawOutlineText(surf,x,y,colorf,colorb,text,aa,othic,font):
    image = font.render(text,aa,colorf)
    image2 = font.render(text,aa,colorb)
    surf.blit(image2,((x+othic),(y+othic)))
    surf.blit(image2,((x+othic),(y-othic)))
    surf.blit(image2,((x-othic),(y+othic)))
    surf.blit(image2,((x-othic),(y-othic)))
    surf.blit(image,(x,y))
def Rmdupe(listi):
    return list(dict.fromkeys(listi))

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
            image2 = font.render(text[:i],aa,(255,255,255))

        #surface.blit(image, (rect.left, y))

        #draw outline of text
        #surface.blit(image2, ((rect.left+1) , y+1))
        #surface.blit(image2, ((rect.left+1) , y-1))
        #surface.blit(image2, ((rect.left-1) , y-1))
        #surface.blit(image2, ((rect.left-1) , y+1))

        #draw real text
        #surface.blit(image,(rect.left,y))
        DrawOutlineText(surface,rect.left,y,black,white,text[:i],aa,1,font)
        
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
#black = (127,127,127)
black = (0,0,0)
#screen=pg.display.set_mode([w, h])
screen=pg.display.set_mode((0,0),pg.FULLSCREEN)


font = pg.font.Font('freesansbold.ttf',32)
calfont = pg.font.Font("freesansbold.ttf",12)
calfont2 = pg.font.Font("freesansbold.ttf",13)
text=font.render(str(dt.today().date()),True,black)
textRect=text.get_rect()
textRect.topleft=GetPix(0,0)


rects.append(CreateRect(calulx,caluly,callrx,callry))

today = dt.today().date()
# for event in Calendar.iter_events_from_file('calc.ics'):
#     if event[5].date() == today:
#         print(" ")
#         print(event[5].date())
#         print(Calendar.event_stringify(event))


def GetCalTextForDay(date):
    global event_extras
    text = ""
    

    for evente in Rmdupe(event_extras):
        if (evente[6].date() - datetime.timedelta(days=1)) == date:
            if str(evente[5].time())=="00:00:00" and str(evente[6].time()) == "00:00:00":
                text = text + "End: " + evente[8] + "\n"
            else:
                text = text + "End: " + evente[8] + " " + str(evente[6].strftime("%-I:%M %p"))
                
    
    for event in Calendar.iter_events_from_file('calc.ics'):
        
        if event[5].date()==date:
            if str(event[5].time())=="00:00:00" and str(event[6].time()) == "00:00:00":
                #text = text + event[8] + "\n"
                if event[5].date() == event[6].date() or event[5].date() == (event[6].date() - datetime.timedelta(days=1)):
                    text = text + event[8] + "\n"
                else:
                    text = text + "Start: " + event[8] + "\n"
                    event_extras.append(event)
            else:
                if event[5].date() == event[6].date():
                    text = text + (event[8]+" "+str(event[5].strftime("%-I:%M %p")) + " - " +str(event[6].strftime("%-I:%M %p")) + "\n")
                else:
                    text = text + ("Start: " + event[8]+" "+str(event[5].strftime("%-I:%M %p")) + " - " +str(event[6].strftime("%-I:%M %p")) + "\n")
                    event_extras.append(event)

            #if event[8][0] == "E" and event[8][1] == "v":
            #    print(event)
            
        
    return text

def DrawCalData(screen,text,color,rect,font):
    y=0
    
    list = text.split("\n")
    for l in list:
        # offsets are because rects are extra thick
        x = rect.x+2
        ry = rect.y+2
        w = rect.w -10
        h = rect.h -2
        ry = ry + y
        goodrect = pygame.Rect(x,ry,w,h)
        newy = drawText(screen,l,color,goodrect,font,aa=True)
        y = y + newy
        #print(newy)

cs = UpdateCalSquares()
url = "http://p105-caldav.icloud.com/published/2/MTY2MDAzNDAwMTY2MDAzNJDm2Vyov8BdGsbb4WCjnS9Uud-xUyiILufO2b5rkw8CIakiZTQLktbw6KtBUycPdeUS_sZ9Wd1OzyLfk7OCHrg"
urllib.request.urlretrieve(url,"calc.ics")
bglist = os.listdir("bgs")
pape = "bgs/" + random.choice(bglist)
updated = False
while True:
    event_extras = []
    dttoday = dt.today()
    bglist = os.listdir("bgs")
    timemin = dttoday.strftime("%-M")
    stringtime = dttoday.strftime("%m/%d/%Y %-I:%M %p")


    if int(timemin) % 2 == 0 and updated == False:
        pape = "bgs/" + random.choice(bglist)
        updated = True

    if int(timemin) % 2 != 0:
        updated = False
    print(pape)
    image = pygame.image.load(pape)
    screen.blit(image,(0,0))
    #screen.fill((0,255,0))
    #screen.blit(text,textRect)
    DrawOutlineText(screen,0,0,black,white,stringtime,False,1,font)
    #DrawOutlineText(screen,

    for rect in rects:
#        temprect1 = CreateRect(rect[0]+1,rect[1]+1,rect[2]+1,rect[3]+1)
#        temprect2 = CreateRect(rect[0]+1,rect[1]-1,rect[2]+1,rect[3]-1)
#        temprect3 = CreateRect(rect[0]-1,rect[1]+1,rect[2]-1,rect[3]+1)
#        temprect4 = CreateRect(rect[0]-1,rect[1]-1,rect[2]-1,rect[3]-1)
#        pg.draw.rect(screen,(255,255,255),temprect1,width=1)
#        pg.draw.rect(screen,(255,255,255),temprect2,width=1)
#        pg.draw.rect(screen,(255,255,255),temprect3,width=1)
#        pg.draw.rect(screen,(255,255,255),temprect4,width=1)
        pg.draw.rect(screen,black,rect,width=1)
        
        #pg.
    
    if timemin == "0":
        print("updateing")
        cs = UpdateCalSquares()
        url = "http://p105-caldav.icloud.com/published/2/MTY2MDAzNDAwMTY2MDAzNJDm2Vyov8BdGsbb4WCjnS9Uud-xUyiILufO2b5rkw8CIakiZTQLktbw6KtBUycPdeUS_sZ9Wd1OzyLfk7OCHrg"
        urllib.request.urlretrieve(url,"calc.ics")
        #print(cs)
    for square in cs:
        #temprect1 = CreateRect(square.rect[0]+1,square.rect[1]+1,square.rect[2]+1,square.rect[3]+1)
        #temprect2 = CreateRect(square.rect[0]+1,square.rect[1]-1,square.rect[2]+1,square.rect[3]-1)
        #temprect3 = CreateRect(square.rect[0]-1,square.rect[1]+1,square.rect[2]-1,square.rect[3]+1)
        #temprect4 = CreateRect(square.rect[0]-1,square.rect[1]-1,square.rect[2]-1,square.rect[3]-1)

        temprect1 = pg.Rect((square.rect[0]+1,square.rect[1]+1),(square.rect[2],square.rect[3]))
        temprect2 = pg.Rect((square.rect[0]+1,square.rect[1]-1),(square.rect[2],square.rect[3]))
        temprect3 = pg.Rect((square.rect[0]-1,square.rect[1]+1),(square.rect[2],square.rect[3]))
        temprect4 = pg.Rect((square.rect[0]-1,square.rect[1]-1),(square.rect[2],square.rect[3]))

        #print(square.rect)
        #print(temprect1)
        pg.draw.rect(screen,(255,255,255),temprect1,width=1)
        pg.draw.rect(screen,(255,255,255),temprect2,width=1)
        pg.draw.rect(screen,(255,255,255),temprect3,width=1)
        pg.draw.rect(screen,(255,255,255),temprect4,width=1)
        
        pg.draw.rect(screen,black,square.rect,width=1)
        
        #drawText(screen,GetCalTextForDay(square.date),black,square.rect,calfont,True)
        #drawText(screen,"aaa",black,square.rect,font)
        DrawCalData(screen,GetCalTextForDay(square.date),black,square.rect,calfont)
        #DrawCalData(screen,GetCalTextForDay(square.date),black,square.rect,calfont2)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            quit()
    pg.display.update()
    time.sleep(1)
    #text=font.render(stringtime,True,black)

    #DrawOutlineText(screen,0,0,black,white,stringtime,False,1,font)
