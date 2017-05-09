# -*- coding:utf-8 -*-
'''
Gin_huo@hotmail.com  MP3 Player
'''
import wx
import wx.media
import os,sys
import wx.grid as gridlib
import wx.lib.mixins.listctrl  as  listmix
import os,sys,inspect,re
import sqlite3
import mutagen
import mutagen.mp3
import mutagen.id3
from mutagen import File
from mutagen.mp3 import MP3 
from mutagen.easyid3 import EasyID3
import math

default_encoding = 'gbk'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

database_name = 'music.db3'
work_path = u'D:\media\demo'


'''
所有的mp3音乐 Gin_huo@hotmail.com  MP3 Player
'''
class MyMP3:
    path            =''
    title           =''
    album           =''
    date            =''
    performer       =''
    encodedby       =''
    tracknumber     =''
    version         =''
    website         =''
    genre           =''
    language        =''
    artist          =''
    organization    =''
    def __init__(self,file_path):
        file            =   MP3(file_path, ID3=EasyID3)
        try:
            self.title           =   str(file['title'])[3:-2]
        except Exception, e:
            print e
        try:
            self.album           =   str(file['album'])[3:-2]
        except Exception, e:
            print e
        try:
            self.date            =   str(file['date'])[3:-2]
        except Exception, e:
            print e
        try:
            self.performer       =   str(file['performer'])[3:-2]
        except Exception, e:
            print e
        try:
            self.encodedby       =   str(file['encodedby'])[3:-2]
        except Exception, e:
            print e
        try:
            self.tracknumber     =   str(file['tracknumber'])[3:-2]
        except Exception, e:
            print e
        try:
            self.version         =   str(file['version'])[3:-2]
        except Exception, e:
            print e
        try:
            self.website         =   str(file['website'])[3:-2]
        except Exception, e:
            print e
        try:
            self.genre           =   str(file['genre'])[3:-2]
        except Exception, e:
            print e
        try:
            self.language        =   str(file['language'])[3:-2]
        except Exception, e:
            print e
        try:
            self.artist          =   str(file['artist'])[3:-2]
        except Exception, e:
            print e
        try:
            self.organization    =   str(file['organization'])[3:-2]
        except Exception, e:
            print e


    def mp3_image(path):
        file = File(path)
        artwork = file.tags['APIC:'].data # access APIC frame and grab the image
        with open('image.jpg', 'wb') as img:
            img.write(artwork) # write artwork to new image

'''
查找所有音乐 Gin_huo@hotmail.com  MP3 Player
'''
def search_music(con,path):  
    queue = []
    queue.append(path);
    cur = con.cursor()
    while len(queue) > 0:  
        tmp = queue.pop(0)  
        if(os.path.isdir(tmp)):  
            for item in os.listdir(tmp):  
                queue.append(os.path.join(tmp, item))  
        elif(os.path.isfile(tmp)):   
            name= os.path.basename(tmp)
            dirname= os.path.dirname(tmp)
            full_path = os.path.join(dirname,name)
            abspath=os.path.abspath(tmp);
            # if full_path.endswith(".wav"):
            if name[-3:] == 'mp3':
                cur.execute('INSERT INTO top_list (o_id, music_dir, music_name,music_abspath) VALUES(NULL, "' + dirname+'", "' + name+'","'+abspath+'")')
                con.commit()
                try:
                    imusic = MyMP3(abspath)
                    cur.execute('INSERT INTO mp3_list(o_id, music_name,music_abspath,title,album,date,performer,encodedby,tracknumber,version,website,genre,language,artist,organization) VALUES(NULL,"'+name+'","'+abspath+'","'+imusic.title+'","'+ imusic.album+'","'+ imusic.date+'","'+ imusic.performer+'","'+ imusic.encodedby+'","'+ imusic.tracknumber+'","'+ imusic.version+'","'+ imusic.website+'","'+ imusic.genre+'","'+ imusic.language+'","'+ imusic.artist+'","'+ imusic.organization+'")')
                except Exception, e:
                    print e 
                    print name
            if name[-3:] == 'wav':
                cur.execute('INSERT INTO top_list (o_id, music_dir, music_name,music_abspath) VALUES(NULL, "' + dirname+'", "' + name+'","'+abspath+'")')
                con.commit()
            if name[-3:] == 'mid':
                cur.execute('INSERT INTO top_list (o_id, music_dir, music_name,music_abspath) VALUES(NULL, "' + dirname+'", "' + name+'","'+abspath+'")')
                con.commit()
    cur.execute('SELECT * FROM top_list')
    con.commit()

