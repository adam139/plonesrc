#-*- coding: UTF-8 -*-
from five import grok
from zope.interface import Interface
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

from my315ok.socialorgnization.browser.orgnization_listing import OrgnizationsView

from Products.ATContentTypes.interfaces import IATFolder,IATFile,IATDocument
from plone.app.collection.interfaces import ICollection

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

class IContainerTablelist(Interface):
    """
    This is really just a marker interface.search container all contents,render them as table
    """

class IPunishTablelist(Interface):
    """
    This is really just a marker interface.search container all contents,render them as table
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
    def render3(self):
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
        return "pass"
     
    def render(self):
        catalog = getToolByName(self.context, "portal_catalog")
        minfei = ["湘潭市益智实验中学",
"湘潭文理专修学院",
"湘潭市泽民中医类风湿病研究中心",
"湘潭融城设计艺术职业学校",
"湘潭新华电脑学校",
"湘潭厨师、服务师培训中心",
"湘潭市现代职业培训中心",
"湘潭市少儿特长启蒙学校",
"湘潭市民生社区综合服务中心",
"湘潭市精益眼视光研究所",
"湘潭市糖尿病中医中药临床研究中心",
"湘潭市飞翔职业技能培训中心",
"湘潭市佳程涉外职业培训学校",
"湘潭市世纪风职业培训学校",
"湘潭市红十字建春医院",
"湘潭市红十字湘仁医院",
"湘潭市体育健康服务指导中心",
"湘潭天英职业技能培训学校",
"湘潭市华顺职业培训中心",
"湘潭市同升国济职业技能培训学校",
"湘潭千里马职业教育培训中心",
"湖南吉利汽车职业技术学院",
"湖南软件职业学院",
"湖南汽车工程师专修学院",
"湘潭新时代医院",
"湘潭市金康白癜风中医中药临床治疗研究中心",
"湘潭湘商文化研究中心",
"湘潭市银海家政服务员职业技能培训",
"湘潭市美术创作中心",
"湘潭易道馆跆拳道培训中心",
"湘潭市人力资源培训学校",
"湘潭市创益扶困咨询中心",
"湘潭市永胜工程机械培训学校",
"湘潭市工商适应技术学校",
"湘潭市中凯人机速记职业培训中心",
"湘潭市金梦园居家养老服务中心",
"湘潭市阳光青少年俱乐部",
"湘潭市荆鹏职业教育培训中心",
"湘潭市德盛职业技能培训学校",
"湘潭市飞扬跆拳道培训中心",
"湘潭市童心幼儿园",
"湘潭市圆梦园小区童之园幼儿园",
"湘潭市易家湾南天幼儿园",
"湘潭市健康幼儿园二分园"
]
#title value is bytestr that encoded by utf-8        
        for i in self.getMemberList():
            title = i.Title
            if title in minfei:
                obj = i.getObject()
                obj.organization_type = "minfei"
                obj.reindexObject()          

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

class addtablemarkinterface(grok.View):
    grok.context(ISiteRoot)
    grok.name('addtablelist')
    grok.require('cmf.ManagePortal')     
    
    def getMemberList(self):
        """获取申请的会议列表"""
#        mlist = []        
        catalog = getToolByName(self.context, "portal_catalog")
#        memberbrains = catalog({'id':'shehuizuzhifengcai'})
        memberbrains = catalog({'id':'chachujieguogonggao','object_provides':IATFolder.__identifier__})
#        import pdb
#        pdb.set_trace()        
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

            mark(folder,IContainerTablelist)
        
        return "I has marked %s folders!" % (j) 

class addFolderDownloadablelistmarkinterface(grok.View):
## mark the current folder     
    grok.context(IATFolder)
    grok.name('adddownloadablelist')
    grok.require('cmf.ManagePortal') 
    
    def render(self):
        folder = self.context

        if not IContainerdownloadablelist.providedBy(folder):
            mark(folder,IContainerdownloadablelist)
            return "I has marked the folders as Containerdownloadablelist!" 
        else:
            return "It has been marked as Containerdownloadablelist!"    

class addFoldertablemarkinterface(grok.View):
## mark the current folder     
    grok.context(IATFolder)
    grok.name('addtable')
    grok.require('cmf.ManagePortal') 
    
    def render(self):
        folder = self.context

        if not IContainerTablelist.providedBy(folder):
            mark(folder,IContainerTablelist)
            return "I has marked the folders as Foldertablelist!" 
        else:
            return "It has been marked as Foldertablelist!"

class addFolderPunishtablemarkinterface(grok.View):
## mark the current folder     
    grok.context(IATFolder)
    grok.name('addpunishtable')
    grok.require('cmf.ManagePortal') 
    
    def render(self):
        folder = self.context

        if not IPunishTablelist.providedBy(folder):
            mark(folder,IPunishTablelist)
            return "I has marked the folders as FolderPunishtablelist!" 
        else:
            return "It has been marked as FolderPunishtablelist!"
        

class ContainerDownloadableListView(OrgnizationsView):
    grok.context(IContainerdownloadablelist)
    grok.template('container_downloadable_list')
    grok.name('view')
    grok.require('zope2.View')
    

        

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

class ContainerTableListView(OrgnizationsView):
    grok.context(IContainerTablelist)
    grok.template('container_table_list')
    grok.name('view')
    grok.require('zope2.View')        

    def getFolders(self):
        """获取当前目录所有文件夹对象"""       

        braindata = self.catalog()({'object_provides':IATFolder.__identifier__,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
 
    def getATDocuments(self):
        """获取所有页面"""

        try:
            from my315ok.products.product import Iproduct
            braindata = self.catalog()({'object_provides':[IATDocument.__identifier__,Iproduct.__identifier__],
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              ) 
        except:
            
            braindata = self.catalog()({'object_provides':IATDocument.__identifier__,
                             'path':"/".join(self.context.getPhysicalPath()),                                  
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              ) 

        return braindata 

    @memoize
    def getTableList(self):
        """获取行政许可列表"""
       
        
#        braindata = self.catalog()({'object_provides':IATDocument.__identifier__,
#                             'path':"/".join(self.context.getPhysicalPath()),                                     
#                             'sort_order': 'reverse',
#                             'sort_on': 'created'}                              
#                                              )
        braindata = self.getATDocuments()
        outhtml = """<table class="table table-striped table-bordered table-condensed"><thead>
        <tr><th class="span9">标题</th><th class="span3" >发布时间</th></tr>
        </thead><tbody>"""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            pubtime = braindata[i].created.strftime('%Y-%m-%d')
#            downloadlink = objurl + "/download"

            
            out = """<tr>
            <td class="span9 title"><a href="%(url)s">%(title)s</a></td>
            <td class="span3 item">%(pubtime)s</td>
            </tr>""" % dict(url = objurl,title = objtitle,pubtime = pubtime)           
            outhtml = outhtml + out
        outhtml = outhtml + "</tbody></table>"
        return outhtml 

class AdminstrativePunishTableListView(ContainerTableListView):
    grok.context(IPunishTablelist)
    grok.template('administrative_punish_table_list')
    grok.name('view')
    grok.require('zope2.View')
    
    
    @memoize
    def getTableList(self):
        """获取行政许可列表"""
       
        
        braindata = self.catalog()({'object_provides':IATDocument.__identifier__,
                             'path':"/".join(self.context.getPhysicalPath()),                                     
                             'sort_order': 'reverse',
                             'sort_on': 'created'}                              
                                              )
        outhtml = """<table class="table table-striped table-bordered table-condensed"><thead>
        <tr><th class="span9">社会组织名称</th><th class="span3" >发布时间</th></tr>
        </thead><tbody>"""
        brainnum = len(braindata)
        
        for i in range(brainnum):
            objurl = braindata[i].getURL()
            objtitle = braindata[i].Title
            pubtime = braindata[i].created.strftime('%Y-%m-%d')
            
            out = """<tr>
            <td class="span9 title"><a href="%(url)s">%(title)s</a></td>
            <td class="span3 item">%(pubtime)s</td>
            </tr>""" % dict(url = objurl,title = objtitle,pubtime = pubtime)           
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
                             'sort_on': 'orgnization_annual_survey'})
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