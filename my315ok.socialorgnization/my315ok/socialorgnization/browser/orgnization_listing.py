#-*- coding: UTF-8 -*-
from five import grok
import json
import datetime
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from plone.memoize.instance import memoize

from zope.i18n.interfaces import ITranslationDomain
from zope.component import queryUtility
from zope.component import getMultiAdapter

from Products.CMFCore.interfaces import ISiteRoot
from plone.app.layout.navigation.interfaces import INavigationRoot

from my315ok.socialorgnization import _

from my315ok.socialorgnization.content.orgnization import IOrgnization
from my315ok.socialorgnization.content.orgnization import IOrgnization_administrative_licence
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder
from my315ok.socialorgnization.content.yuhuqufolder import IYuhuquOrgnizationFolder
from my315ok.socialorgnization.content.yuetangqufolder import IYuetangquOrgnizationFolder
from my315ok.socialorgnization.content.xiangxiangshifolder import IXiangxiangshiOrgnizationFolder
from my315ok.socialorgnization.content.xiangtanxianfolder import IXiangtanxianOrgnizationFolder
from my315ok.socialorgnization.content.shaoshanshifolder import IShaoshanshiOrgnizationFolder
from my315ok.socialorgnization.content.shibenjifolder import IShibenjiOrgnizationFolder

from plone.memoize.instance import memoize

from Products.CMFCore import permissions
grok.templatedir('templates') 