'''
创建数据库 Gin_huo@hotmail.com  MP3 Player
'''
#
def creat_database():
    exist_database = os.path.isfile(database_name)
    print exist_database
    if(exist_database==True):
        os.remove(database_name)
        print "database was removed"
    con = sqlite3.connect(database_name)
    print "database was created"
    cur = con.cursor()
    cur.execute('CREATE TABLE top_list (o_id INTEGER PRIMARY KEY, music_dir VARCHAR(100), music_name VARCHAR(100),music_abspath VARCHAR(200))')
    cur.execute('CREATE TABLE mp3_list (o_id INTEGER PRIMARY KEY, music_name VARCHAR(100),music_abspath VARCHAR(200),title VARCHAR(100),album VARCHAR(100),date VARCHAR(100),performer VARCHAR(100),encodedby VARCHAR(100),tracknumber VARCHAR(100),version VARCHAR(100),website VARCHAR(100),genre VARCHAR(100),language VARCHAR(100),artist VARCHAR(100),organization VARCHAR(100))')
    con.commit()
    print "table was created"
    search_music(con,work_path)
    con.close()
'''
创建窗体 Gin_huo@hotmail.com  MP3 Player
'''
class HuoForm(wx.Frame):
    def __init__(self): 
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="play audio Gin_huo@hotmail.com", size = (320, 420))
        panel = HuoPanel(self, -1)
'''
创建listctrl Gin_huo@hotmail.com  MP3 Player
'''
class Music_List(wx.ListCtrl,listmix.ListCtrlAutoWidthMixin):
    index = 0
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
            style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES, pos=(10,170), size=(280,200))
        self.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.InsertColumn(0, "id",width=30)
        self.InsertColumn(1, "name",width=100)
        self.InsertColumn(2, "path",width=100)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        # index1 = self.InsertStringItem(sys.maxint, "Same String")
        # self.SetStringItem(index1, 1, "1")

    # def OnGetItemText(self, item, col):
    #     prints = "%d,%d" % (item, col)
    #     return prints
    
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        print 'OnItemSelected: "%s"\n' %self.currentItem
        # self.SetItemState(self.currentItem,self.SetBackgroundColour("yellow"),
        #                   wx.LIST_STATE_SELECTED)
