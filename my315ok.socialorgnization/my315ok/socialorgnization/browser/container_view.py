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
from my315ok.socialorgnization.content.orgnization import IOrgnization_annual_survey,IOrgnization
from my315ok.socialorgnization.content.orgnizationfolder import IOrgnizationFolder

from plone.dexterity.utils import createContentInContainer
from plone.i18n.normalizer.interfaces import IUserPreferredFileNameNormalizer

class IContainerdownloadablelist(Interface):
    """
    This is really just a marker interface.search container all downloadable files,render them as table
    """

grok.templatedir('templates') 

class maintain(grok.View):
    grok.context(IOrgnizationFolder)
    grok.name('maintainview')
    grok.require('cmf.ManagePortal')     
    
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
# set default annual survey recoder    
    def render(self):
        catalog = getToolByName(self.context, "portal_catalog")
        jibenhege = ["湘潭市杂文学会",
"湘潭市农村经济学会",
"湘潭市护理学会",
"湘潭市医学会",
"湘潭市粮食经济科技学会",
"湘潭市民俗文化学会",
"湘潭市干部教育研究会",
"湘潭市集邮协会",
"湘潭市电子信息行业协会",
"湘潭市农业机械流通行业协会",
"湘潭市烟草学会",
"湘潭钢铁公司职工技术协会",
"湘潭市戏剧家协会","湘潭海峡两岸经贸发展促进会","湘潭齐白石研究会",
"湘潭市政策科学研究会",
"湘潭市少年儿童文学艺术家协会",
"湘潭市音乐家协会",
"湘潭市专业技术人员奖励工作促进会",
"湘潭市妇女人才联谊会",
"湘潭市市场发展促进会",
"湘潭市房地产开发协会",
"湘潭市民间文艺家协会",
"湘潭市国际标准舞协会",
"湘潭市气象学会",
"湘潭市翻译工作者协会",
"湘潭市九华示范区个体劳动者私营企业协会",
"湘潭市心理学会",
"湘潭市振兴湘宁经济联谊会",
"湘潭市舞蹈家协会"
]
#title value is bytestr that encoded by utf-8        
        for i in self.getMemberList():
            title = i.Title
            
            brains = catalog({'path':i.getPath(),'object_provides':IOrgnization_annual_survey.__identifier__})
            num = len(brains)
            if num == 0:
#                import pdb
#                pdb.set_trace()

                newid = u"2012年检"
                if not isinstance(newid, unicode):
                    newid = unicode(newid, 'utf-8')
                surveyid = IUserPreferredFileNameNormalizer(self.request).normalize(newid)
                item =createContentInContainer(i.getObject(),"my315ok.socialorgnization.orgnizationsurvey",checkConstraints=False,id=surveyid)
                item.title = title
                if title in jibenhege:
                    item.annual_survey = "jibenhege"
                else:                                                                                
                    item.annual_survey = "hege"
                item.year = "2012"
                item.reindexObject()
                 
            
#            import pdb
#            pdb.set_trace()
#            for m in brains:
#                obj = m.getObject()
#                obj.title = title
#                obj.reindexObject()
        return "pass" 


class maintainmarkinterface(grok.View):
    grok.context(ISiteRoot)
    grok.name('maintainmarker')
    grok.require('cmf.ManagePortal')     
    
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

    @memoize
    def getDownloadFileList(self):
        """获取行政许可列表"""
       
        
        braindata = self.catalog()({'object_provides':IATFile.__identifier__,
                             'path':"/".join(self.context.getPhysicalPath()),                                     
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        outhtml = """<table class="table table-striped table-bordered table-condensed"><thead>
        <tr><th class="span7">文件名称</th><th class="span3" >发布时间</th><th class="span2" >下载链接</th></tr>
        </thead><tbody>"""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            pubtime = braindata[i].created.strftime('%Y-%m-%d')
            downloadlink = objurl + "/download"

            
            out = """<tr>
            <td class="span7 title">%(title)s</td>
            <td class="span3 item">%(pubtime)s</td>
            <td class="span2 result"><a href="%(downloadlink)s">下载</a></td></tr>""" % dict(objurl=objurl,
                                            title = objtitle,
                                            pubtime = pubtime,
                                            downloadlink = downloadlink)           
            outhtml = outhtml + out
        outhtml = outhtml + "</tbody></table>"
        return outhtml        

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