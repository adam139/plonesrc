#-*- coding: UTF-8 -*-
from five import grok
from collective.conference.conference import IConference
from collective.conference.session import ISession
from Products.CMFCore.utils import getToolByName
import json
from datetime import datetime, timedelta
#from Products.AdvancedQuery import Le, Ge, Generic, And, Eq
from zope.security import checkPermission
from collective.conference import MessageFactory as _

grok.templatedir('templates')

class AgendaView(grok.View):
    grok.context(IConference)
    grok.name('agenda')
    grok.template('agenda')
    grok.require('zope2.View')

    title = _(u'Agenda')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
        
    def days(self):
        result = []
        delta = self.context.endDate-self.context.startDate
        for i in range(delta.days if delta.seconds == 0 else delta.days + 1):
            result.append({
                'id':i,
                'year':self.context.startDate.year,
                'month':self.context.startDate.month,
                'date':self.context.startDate.day + i
            })
        return result

    def script(self):
        initcode = ''

        for day in self.days():
            for idx, room in enumerate(self.context.rooms):
                initcode += """

                    $('#calendar-%s-%s').fullCalendar($.extend({
                        events: "%s",
                        year: %s,
                        month: %s,
                        date: %s
                    }, opts))
                """ % (
                    day['id'],
                    idx, 
                    '%s/events.json?room=%s' % (
                        self.context.absolute_url(),
                        room
                    ),
                    day['year'],
                    day['month'] - 1,
                    day['date']
                    )

        editable = checkPermission('cmf.ModifyPortalContent', self.context)
        result = """
         $(document).ready(function () {
            var opts = {
               defaultView: 'agendaDay',
               header:'',
               height:1000,
               minTime:8,
               maxTime:18,
               monthNames: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],  
               monthNamesShort: ["一月", "二月", "三月", "四月", "五月", "六月", "七月", "八月", "九月", "十月", "十一月", "十二月"],  
               dayNames: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],  
               dayNamesShort: ["周日", "周一", "周二", "周三", "周四", "周五", "周六"],  
               today: ["今天"],  
               firstDay: 1,  
               buttonText: {  
                  today: '本日',  
                  month: '月',  
                  week: '周',  
                  day: '日',  
                  prev: '上一月',  
                  next: '下一月' }, 
               allDaySlot: false,
               currentTimezone: 'Asia/Beijing',
               editable: %s,
               eventResize: function (event, dayDelta, minuteDelta, revertFunc,
                                        jsEvent, ui, view) {
                        $.post(event.url + '/updateStartEnd',
                              { 'operation': 'resize',
                                'dayDelta': dayDelta,
                                'minuteDelta': minuteDelta});
                        $('.conference-calendar').fullCalendar('refetchEvents');
               },
               eventDrop: function (event, dayDelta, minuteDelta, revertFunc,
                                        jsEvent, ui, view) {
                        $.post(event.url + '/updateStartEnd',
                              { 'operation': 'drag',
                                'dayDelta': dayDelta,
                                'minuteDelta': minuteDelta})
                        $('.conference-calendar').fullCalendar('refetchEvents');
               }
            }

            %s
        });
        """ % ('true' if editable else 'false', initcode)

        return result

class EventJson(grok.View):
    grok.context(IConference)
    grok.name('events.json')
    grok.require('zope2.View')

    def render(self):
        self.request.response.setHeader('Content-Type','text/json')
        start = int(self.request.get('start', 0))
        end = int(self.request.get('end', 0))
        room = self.request.get('room', '')
        result = []
        for event in self.events(room,
                                datetime.fromtimestamp(start),
                                datetime.fromtimestamp(end)):
            result.append({
                'id':event.id,
                'title':event.title,
                'start': event.startDate.isoformat(),
                'end':event.endDate.isoformat(),
                'allDay': False,
                'url': event.absolute_url(),
                'color': '#%s' % getattr(event, 'color', '3366CC')[:6],
                'textColor': '#%s' % getattr(event, 'textColor', 'ffffff')[:6]
            })
        return json.dumps(result)

    def events(self, room, start, end):
        catalog = getToolByName(self.context, 'portal_catalog')

        queries = [
            Eq('portal_type', 'collective.conference.session'),
            Eq('conference_rooms', room),
            Generic('path', {'query': '/'.join(self.context.getPhysicalPath()),
                'depth':2})
        ]
        result = []
# list parameter write this        
        for brain in catalog.evalAdvancedQuery(And(*queries)):
            result.append(brain.getObject())
        return result


class Update(grok.View):
    grok.context(ISession)
    grok.name('updateStartEnd')
    grok.require('zope2.View')
    
    def render(self):
        self.request.response.setHeader('Content-Type','text/json')
        dayDelta = int(self.request.get('dayDelta', 0))
        minuteDelta = int(self.request.get('minuteDelta', 0))
        operation = self.request.get('operation', '')
        secondsDelta = minuteDelta * 60

        delta = timedelta(dayDelta, secondsDelta)

        if operation == 'resize':
            self.context.endDate = self.context.endDate + delta
        elif operation == 'drag':
            self.context.startDate = self.context.startDate + delta
            self.context.endDate = self.context.endDate + delta
        return ''