'''
创建panel Gin_huo@hotmail.com  MP3 Player
'''
class HuoPanel(wx.Panel):
    def __init__(self, parent, id):
        #self.log = log
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)

        # Create some controls
        try:
            self.mc = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise
        self.currentVolume = 50
        self.index = 0
        creat_database()
        loadButton = wx.Button(self, -1, "Load File")
        # self.Bind(wx.EVT_BUTTON, self.onLoadFile, loadButton)
        self.Bind(wx.EVT_BUTTON, self.onLoadFile, loadButton)
        
        playButton = wx.Button(self, -1, "Play")
        self.playButton = playButton
        self.Bind(wx.EVT_BUTTON, self.onPlay, playButton)
        
        pauseButton = wx.Button(self, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.onPause, pauseButton)
        
        stopButton = wx.Button(self, -1, "Stop")
        self.Bind(wx.EVT_BUTTON, self.onStop, stopButton)
        ###player
        slider = wx.Slider(self, -1, 0, 0, 0, size=wx.Size(300, -1))   
        self.slider = slider
        self.Bind(wx.EVT_SLIDER, self.onSeek, slider)

        ###player volumeslider
        volumeslider = wx.Slider(self, -1, 0, 0, 0, pos=(200,75),size=wx.Size(40, 75),style = wx.SL_VERTICAL)
        volumeslider.SetRange(0, 100) 
        self.volumeslider = volumeslider
        self.volumeslider.SetValue(self.currentVolume)
        # self.Bind(wx.EVT_SLIDER, self.onVolume, self.volumeslider)
        self.volumeslider.Bind(wx.EVT_SLIDER, self.onSetVolume)

        testButton = wx.Button(self, -1, "test",pos = (200, 50))
        # self.Bind(wx.EVT_BUTTON, self.onLoadFile, loadButton)
        self.Bind(wx.EVT_BUTTON, self.add_line, testButton)

        checkbox = wx.CheckBox(self, -1, "Repeat", pos = (20, 150))
        self.checkbox = checkbox

        # listctrl = Music_List(self)
        # self.listctrl = listctrl

        listctrl = wx.ListCtrl(self, -1, pos=(10,170), size=(280,200),style=wx.LC_REPORT |wx.BORDER_SUNKEN )
        self.listctrl = listctrl
        self.listctrl.InsertColumn(0, "id",width=30)
        self.listctrl.InsertColumn(1, "name",width=100)
        self.listctrl.InsertColumn(2, "path",width=100)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected,listctrl)


        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("select o_id,music_name,music_abspath from top_list")
        for row in cur:
            self.listctrl.InsertStringItem(self.index, str(row[0]))
            self.listctrl.SetStringItem(self.index, 1, str(row[1]))
            self.listctrl.SetStringItem(self.index, 2, str(row[2]))
            self.index += 1
        con.close()


        self.st_file = wx.StaticText(self, -1, ".mid .mp3 .wav .au .avi .mpg", size=(200,-1))
        self.st_size = wx.StaticText(self, -1, size=(100,-1))
        self.st_len  = wx.StaticText(self, -1, size=(100,-1))
        self.st_pos  = wx.StaticText(self, -1, size=(100,-1))
        
        # setup the button/label layout using a sizer
        sizer = wx.GridBagSizer(5,5)
        sizer.Add(loadButton, (1,1))
        sizer.Add(playButton, (2,1))
        sizer.Add(pauseButton, (3,1))
        sizer.Add(stopButton, (4,1))
        sizer.Add(self.st_file, (1, 2))
        sizer.Add(self.st_size, (2, 2))
        sizer.Add(self.st_len,  (3, 2))
        sizer.Add(self.st_pos,  (4, 2))
        sizer.Add(self.mc, (5,1), span=(5,1))  # for .avi .mpg video files 
        self.SetSizer(sizer)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)
        
    def onLoadFile(self, evt):
        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.doLoadFile(path)
        dlg.Destroy()
        
    def doLoadFile(self, path):
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path, "ERROR", wx.ICON_ERROR | wx.OK)
        else:
            folder, filename = os.path.split(path)
            self.st_file.SetLabel('%s' % filename)
            self.mc.SetBestFittingSize()
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
            self.mc.Play()
        
    def onPlay(self, evt):
        self.mc.Play()
        self.playButton.SetLabel("Play >>")

    def onPause(self, evt):
        self.mc.Pause()
    
    def onStop(self, evt):
        self.mc.Stop()
    
    def onSeek(self, evt):
        offset = self.slider.GetValue()
        self.mc.Seek(offset)

    def add_line(self, event):
        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("select o_id,music_name,music_abspath from top_list")
        for row in cur:
            self.listctrl.InsertStringItem(self.index, str(row[0]))
            self.listctrl.SetStringItem(self.index, 1, str(row[1]))
            self.listctrl.SetStringItem(self.index, 2, str(row[2]))
            self.index += 1
        con.close()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        # print 'OnItemSelected: "%s"\n' %self.currentItem
        COL = 2
        index = event.GetIndex()
        data = self.listctrl.GetItem(index, COL)
        self.doLoadFile(data.GetText())
        # print data.GetText()

    def onVolume(self,evt):
        self.mc.setvolume()
        
    def onSetVolume(self, event):
        """
        Sets the volume of the music player
        self.volumeslider.SetValue(self.currentVolume)
        """
        self.currentVolume = self.volumeslider.GetValue()
        print "setting volume to: %s" % int(self.currentVolume)
        print self.mc.GetVolume()

        self.mc.SetVolume(round(1.0/self.currentVolume,2))