class Orgnizations_adminView(grok.View):
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_listing_admin')
    grok.name('view')
    grok.require('zope2.View')    
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)

    @memoize    
    def catalog(self):
        context = aq_inner(self.context)
        pc = getToolByName(context, "portal_catalog")
        return pc
    
    @memoize    
    def pm(self):
        context = aq_inner(self.context)
        pm = getToolByName(context, "portal_membership")
        return pm    
            
    @property
    def isEditable(self):
        return self.pm().checkPermission(permissions.ManagePortal,self.context) 

    def tranVoc(self,value):
        """ translate vocabulary value to title"""
        translation_service = getToolByName(self.context,'translation_service')
        title = translation_service.translate(
                                                  value,
                                                  domain='my315ok.socialorgnization',
                                                  mapping={},
                                                  target_language='zh_CN',
                                                  context=self.context,
                                                  default="chengli")
        return title   
        
    def fromid2title(self,id):
        """根据对象id，获得对象title"""
       
        
        brains = self.catalog()({'id':id})
        if len(brains) >0:
            return brains[0].Title
        else:
            return id
        
    @memoize         
    def getOrgnizationFolder(self):

        topicfolder = self.catalog()({'object_provides': IOrgnizationFolder.__identifier__})

        canManage = self.pm().checkPermission(permissions.AddPortalContent,self.context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath        
        
    @memoize     
    def getMemberList(self):
        """获取申请的会议列表"""
        mlist = []        
        
        memberbrains = self.catalog()({'object_provides':IOrgnization.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        i = 0
        for brain in memberbrains:
            i = i+1           
            row = {'number':'','id':'', 'name':'', 'url':'',
                    'sponsor':'', 'orgnization_passDate':'', 'legal_person':'','address':'','register_code':'','editurl':'',
                    'delurl':''}
            row['number'] = i
            row['id'] = brain.id
            row['name'] = brain.Title
            row['url'] = brain.getURL()
            row['sponsor'] = brain.orgnization_supervisor
            row['orgnization_passDate'] = brain.orgnization_passDate.strftime('%Y-%m-%d')
            row['legal_person'] = brain.orgnization_legalPerson            
            row['address'] = brain.orgnization_address
            row['register_code'] = brain.orgnization_registerCode


            row['editurl'] = row['url'] + '/confajaxedit'
            row['delurl'] = row['url'] + '/delete_confirmation'            
            mlist.append(row)
        return mlist

class OrgnizationsView(Orgnizations_adminView):
    grok.context(IOrgnization)
    grok.template('orgnization_view')
    grok.name('view')
    grok.require('zope2.View')
    
    def getAnnualSurveyList(self):
        """获取年检结果列表"""
       
        
        braindata = self.catalog()({'object_provides':IOrgnization_annual_survey.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            annual_survey = self.tranVoc(braindata[i].orgnization_annual_survey)
            year = braindata[i].orgnization_survey_year

            
            out = """<tr>
            <td class="title"><a href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(year)s</td>
            <td class="result">%(annual_survey)s</td></tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            annual_survey= annual_survey,
                                            year=year)           
            outhtml = outhtml + out
        return outhtml             
    
    def getAdministrativeLicenceList(self):
        """获取行政许可列表"""
       
       
        braindata = self.catalog()({'object_provides':IOrgnization_administrative_licence.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            audit_item = self.tranVoc(braindata[i].orgnization_audit_item)
            audit_result = self.tranVoc(braindata[i].orgnization_audit_result)
            audit_date = braindata[i].orgnization_audit_date.strftime('%Y-%m-%d')


            
            out = """<tr>
            <td class="title"><a href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(audit_item)s</td>
            <td class="result">%(audit_result)s</td>
            <td class="result">%(audit_date)s</td>            
            </tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            audit_item= audit_item,
                                            audit_result=audit_result,
                                            audit_date= audit_date)           
            outhtml = outhtml + out
        return outhtml
    
#年检默认视图    
class AnnualsurveyView(Orgnizations_adminView):
    grok.context(IOrgnization_annual_survey)
    grok.template('orgnization_annual_survey')
    grok.name('view')
    grok.require('zope2.View') 
        
#行政许可默认视图    
class AdministrativeLicenceView(Orgnizations_adminView):
    grok.context(IOrgnization_administrative_licence)
    grok.template('orgnization_administrative_licence')
    grok.name('view')
    grok.require('zope2.View')                

class Orgnizations_annualsurveyView(Orgnizations_adminView):
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_annual_survey_roll')
    grok.name('orgnizations_survey')
    grok.require('zope2.View')

    @memoize
    def getMemberList(self):
        """获取年检结果列表"""
       
        
        braindata = self.catalog()({'object_provides':IOrgnization_annual_survey.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'})
        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            annual_survey = self.tranVoc(braindata[i].orgnization_annual_survey)
            year = braindata[i].orgnization_survey_year

            
            out = """<tr>
            <td class="title"><a target="_blank" href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(year)s</td>
            <td class="result">%(annual_survey)s</td></tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            annual_survey= annual_survey,
                                            year=year)           
            outhtml = outhtml + out
        return outhtml        

class AnnualsurveyFullView(Orgnizations_annualsurveyView):
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_annual_survey_fullview')
    grok.name('orgnizations_survey_fullview')
    grok.require('zope2.View')           
 
class Orgnizations_administrativeView(Orgnizations_adminView):
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_administrative_licence_roll')
    grok.name('orgnizations_administrative')
    grok.require('zope2.View')  


    @memoize        
    def getMemberList(self):
        """获取行政许可列表"""
       
        
        braindata = self.catalog()({'object_provides':IOrgnization_administrative_licence.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )

        outhtml = ""
        brainnum = len(braindata)
        
        for i in range(brainnum):
#            import pdb
#            pdb.set_trace()
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            audit_item = self.tranVoc(braindata[i].orgnization_audit_item)
            audit_result = self.tranVoc(braindata[i].orgnization_audit_result)

            
            out = """<tr>
            <td class="title"><a target="_blank" href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(audit_item)s</td>
            <td class="result">%(audit_result)s</td></tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            audit_item= audit_item,
                                            audit_result=audit_result)           
            outhtml = outhtml + out
        return outhtml

class AdministrativeFullView(Orgnizations_administrativeView):
    grok.context(IOrgnizationFolder)
    grok.template('orgnization_administrative_licence_fullview')
    grok.name('orgnizations_administrative_fullview')
    grok.require('zope2.View')              
    
class SiteRootOrgnizationListingView(Orgnizations_adminView):
    grok.context(ISiteRoot)
    grok.template('orgnization_listings')
    grok.name('orgnization_listings')
    
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)
  
    
    def getOrgnizationFolder(self):

        topicfolder = self.catalog()({'object_provides': IOrgnizationFolder.__identifier__})

        canManage = self.pm().checkPermission(permissions.AddPortalContent,context)        
        if (len(topicfolder) > 0) and  canManage:
            tfpath = topicfolder[0].getURL()
        else:
            tfpath = None            
        return tfpath

    def getorgnizations(self,num=10):
 
        """返回前num个conference
        """

        
        maxlen = len(self.catalog()({'object_provides': IOrgnization.__identifier__}))
        if maxlen > num:
            return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on': 'conference_passDate',
                             'sort_limit': num})
        else:
            return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'conference_passDate'})    

