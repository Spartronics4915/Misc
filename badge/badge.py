#!/usr/bin/env python
import inkex
import simplestyle, sys
from math import *

class DbBadge(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

        self.OptionParser.add_option("--target",
                        action="store", type="string",
                        dest="target", default="P3",
                        help="select a target material size")
        self.OptionParser.add_option("--width",
                        action="store", type="float",
                        dest="width", default="100",
                        help="select badge width")
        self.OptionParser.add_option("--height",
                        action="store", type="float",
                        dest="height", default="100",
                        help="select badge width")
        self.OptionParser.add_option("--cornerradius",
                        action="store", type="float",
                        dest="cornerradius", default="5",
                        help="select corner radius")
        self.OptionParser.add_option("--debug",
                        action="store", type="inkbool",
                        dest="debug", default=False,
                        help="choose a debug style")
        self.svg = None
        self.coordsysScale = 1.

        #nmfile = "C:/Users/dana/Documents/reading/robot/Roster2015-16.csv"
        #nmfile = "C:/Users/danab/Documents/reading/robot/RosterNewSteamworks.csv"
        nmfile = "C:/Users/danab/Documents/reading/robot/2018Nametags.csv"
        f = open(nmfile)
        # namelist contains csv  entries:
        #   num,First,Last,email,,,experience
        self.namelist = f.read().split('\n')
        f.close()

        self.blackOutline = "fill:none;stroke:#000000;stroke-width:1px;" \
                        "stroke-miterlimit:4;stroke-dasharray:none"

        self.redOutline = "fill:none;stroke:#FF0000;stroke-width:1px;" \
                        "stroke-miterlimit:4;stroke-dasharray:none"

        self.ponokoCutline = "fill:none;stroke:#0000ff;stroke-width:0.01mm;" \
                         "stroke-miterlimit:4;stroke-dasharray:none"

        self.ponokoEtchline = "fill:none;stroke:#ff0000;stroke-width:0.01mm;" \
                         "stroke-miterlimit:4;stroke-dasharray:none"

        self.ponokoText = "fill:none;stroke:#ff0000;stroke-width:0.01mm;" \
                         "stroke-miterlimit:4;stroke-dasharray:none"

        self.redfill =  simplestyle.formatStyle({
                              'stroke': '#000000',
                              'stroke-width': "1px",
                              'fill': '#FF0000' })

        self.blackfill =  simplestyle.formatStyle({
                              'stroke': '#000000',
                              'stroke-width': "1px",
                              'fill': '#000000' })

        # style strings for inkscape can be found by creating a trivial
        # file (with one letter), then inspecting the saved .svg file.

        self.firstnameTxtStyle = "font-style:normal;font-variant:normal;font-weight:900;font-stretch:normal;font-size:12.34722233px;line-height:125%;font-family:Raleway;-inkscape-font-specification:'Raleway, Heavy';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal;text-align:center;writing-mode:lr-tb;text-anchor:middle;stroke-width:0.26458332px"

        self.lastnameTxtStyle = "font-style:normal;font-variant:normal;font-weight:300;font-stretch:normal;font-size:7.76111111px;font-family:Raleway;-inkscape-font-specification:'Raleway, Light';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal;text-align:center;writing-mode:lr;text-anchor:middle;stroke-width:0.26458332px"

        self.logoTxtStyle = "font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:12.34722233px;line-height:8.57835589px;font-family:Spartronics;-inkscape-font-specification:'Spartronics, Bold';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal;text-align:center;writing-mode:lr-tb;text-anchor:middle;stroke-width:0.26458332px;"

        self.logoNumStyle = "font-style:normal;font-variant:normal;font-weight:bold;font-stretch:normal;font-size:12.34722233px;line-height:8.57835589px;font-family:Spartronics;-inkscape-font-specification:'Spartronics, Bold';font-variant-ligatures:normal;font-variant-caps:normal;font-variant-numeric:normal;font-feature-settings:normal;text-align:center;writing-mode:lr-tb;text-anchor:middle;stroke-width:0.26458332px;"

        self.styles = {}

    def effect(self):
        if self.options.debug:
            self.styles["cutline"] = self.blackOutline
            self.styles["etchline"] = self.blackOutline
        else:
            self.styles["cutline"] = self.ponokoCutline
            self.styles["etchline"] = self.ponokoEtchline

        self.svg = self.document.getroot()
        docW = self.unittouu(self.svg.get('width'))
        docH = self.unittouu(self.svg.get('height'))
        self.coordsysScale = self.unittouu("1mm")

        if self.options.cornerradius > 0:
            self.badge = rrect(0, 0, self.options.width, self.options.height,
                               self.options.cornerradius)
        else:
            self.badge = rect(0, 0, self.options.width, self.options.height)

        self.midline = rect(0, 0, self.badge.w * .8, .5)

        borderslop = 5 # orange ponoko safe-zone
        badgeslop = 0
        if self.options.target == "P3":
            self.board = rect(0,0, 791, 384)
        elif self.options.target == "P2":
            self.board = rect(0,0, 384, 384)
        elif self.options.target == "P1":
            self.board = rect(0,0, 181, 181)
        else:
            self.board = rect(0,0, 24*25.4, 96*25.4)
            badgeslop = .125 * 25.4  # 1/8 in

        self.numW = int((self.board.w-2*borderslop) / self.badge.w)
        self.numH = int((self.board.h-2*borderslop) / self.badge.h)

        self.borderslop = borderslop * self.coordsysScale
        self.badgeslop = badgeslop * self.coordsysScale
        self.board.Scale(self.coordsysScale)
        self.badge.Scale(self.coordsysScale)
        self.midline.Scale(self.coordsysScale)
        # center midline horizontally, but place it below midline
        self.midline.MoveTo((self.badge.w-self.midline.w)*.5, 
                            .6*self.badge.h);

        # hole is .5" == 130 mm
        self.hole = rrect(0, 0, .52*25.4, .15*25.4, 1.5)
        self.hole.Scale(self.coordsysScale)
        self.hole.MoveTo((self.badge.w-self.hole.w)/2, self.hole.h)

        # since badges share many edges we really only need to 
        # cut a subset... We always need to cut rounded corners.
        ix = 0; iy = 0; i = 0;
        drawLeft = True
        drawTop = True
        for line in self.namelist:
            # line is First,Last
            sline = line.split(',')
            if len(sline) != 2: 
                continue
            (firstnm,lastnm) = sline[0:2]
            self.drawBadge(i, ix, iy, firstnm, lastnm, drawLeft, drawTop)
            i = i + 1
            ix = ix + 1
            if ix == self.numW:
                ix = 0
                if self.badgeslop == 0:
                    drawLeft = True
                    drawTop = False
                iy = iy + 1
                if iy > self.numH:
                    break
            else:
                if self.badgeslop == 0:
                    drawLeft = False

    def drawBadge(self, i, ix, iy, firstnm, lastnm, drawLeft, drawTop):
        pgrp = self.current_layer
        uid = self.uniqueId("badge%0.3d"%i)
        x = self.borderslop + (self.badge.w + self.badgeslop) * ix
        y = self.borderslop + (self.badge.h + self.badgeslop) * iy

        gattrs = {inkex.addNS('label','inkscape'): uid,
                  'transform': 'translate(%g, %g)' % (x, y)}
        bgrp = inkex.etree.SubElement(pgrp, 'g', gattrs)

        # cuts ------------------------------------------------
        badge = {}
        badge["style"] = self.styles["cutline"]
        outline = "".join([self.fmtvec(t) 
                    for t in self.badge.GetDisplayList(drawLeft, drawTop)])
        hole = "".join([self.fmtvec(t)
                                for t in self.hole.GetDisplayList()])

        badge["d"] = outline + hole
        inkex.etree.SubElement(bgrp, inkex.addNS('path','svg'), badge )

        # engraved divider ------------------------------------
        midline = {}
        midline["style"] = self.styles["etchline"]
        midline["d"] = "".join([self.fmtvec(t) 
                                for t in self.midline.GetDisplayList()])
        inkex.etree.SubElement(bgrp, inkex.addNS('path','svg'), midline)

        # text ------------------------------------------------
        centerX = self.badge.w * .5
        self.addLabel(bgrp, firstnm.decode('utf-8').upper(), 
                      (centerX, self.badge.h*.33),
                      self.firstnameTxtStyle)
        self.addLabel(bgrp, lastnm.decode('utf-8').upper(),
                      (centerX, self.badge.h*.43),
                      self.lastnameTxtStyle)

        self.addLabel(bgrp, "SPARTRONICS", 
                      (centerX, self.badge.h*.75),
                      self.logoTxtStyle)
        self.addLabel(bgrp, "4915",
                      (centerX, self.badge.h*.88), 
                      self.logoNumStyle)

    def fmtvec(self, vec):
        l = len(vec)
        if l == 1:
            return vec[0]
        elif l == 2:
            return "%c %g" % vec
        elif l == 3:
            return "%c %g,%g" % vec
        elif l == 5:
            return "%c %g,%g %g,%g" % vec
        elif l == 7:
            return "%c %g,%g %g,%g %g,%g" % vec

    def addLabel(self, layer, txt, loc, style):
        text = inkex.etree.Element(inkex.addNS('text','svg'))
        text.text = txt
        text.set('x', str(loc[0]))
        text.set('y', str(loc[1]))
        text.set('style', style)
        layer.append(text)

class rect(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

    def MoveTo(self, x, y):
        self.x = x
        self.y = y

    def Scale(self, s):
        self.w *= s
        self.h *= s

    def GetSize(self):
        return (self.w, self.h)

    def GetWidth(self):
        return self.w

    def GetHeight(self):
        return self.h

    def GetPos(self):
        return (self.x, self.y)

    def GetDisplayList(self): 
        #   a --------------- b
        #   |                 |
        #   |                 |
        #   |                 |
        #   |                 |
        #   d --------------- c
        return [("M", self.x, self.y),  # at a
                ("h", self.w),          # to b
                ("v", self.h),          # to c
                ("h", -self.w),         # to d
                ("z")]                  # to a
    
    def Draw(self, inkex, ctx, s, pgrp, origin, kbd, key, switch):
        # a single rect
        bboxAttrs = {"style": s}
        bboxAttrs["d"]= "".join([ctx.fmtvec(t) 
                            for t in self.GetDisplayList()])
        inkex.etree.SubElement(grp, inkex.addNS('path','svg'), bboxAttrs)

# round rect
class rrect(rect):
    def __init__(self, x, y, width, height, radius):
        rect.__init__(self, x, y, width, height)
        self.radius = radius

    def Scale(self, s):
        rect.Scale(self, s)
        self.radius *= s

    def GetDisplayList(self, drawLeft=True, drawTop=True): 
        #   a --e-------------f-- b
        #   |                     |
        #   l                     g
        #   k                     h
        #   |                     |
        #   d --j-------------i-- c
        if self.radius == 0:
            return rect.GetDisplayList(self)
        else:
            r = self.radius
            hlen = self.w - 2*r
            vlen = self.h - 2*r
            if drawLeft and drawTop:
                return [("M", self.x+r, self.y),# at e
                        ("h", hlen),            # to f
                        ("q", r, 0, r, r),      # curveto g, thru b
                        ("v", vlen),            # lineto h
                        ("q", 0, r, -r, r),     # curveto i, thru c
                        ("h", -hlen),           # lineto j
                        ("q", -r, 0, -r, -r),   # curveto k, thru d
                        ("v", -vlen),           # lineto l
                        ("q", 0, -r, r, -r),    # curveto e, thru a
                        ("z")
                        ]
            else:
                ret = [("M", self.x+r+hlen, self.y),  # at f
                        ("q", r, 0, r, r),      # curveto g, thru b
                        ("v", vlen),            # lineto h
                        ("q", 0, r, -r, r),     # curveto i, thru c
                        ("h", -hlen),           # lineto j
                        ("q", -r, 0, -r, -r),   # curveto k, thru d
                        ]
                if drawLeft:
                    ret.extend([
                        ("v", -vlen),           # lineto l
                        ("q", 0, -r, r, -r),    # curveto e, thru a
                        ])
                else:
                    # only the left corners
                    ret.extend([
                        ("M", self.x, self.y+r), # at l
                        ("q", 0, -r, r, -r),    # curveto e, thru a
                        ])

                if drawTop:
                    ret.extend([("h", hlen)]),  # lineto f

                return  ret

# half round rect
class hrrect(rrect): 
    def __init__(self, x, y, width, height, radius, style):
        rrect.__init__(self, x, y, width, height, radius)
        self.style = style  # 'n','s','e','w' signifees the rounded side

    def GetDisplayList(self): 
        if self.radius == 0:
            return rect.GetDisplayList(self)
        else:
            r = self.radius
            hlen1 = self.w - r
            hlen2 = self.w - 2*r
            vlen1 = self.h - r
            vlen2 = self.h - 2*r
            if self.style == 'w':
                #   a --e---------------- b
                #   |                     |
                #   h                     |
                #   g                     |
                #   |                     |
                #   d --f---------------- c
                return [("M", self.x+r, self.y),# at e
                        ("h", hlen1),           # lineto b
                        ("v", self.h),          # lineto c
                        ("h", -hlen1),          # lineto f
                        ("q", -r, 0, -r, -r),   # curveto g, thru d
                        ("v", -vlen2),          # lineto h
                        ("q", -r, 0, -r, r),    # curveto e, thru a
                        ("z")                   # end (vestigial)
                        ]
            elif self.style == 'e':
                #   a ----------------f-- b
                #   |                     |
                #   |                     g
                #   |                     h
                #   |                     |
                #   d ----------------i-- c
                return [("M", self.x+hlen1, self.y+self.h),  # at i
                        ("h", -hlen1),          # lineto d
                        ("v", -self.h),         # lineto a
                        ("h", hlen1),           # lineto f
                        ("q", r, 0, r, r),      # curveto g, thru b
                        ("v", vlen2),           # lineto h
                        ("q", 0, r, -r, r),     # curveto i, thru c
                        ("z")                   # close (vestigial)
                        ]
            elif self.style == 'n':
                #   a --e------------f--- b
                #   |                     |
                #   h                     g
                #   |                     |
                #   |                     |
                #   d ------------------- c
                return [("M", self.x+self.w, self.y+r),  # at g
                        ("v", vlen1),           # lineto c
                        ("h", -self.w),         # lineto d
                        ("v", -vlen1),          # lineto h
                        ("q", 0, -r, r, -r),    # curveto e, thru a
                        ("h", hlen2),           # lineto f
                        ("q", r, 0, r, r),      # curveto g, thru b
                        ("z")                   # close (vestigial)
                        ]
            elif self.style == 'nc':
                #   a --e------------f--- b
                #   |                     |
                #   h                     g
                #   |   j------------i    |
                #   |   |            |    |
                #   d --k            h--- c
                cutout = .5 * r
                return [("M", self.x+self.w, self.y+r),  # at g
                        ("v", vlen1),           # lineto c
                        ("h", -r),              # lineto h
                        ("v", -cutout),         # lineto i
                        ("h", -hlen2),          # lineto j
                        ("v", cutout),          # lineto k
                        ("h", -r),              # lineto d
                        ("v", -vlen1),          # lineto h
                        ("q", 0, -r, r, -r),    # curveto e, thru a
                        ("h", hlen2),           # lineto f
                        ("q", r, 0, r, r),      # curveto g, thru b
                        ("z")                   # close (vestigial)
                        ]
            elif self.style == 's':
                #   a ------------------- b
                #   |                     |
                #   |                     |
                #   h                     e
                #   |                     |
                #   d --g--------------f- c
                return [("M", self.x, self.y+vlen1),  # at h
                        ("v", -vlen1),          # lineto a
                        ("h", self.w),          # lineto b
                        ("v", vlen1),           # lineto e
                        ("q", 0, r, -r, r),     # curveto f, thru c
                        ("q", -r, 0, -r, -r),   # curveto h, thru d
                        ("z")                   # close (vestigial)
                        ]
            else:
                raise Exception("unknown style (choose from n,s,e,w)");


# --------------------------------------------------------------------------
if __name__ == '__main__':
    e = DbBadge()
    e.affect()