# -*- coding:utf-8 -*-
'''
Gin_huo@hotmail.com  MP3 Player
'''
import wx
import wx.media
import os,sys
import wx.grid as gridlib
import wx.lib.mixins.listctrl  as  listmix
import os,sys,inspect,re
import sqlite3
import mutagen
import mutagen.mp3
import mutagen.id3
from mutagen import File
from mutagen.mp3 import MP3 
from mutagen.easyid3 import EasyID3
import math

default_encoding = 'gbk'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

database_name = 'music.db3'
work_path = u'D:\media\demo'


'''
所有的mp3音乐 Gin_huo@hotmail.com  MP3 Player
'''
class MyMP3:
    path            =''
    title           =''
    album           =''
    date            =''
    performer       =''
    encodedby       =''
    tracknumber     =''
    version         =''
    website         =''
    genre           =''
    language        =''
    artist          =''
    organization    =''
    def __init__(self,file_path):
        file            =   MP3(file_path, ID3=EasyID3)
        try:
            self.title           =   str(file['title'])[3:-2]
        except Exception, e:
            print e
        try:
            self.album           =   str(file['album'])[3:-2]
        except Exception, e:
            print e
        try:
            self.date            =   str(file['date'])[3:-2]
        except Exception, e:
            print e
        try:
            self.performer       =   str(file['performer'])[3:-2]
        except Exception, e:
            print e
        try:
            self.encodedby       =   str(file['encodedby'])[3:-2]
        except Exception, e:
            print e
        try:
            self.tracknumber     =   str(file['tracknumber'])[3:-2]
        except Exception, e:
            print e
        try:
            self.version         =   str(file['version'])[3:-2]
        except Exception, e:
            print e
        try:
            self.website         =   str(file['website'])[3:-2]
        except Exception, e:
            print e
        try:
            self.genre           =   str(file['genre'])[3:-2]
        except Exception, e:
            print e
        try:
            self.language        =   str(file['language'])[3:-2]
        except Exception, e:
            print e
        try:
            self.artist          =   str(file['artist'])[3:-2]
        except Exception, e:
            print e
        try:
            self.organization    =   str(file['organization'])[3:-2]
        except Exception, e:
            print e


    def mp3_image(path):
        file = File(path)
        artwork = file.tags['APIC:'].data # access APIC frame and grab the image
        with open('image.jpg', 'wb') as img:
            img.write(artwork) # write artwork to new image

'''
查找所有音乐 Gin_huo@hotmail.com  MP3 Player
'''
def search_music(con,path):  
    queue = []
    queue.append(path);
    cur = con.cursor()
    while len(queue) > 0:  
        tmp = queue.pop(0)  
        if(os.path.isdir(tmp)):  
            for item in os.listdir(tmp):  
                queue.append(os.path.join(tmp, item))  
        elif(os.path.isfile(tmp)):   
            name= os.path.basename(tmp)
            dirname= os.path.dirname(tmp)
            full_path = os.path.join(dirname,name)
            abspath=os.path.abspath(tmp);
            # if full_path.endswith(".wav"):
            if name[-3:] == 'mp3':
                cur.execute('INSERT INTO top_list (o_id, music_dir, music_name,music_abspath) VALUES(NULL, "' + dirname+'", "' + name+'","'+abspath+'")')
                con.commit()
                try:
                    imusic = MyMP3(abspath)
                    cur.execute('INSERT INTO mp3_list(o_id, music_name,music_abspath,title,album,date,performer,encodedby,tracknumber,version,website,genre,language,artist,organization) VALUES(NULL,"'+name+'","'+abspath+'","'+imusic.title+'","'+ imusic.album+'","'+ imusic.date+'","'+ imusic.performer+'","'+ imusic.encodedby+'","'+ imusic.tracknumber+'","'+ imusic.version+'","'+ imusic.website+'","'+ imusic.genre+'","'+ imusic.language+'","'+ imusic.artist+'","'+ imusic.organization+'")')
                except Exception, e:
                    print e 
                    print name
            if name[-3:] == 'wav':
                cur.execute('INSERT INTO top_list (o_id, music_dir, music_name,music_abspath) VALUES(NULL, "' + dirname+'", "' + name+'","'+abspath+'")')
                con.commit()
            if name[-3:] == 'mid':
                cur.execute('INSERT INTO top_list (o_id, music_dir, music_name,music_abspath) VALUES(NULL, "' + dirname+'", "' + name+'","'+abspath+'")')
                con.commit()
    cur.execute('SELECT * FROM top_list')
    con.commit()