class SiteRootAllOrgnizationListingView(SiteRootOrgnizationListingView):
    grok.context(ISiteRoot)
    grok.template('allorgnization_listings')
    grok.name('allorgnization_listings')
     
    def update(self):
        # Hide the editable-object border
        self.request.set('disable_border', True)                
        
    def test(self,t,a,b):
        """ test method"""   
        if t:
            return a
        else:
            return b
    
    def getorgnizations(self):
 
        """返回 all conference
        """


        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'sort_order': 'reverse',
                             'sort_on':'created'})
#翻译 社团，民非，基金会          
    def getType(self,typekey):
        if typekey == 1:
            return "shetuan"
        elif typekey ==2:
            return "minfei"
        else:
            return "jijinhui"
         
#翻译 成立公告，变更，注销公告  
    def getProvince(self,provincekey):
        if provincekey == 1:
            return "chengli"
        elif provincekey ==2:
            return "biangeng"
        else:
            return "zhuxiao"
         
    def search_multicondition(self,query):
#        catalog = getToolByName(self.context, 'portal_catalog')    
        return self.catalog()(query)        


class yuhuquorgnizations(SiteRootAllOrgnizationListingView):
    grok.context(IYuhuquOrgnizationFolder)     
    grok.template('yuhuqu_allorgnization_listings')
    grok.name('view')   
    
    def getorgnizations(self):
 
        """返回 all conference
        """
        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'orgnization_belondtoArea':'yuhuqu',
                             'sort_order': 'reverse',
                             'sort_on':'created'})
        
class yuetangquorgnizations(SiteRootAllOrgnizationListingView):
    grok.context(IYuetangquOrgnizationFolder)     
    grok.template('yuetangqu_allorgnization_listings')
    grok.name('view')   
    
    def getorgnizations(self):
 
        """返回 all conference
        """
        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'orgnization_belondtoArea':'yuetangqu',
                             'sort_order': 'reverse',
                             'sort_on':'created'})
        
class xiangxiangshiorgnizations(SiteRootAllOrgnizationListingView):
    grok.context(IXiangxiangshiOrgnizationFolder)     
    grok.template('xiangxiangshi_allorgnization_listings')
    grok.name('view')   
    
    def getorgnizations(self):
 
        """返回 all conference
        """
        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'orgnization_belondtoArea':'xiangxiangshi',
                             'sort_order': 'reverse',
                             'sort_on':'created'})

class shaoshanshiorgnizations(SiteRootAllOrgnizationListingView):
    grok.context(IShaoshanshiOrgnizationFolder)     
    grok.template('shaoshanshi_allorgnization_listings')
    grok.name('view')   
    
    def getorgnizations(self):
 
        """返回 all conference
        """
        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'orgnization_belondtoArea':'shaoshanshi',
                             'sort_order': 'reverse',
                             'sort_on':'created'})
        
class xiangtanxianorgnizations(SiteRootAllOrgnizationListingView):
    grok.context(IXiangtanxianOrgnizationFolder)     
    grok.template('xiangtanxian_allorgnization_listings')
    grok.name('view')   
    
    def getorgnizations(self):
 
        """返回 all conference
        """
        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'orgnization_belondtoArea':'xiangtanxian',
                             'sort_order': 'reverse',
                             'sort_on':'created'})
           
