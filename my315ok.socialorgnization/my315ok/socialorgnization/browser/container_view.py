#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

from my315ok.socialorgnization.browser.orgnization_listing import OrgnizationsView

from Products.ATContentTypes.interfaces import IATFolder,IATFile
from Products.Five.utilities.marker import mark
from Products.CMFCore.interfaces import ISiteRoot

from my315ok.socialorgnization.content.administrativelicencefolder import IAdministrativeLicenceFolder
from my315ok.socialorgnization.content.annualsurveyfolder import IAnnualSurveyFolder
from my315ok.socialorgnization.content.orgnization import IOrgnization_administrative_licence
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey
from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder

class IContainerdownloadablelist(Interface):
    """
    This is really just a marker interface.search container all downloadable files,render them as table
    """

grok.templatedir('templates') 

class maintain(grok.View):
    grok.context(IOrgnizationFolder)
    grok.name('maintainview')
    grok.require('zope2.View')    
    
    def getMemberList(self):
        """获取申请的会议列表"""
#        mlist = []        
        catalog = getToolByName(self.context, "portal_catalog")        
        memberbrains = catalog({'object_provides':IOrgnization.__identifier__, 
                                'path':"/".join(self.context.getPhysicalPath()),
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              ) 
        return memberbrains
    
    def render(self):
        catalog = getToolByName(self.context, "portal_catalog")
        
        for i in self.getMemberList():
            title = i.Title
            brains = catalog({'path':i.getPath()})
#            import pdb
#            pdb.set_trace()
            for m in brains:
                obj = m.getObject()
                obj.title = title
                obj.reindexObject()
        return "pass" 


class maintainmarkinterface(grok.View):
    grok.context(ISiteRoot)
    grok.name('maintainmarker')
    grok.require('zope2.View')    
    
    def getMemberList(self):
        """获取申请的会议列表"""
#        mlist = []        
        catalog = getToolByName(self.context, "portal_catalog")
        memberbrains = catalog({'id':'biaogexiazai'})
        top = memberbrains[0].getPath()
        allfolders = self.getFolders(top)
         
        return allfolders
    
    def getFolders(self,path):
        """获取行政许可列表"""       
        catalog = getToolByName(self.context, "portal_catalog")

        braindata = catalog({'object_provides':IATFolder.__identifier__,
                             'path':path,                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        return braindata
    
    def render(self):
        j = 0
        for obj in self.getMemberList():
            j = j+1
            folder = obj.getObject()

            mark(folder,IContainerdownloadablelist)
        
        return "I has marked %s folders!" % (j)         


class ContainerDownloadableListView(OrgnizationsView):
    grok.context(IContainerdownloadablelist)
    grok.template('container_downloadable_list')
    grok.name('view')
    grok.require('zope2.View')
    
#    @memoize   
#    def catalog(self):                
#        catalog = getToolByName(self.context, "portal_catalog")
#        return catalog
        

    def getFolders(self):
        """获取行政许可列表"""       

        braindata = self.catalog()({'object_provides':IATFolder.__identifier__,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
 
    def getFiles(self):
        """获取行政许可列表"""

        braindata = self.catalog()({'object_provides':IATFile.__identifier__,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              ) 

        return braindata     

class AdministrativeLicenceFolderView(OrgnizationsView):
    grok.context(IAdministrativeLicenceFolder)
    grok.template('administrative_licence_folder')
    grok.name('view')
    grok.require('zope2.View')   
         
    
    @memoize
    def getAdministrativeLicenceList(self):
        """获取行政许可列表"""
       
        
        braindata = self.catalog()({'object_provides':IOrgnization_administrative_licence.__identifier__,
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

            
            out = """<tr>
            <td class="title"><a  target="_blank" href="%(objurl)s">%(title)s</a></td>
            <td class="item">%(audit_item)s</td>
            <td class="result">%(audit_result)s</td></tr>""" % dict(objurl=objurl,
                                            title=objtitle,
                                            audit_item= audit_item,
                                            audit_result=audit_result)           
            outhtml = outhtml + out
        return outhtml
    
    
class AnnualSurveyFolderView(OrgnizationsView):
    grok.context(IAnnualSurveyFolder)
    grok.template('annual_survey_folder')
    grok.name('view')
    grok.require('zope2.View')
    
    @memoize    
    def getAnnualSurveyList(self):
        """获取年检结果列表"""
       
        
        braindata = self.catalog()({'object_provides':IOrgnization_annual_survey.__identifier__,
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