'''
创建数据库 Gin_huo@hotmail.com  MP3 Player
'''
#
def creat_database():
    exist_database = os.path.isfile(database_name)
    print exist_database
    if(exist_database==True):
        os.remove(database_name)
        print "database was removed"
    con = sqlite3.connect(database_name)
    print "database was created"
    cur = con.cursor()
    cur.execute('CREATE TABLE top_list (o_id INTEGER PRIMARY KEY, music_dir VARCHAR(100), music_name VARCHAR(100),music_abspath VARCHAR(200))')
    cur.execute('CREATE TABLE mp3_list (o_id INTEGER PRIMARY KEY, music_name VARCHAR(100),music_abspath VARCHAR(200),title VARCHAR(100),album VARCHAR(100),date VARCHAR(100),performer VARCHAR(100),encodedby VARCHAR(100),tracknumber VARCHAR(100),version VARCHAR(100),website VARCHAR(100),genre VARCHAR(100),language VARCHAR(100),artist VARCHAR(100),organization VARCHAR(100))')
    con.commit()
    print "table was created"
    search_music(con,work_path)
    con.close()
'''
创建窗体 Gin_huo@hotmail.com  MP3 Player
'''
class HuoForm(wx.Frame):
    def __init__(self): 
        """Constructor"""
        wx.Frame.__init__(self, parent=None, title="play audio Gin_huo@hotmail.com", size = (320, 420))
        panel = HuoPanel(self, -1)
'''
创建listctrl Gin_huo@hotmail.com  MP3 Player
'''
class Music_List(wx.ListCtrl,listmix.ListCtrlAutoWidthMixin):
    index = 0
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1,
            style=wx.LC_REPORT|wx.LC_VIRTUAL|wx.LC_HRULES|wx.LC_VRULES, pos=(10,170), size=(280,200))
        self.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.InsertColumn(0, "id",width=30)
        self.InsertColumn(1, "name",width=100)
        self.InsertColumn(2, "path",width=100)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected)
        # index1 = self.InsertStringItem(sys.maxint, "Same String")
        # self.SetStringItem(index1, 1, "1")

    # def OnGetItemText(self, item, col):
    #     prints = "%d,%d" % (item, col)
    #     return prints
    
    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        print 'OnItemSelected: "%s"\n' %self.currentItem
        # self.SetItemState(self.currentItem,self.SetBackgroundColour("yellow"),
        #                   wx.LIST_STATE_SELECTED)