class shibenjiorgnizations(SiteRootAllOrgnizationListingView):
    grok.context(IShibenjiOrgnizationFolder)     
    grok.template('xiangtanshi_allorgnization_listings')
    grok.name('view')   
    
    def getorgnizations(self):
 
        """返回 all conference
        """
        return self.catalog()({'object_provides': IOrgnization.__identifier__,
                             'orgnization_belondtoArea':'xiangtanshi',
                             'sort_order': 'reverse',
                             'sort_on':'created'})                                 
                      
 # ajax multi-condition search       
class ajaxsearch(grok.View):
    """AJAX action for search.
    """    
    grok.context(ISiteRoot)
    grok.name('oajaxsearch')
    grok.require('zope2.View')

    def Datecondition(self,key):        

        end = datetime.datetime.today()
#最近一周        
        if key == 1:  
            start = end - datetime.timedelta(7) 
#最近一月             
        elif key == 2:
            start = end - datetime.timedelta(30) 
#最近一年            
        elif key == 3:
            start = end - datetime.timedelta(365) 
#最近两年                                                  
        elif key == 4:
            start = end - datetime.timedelta(365*2) 
#最近五年               
        else:
            start = end - datetime.timedelta(365*5) 
#            return    { "query": [start,],"range": "min" }                                                             
        datecondition = { "query": [start, end],"range": "minmax" }
        return datecondition  
          
    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""

#        import pdb
#        pdb.set_trace()
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            address = braindata[i].orgnization_address
            register_code = braindata[i].orgnization_registerCode
            legal_person = braindata[i].orgnization_legalPerson
            objdate = braindata[i].orgnization_passDate.strftime('%Y-%m-%d')
            sponsor = braindata[i].orgnization_supervisor            
#            objid = braindata[i].id.replace('.','_')
            numindex = str(i + 1)
            
            out = """<tr>
                                <td class="span1">%(num)s</td>
                                <td class="span2"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="span1">%(code)s</td>
                                <td class="span2">%(address)s</td>
                                <td class="span2">%(sponsor)s</td>
                                <td class="span2">%(legal_person)s</td>
                                <td class="span2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=objurl,
                                            num=numindex,
                                            title=objtitle,
                                            code= register_code,
                                            address=address,
                                            sponsor=sponsor,
                                            legal_person = legal_person,
                                            pass_date = objdate)
           
            outhtml = outhtml + out 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
                              
class yuhuqusearchlist(ajaxsearch):
    grok.name('yuhuqusearch')
    
    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        origquery['orgnization_belondtoArea'] = 'yuhuqu'
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""


        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            address = braindata[i].orgnization_address
            register_code = braindata[i].orgnization_registerCode
            legal_person = braindata[i].orgnization_legalPerson
            objdate = braindata[i].orgnization_passDate.strftime('%Y-%m-%d')
            sponsor = braindata[i].orgnization_supervisor            
#            objid = braindata[i].id.replace('.','_')
            numindex = str(i + 1)
            
            out = """<tr>
                                <td class="span1">%(num)s</td>
                                <td class="span2"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="span1">%(code)s</td>
                                <td class="span2">%(address)s</td>
                                <td class="span2">%(sponsor)s</td>
                                <td class="span2">%(legal_person)s</td>
                                <td class="span2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=objurl,
                                            num=numindex,
                                            title=objtitle,
                                            code= register_code,
                                            address=address,
                                            sponsor=sponsor,
                                            legal_person = legal_person,
                                            pass_date = objdate)
           
            outhtml = outhtml + out 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)     

class yuetangqusearchlist(ajaxsearch):
    grok.name('yuetangqusearch')
    
    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        origquery['orgnization_belondtoArea'] = 'yuetangqu'
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""

