#-*- coding: UTF-8 -*-
from five import grok
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from my315ok.socialorgnization.browser.orgnization_listing import OrgnizationsView


from my315ok.socialorgnization.content.administrativelicencefolder import IAdministrativeLicenceFolder
from my315ok.socialorgnization.content.annualsurveyfolder import IAnnualSurveyFolder
from my315ok.socialorgnization.content.orgnization import IOrgnization_administrative_licence
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey

grok.templatedir('templates') 

class AdministrativeLicenceFolderView(OrgnizationsView):
    grok.context(IAdministrativeLicenceFolder)
    grok.template('administrative_licence_folder')
    grok.name('view')
    grok.require('zope2.View')   
         
    
    @memoize
    def getAdministrativeLicenceList(self):
        """获取行政许可列表"""
       
        catalog = getToolByName(self.context, "portal_catalog")
        braindata = catalog({'object_provides':IOrgnization_administrative_licence.__identifier__,
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
       
        catalog = getToolByName(self.context, "portal_catalog")
        braindata = catalog({'object_provides':IOrgnization_annual_survey.__identifier__,
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