'''
创建panel Gin_huo@hotmail.com  MP3 Player
'''
class HuoPanel(wx.Panel):
    def __init__(self, parent, id):
        #self.log = log
        wx.Panel.__init__(self, parent, -1, style=wx.TAB_TRAVERSAL|wx.CLIP_CHILDREN)

        # Create some controls
        try:
            self.mc = wx.media.MediaCtrl(self, style=wx.SIMPLE_BORDER)
        except NotImplementedError:
            self.Destroy()
            raise
        self.currentVolume = 50
        self.index = 0
        creat_database()
        loadButton = wx.Button(self, -1, "Load File")
        # self.Bind(wx.EVT_BUTTON, self.onLoadFile, loadButton)
        self.Bind(wx.EVT_BUTTON, self.onLoadFile, loadButton)
        
        playButton = wx.Button(self, -1, "Play")
        self.playButton = playButton
        self.Bind(wx.EVT_BUTTON, self.onPlay, playButton)
        
        pauseButton = wx.Button(self, -1, "Pause")
        self.Bind(wx.EVT_BUTTON, self.onPause, pauseButton)
        
        stopButton = wx.Button(self, -1, "Stop")
        self.Bind(wx.EVT_BUTTON, self.onStop, stopButton)
        ###player
        slider = wx.Slider(self, -1, 0, 0, 0, size=wx.Size(300, -1))   
        self.slider = slider
        self.Bind(wx.EVT_SLIDER, self.onSeek, slider)

        ###player volumeslider
        volumeslider = wx.Slider(self, -1, 0, 0, 0, pos=(200,75),size=wx.Size(40, 75),style = wx.SL_VERTICAL)
        volumeslider.SetRange(0, 100) 
        self.volumeslider = volumeslider
        self.volumeslider.SetValue(self.currentVolume)
        # self.Bind(wx.EVT_SLIDER, self.onVolume, self.volumeslider)
        self.volumeslider.Bind(wx.EVT_SLIDER, self.onSetVolume)

        testButton = wx.Button(self, -1, "test",pos = (200, 50))
        # self.Bind(wx.EVT_BUTTON, self.onLoadFile, loadButton)
        self.Bind(wx.EVT_BUTTON, self.add_line, testButton)

        checkbox = wx.CheckBox(self, -1, "Repeat", pos = (20, 150))
        self.checkbox = checkbox

        # listctrl = Music_List(self)
        # self.listctrl = listctrl

        listctrl = wx.ListCtrl(self, -1, pos=(10,170), size=(280,200),style=wx.LC_REPORT |wx.BORDER_SUNKEN )
        self.listctrl = listctrl
        self.listctrl.InsertColumn(0, "id",width=30)
        self.listctrl.InsertColumn(1, "name",width=100)
        self.listctrl.InsertColumn(2, "path",width=100)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.OnItemSelected,listctrl)


        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("select o_id,music_name,music_abspath from top_list")
        for row in cur:
            self.listctrl.InsertStringItem(self.index, str(row[0]))
            self.listctrl.SetStringItem(self.index, 1, str(row[1]))
            self.listctrl.SetStringItem(self.index, 2, str(row[2]))
            self.index += 1
        con.close()


        self.st_file = wx.StaticText(self, -1, ".mid .mp3 .wav .au .avi .mpg", size=(200,-1))
        self.st_size = wx.StaticText(self, -1, size=(100,-1))
        self.st_len  = wx.StaticText(self, -1, size=(100,-1))
        self.st_pos  = wx.StaticText(self, -1, size=(100,-1))
        
        # setup the button/label layout using a sizer
        sizer = wx.GridBagSizer(5,5)
        sizer.Add(loadButton, (1,1))
        sizer.Add(playButton, (2,1))
        sizer.Add(pauseButton, (3,1))
        sizer.Add(stopButton, (4,1))
        sizer.Add(self.st_file, (1, 2))
        sizer.Add(self.st_size, (2, 2))
        sizer.Add(self.st_len,  (3, 2))
        sizer.Add(self.st_pos,  (4, 2))
        sizer.Add(self.mc, (5,1), span=(5,1))  # for .avi .mpg video files 
        self.SetSizer(sizer)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer)
        self.timer.Start(100)
        
    def onLoadFile(self, evt):
        dlg = wx.FileDialog(self, message="Choose a media file",
                            defaultDir=os.getcwd(), defaultFile="",
                            style=wx.OPEN | wx.CHANGE_DIR )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.doLoadFile(path)
        dlg.Destroy()
        
    def doLoadFile(self, path):
        if not self.mc.Load(path):
            wx.MessageBox("Unable to load %s: Unsupported format?" % path, "ERROR", wx.ICON_ERROR | wx.OK)
        else:
            folder, filename = os.path.split(path)
            self.st_file.SetLabel('%s' % filename)
            self.mc.SetBestFittingSize()
            self.GetSizer().Layout()
            self.slider.SetRange(0, self.mc.Length())
            self.mc.Play()
        
    def onPlay(self, evt):
        self.mc.Play()
        self.playButton.SetLabel("Play >>")

    def onPause(self, evt):
        self.mc.Pause()
    
    def onStop(self, evt):
        self.mc.Stop()
    
    def onSeek(self, evt):
        offset = self.slider.GetValue()
        self.mc.Seek(offset)

    def add_line(self, event):
        con = sqlite3.connect(database_name)
        cur = con.cursor()
        cur.execute("select o_id,music_name,music_abspath from top_list")
        for row in cur:
            self.listctrl.InsertStringItem(self.index, str(row[0]))
            self.listctrl.SetStringItem(self.index, 1, str(row[1]))
            self.listctrl.SetStringItem(self.index, 2, str(row[2]))
            self.index += 1
        con.close()

    def OnItemSelected(self, event):
        self.currentItem = event.m_itemIndex
        # print 'OnItemSelected: "%s"\n' %self.currentItem
        COL = 2
        index = event.GetIndex()
        data = self.listctrl.GetItem(index, COL)
        self.doLoadFile(data.GetText())
        # print data.GetText()

    def onVolume(self,evt):
        self.mc.setvolume()
        
    def onSetVolume(self, event):
        """
        Sets the volume of the music player
        self.volumeslider.SetValue(self.currentVolume)
        """
        self.currentVolume = self.volumeslider.GetValue()
        print "setting volume to: %s" % int(self.currentVolume)
        print self.mc.GetVolume()

        self.mc.SetVolume(round(1.0/self.currentVolume,2))

    def onTimer(self, evt):
        offset = self.mc.Tell()
        self.slider.SetValue(offset)
        self.st_size.SetLabel('size: %s ms' % self.mc.Length())
        self.st_len.SetLabel('( %d seconds )' % (self.mc.Length()/1000))
        self.st_pos.SetLabel('position: %d ms' % offset)
        self.slider.SetRange(0,self.mc.Length())
        if ( offset == 0 ):
            if ( self.checkbox.IsChecked()):
                if(self.playButton.GetLabel()=="Play >>" ):
                    self.mc.Play()
            else:
                self.playButton.SetLabel("Play")