#        import pdb
#        pdb.set_trace()
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            address = braindata[i].orgnization_address
            register_code = braindata[i].orgnization_registerCode
            legal_person = braindata[i].orgnization_legalPerson
            objdate = braindata[i].orgnization_passDate.strftime('%Y-%m-%d')
            sponsor = braindata[i].orgnization_supervisor            
#            objid = braindata[i].id.replace('.','_')
            numindex = str(i + 1)
            
            out = """<tr>
                                <td class="span1">%(num)s</td>
                                <td class="span2"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="span1">%(code)s</td>
                                <td class="span2">%(address)s</td>
                                <td class="span2">%(sponsor)s</td>
                                <td class="span2">%(legal_person)s</td>
                                <td class="span2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=objurl,
                                            num=numindex,
                                            title=objtitle,
                                            code= register_code,
                                            address=address,
                                            sponsor=sponsor,
                                            legal_person = legal_person,
                                            pass_date = objdate)
           
            outhtml = outhtml + out 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
    
class xiangxiangshisearchlist(ajaxsearch):
    grok.name('xiangxiangshisearch')
    
    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        origquery['orgnization_belondtoArea'] = 'xiangxiangshi'
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""

#        import pdb
#        pdb.set_trace()
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            address = braindata[i].orgnization_address
            register_code = braindata[i].orgnization_registerCode
            legal_person = braindata[i].orgnization_legalPerson
            objdate = braindata[i].orgnization_passDate.strftime('%Y-%m-%d')
            sponsor = braindata[i].orgnization_supervisor            
#            objid = braindata[i].id.replace('.','_')
            numindex = str(i + 1)
            
            out = """<tr>
                                <td class="span1">%(num)s</td>
                                <td class="span2"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="span1">%(code)s</td>
                                <td class="span2">%(address)s</td>
                                <td class="span2">%(sponsor)s</td>
                                <td class="span2">%(legal_person)s</td>
                                <td class="span2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=objurl,
                                            num=numindex,
                                            title=objtitle,
                                            code= register_code,
                                            address=address,
                                            sponsor=sponsor,
                                            legal_person = legal_person,
                                            pass_date = objdate)
           
            outhtml = outhtml + out 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data) 
    
class shaoshanshisearchlist(ajaxsearch):
    grok.name('shaoshanshisearch')
    
    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        origquery['orgnization_belondtoArea'] = 'shaoshanshi'
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""

#        import pdb
#        pdb.set_trace()
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            address = braindata[i].orgnization_address
            register_code = braindata[i].orgnization_registerCode
            legal_person = braindata[i].orgnization_legalPerson
            objdate = braindata[i].orgnization_passDate.strftime('%Y-%m-%d')
            sponsor = braindata[i].orgnization_supervisor            
#            objid = braindata[i].id.replace('.','_')
            numindex = str(i + 1)
            
            out = """<tr>
                                <td class="span1">%(num)s</td>
                                <td class="span2"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="span1">%(code)s</td>
                                <td class="span2">%(address)s</td>
                                <td class="span2">%(sponsor)s</td>
                                <td class="span2">%(legal_person)s</td>
                                <td class="span2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=objurl,
                                            num=numindex,
                                            title=objtitle,
                                            code= register_code,
                                            address=address,
                                            sponsor=sponsor,
                                            legal_person = legal_person,
                                            pass_date = objdate)
           
            outhtml = outhtml + out 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)
    
class xiangtanxiansearchlist(ajaxsearch):
    grok.name('xiangtanxiansearch')
    
    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        origquery['orgnization_belondtoArea'] = 'xiangtanxian'
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""

#        import pdb
#        pdb.set_trace()
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            address = braindata[i].orgnization_address
            register_code = braindata[i].orgnization_registerCode
            legal_person = braindata[i].orgnization_legalPerson
            objdate = braindata[i].orgnization_passDate.strftime('%Y-%m-%d')
            sponsor = braindata[i].orgnization_supervisor            
#            objid = braindata[i].id.replace('.','_')
            numindex = str(i + 1)
            
            out = """<tr>
                                <td class="span1">%(num)s</td>
                                <td class="span2"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="span1">%(code)s</td>
                                <td class="span2">%(address)s</td>
                                <td class="span2">%(sponsor)s</td>
                                <td class="span2">%(legal_person)s</td>
                                <td class="span2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=objurl,
                                            num=numindex,
                                            title=objtitle,
                                            code= register_code,
                                            address=address,
                                            sponsor=sponsor,
                                            legal_person = legal_person,
                                            pass_date = objdate)
           
            outhtml = outhtml + out 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data) 
    
class xiangtanshisearchlist(ajaxsearch):
    grok.name('xiangtanshisearch')
    
    def render(self):    
        self.portal_state = getMultiAdapter((self.context, self.request), name=u"plone_portal_state")
        searchview = getMultiAdapter((self.context, self.request),name=u"allorgnization_listings")        
        
        datadic = self.request.form
        start = int(datadic['start']) # batch search start position
        datekey = int(datadic['datetype'])  # 对应 最近一周，一月，一年……
        size = int(datadic['size'])      # batch search size          
        provincekey = int(datadic['province'])  # 对应 成立公告，变更公告，注销公告
        typekey = int(datadic['type']) # 对应 社会团体，民非，基金会
        sortcolumn = datadic['sortcolumn']
        sortdirection = datadic['sortdirection']
        keyword = (datadic['searchabletext']).strip()     

        origquery = {'object_provides': IOrgnization.__identifier__}
        origquery['sort_on'] = sortcolumn  
        origquery['sort_order'] = sortdirection
#        origquery['b_size'] = size 
#        origquery['b_start'] = start                 
        
        if keyword != "":
            origquery['SearchableText'] = '*'+keyword+'*'        

        if provincekey != 0:
            conference_province = searchview.getProvince(provincekey)
            origquery['orgnization_announcementType'] = conference_province
        if datekey != 0:
            origquery['orgnization_passDate'] = self.Datecondition(datekey)           
        if typekey != 0:
            origquery['orgnization_orgnizationType'] = searchview.getType(typekey)          

        origquery['orgnization_belondtoArea'] = 'xiangtanshi'
        totalquery = origquery.copy()
        origquery['b_size'] = size 
        origquery['b_start'] = start                         
        totalbrains = searchview.search_multicondition(totalquery)
        totalnum = len(totalbrains)         
        braindata = searchview.search_multicondition(origquery)
        brainnum = len(braindata)         
        del origquery 
        del totalquery,totalbrains            
       
        # Capture a status message and translate it
#        translation_service = getToolByName(self.context, 'translation_service')        
#        searchview = getMultiAdapter((self.context, self.request),name=u"allconference_listings")         
        outhtml = ""

#        import pdb
#        pdb.set_trace()
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            address = braindata[i].orgnization_address
            register_code = braindata[i].orgnization_registerCode
            legal_person = braindata[i].orgnization_legalPerson
            objdate = braindata[i].orgnization_passDate.strftime('%Y-%m-%d')
            sponsor = braindata[i].orgnization_supervisor            
#            objid = braindata[i].id.replace('.','_')
            numindex = str(i + 1)
            
            out = """<tr>
                                <td class="span1">%(num)s</td>
                                <td class="span2"><a href="%(objurl)s">%(title)s</a></td>
                                <td class="span1">%(code)s</td>
                                <td class="span2">%(address)s</td>
                                <td class="span2">%(sponsor)s</td>
                                <td class="span2">%(legal_person)s</td>
                                <td class="span2">%(pass_date)s</td>                                
                            </tr> """% dict(objurl=objurl,
                                            num=numindex,
                                            title=objtitle,
                                            code= register_code,
                                            address=address,
                                            sponsor=sponsor,
                                            legal_person = legal_person,
                                            pass_date = objdate)
           
            outhtml = outhtml + out 
           
        data = {'searchresult': outhtml,'start':start,'size':size,'total':totalnum}        
        self.request.response.setHeader('Content-Type', 'application/json')
        return json.dumps(data)                   