class App(wx.App):
    """Application class."""

    def OnInit(self):
        # image = wx.Image('image.jpg', wx.BITMAP_TYPE_JPEG)
        self.frame = HuoForm()
        self.frame.Show()
        # self.SetTopWindow(self.frame)
        return True

def main():
    app = App()
    app.MainLoop()

if __name__ == '__main__':
    main()


# if __name__ == '__main__':
#     app = wx.PySimpleApp()
#     frame = HuoForm()
#     frame.Show()
#     app.MainLoop()


    def onTimer(self, evt):
        offset = self.mc.Tell()
        self.slider.SetValue(offset)
        self.st_size.SetLabel('size: %s ms' % self.mc.Length())
        self.st_len.SetLabel('( %d seconds )' % (self.mc.Length()/1000))
        self.st_pos.SetLabel('position: %d ms' % offset)
        self.slider.SetRange(0,self.mc.Length())
        if ( offset == 0 ):
            if ( self.checkbox.IsChecked()):
                if(self.playButton.GetLabel()=="Play >>" ):
                    self.mc.Play()
            else:
                self.playButton.SetLabel("Play")


class App(wx.App):
    """Application class."""

    def OnInit(self):
        # image = wx.Image('image.jpg', wx.BITMAP_TYPE_JPEG)
        self.frame = HuoForm()
        self.frame.Show()
        # self.SetTopWindow(self.frame)
        return True

def main():
    app = App()
    app.MainLoop()

if __name__ == '__main__':
    main()


# if __name__ == '__main__':
#     app = wx.PySimpleApp()
#     frame = HuoForm()
#     frame.Show()
#     app.MainLoop()