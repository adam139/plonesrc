import unittest2 as unittest

from my315ok.socialorgnization.testing import MY315OK_PRODUCTS_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, setRoles
from plone.namedfile.file import NamedImage

class Allcontents(unittest.TestCase):
    layer = MY315OK_PRODUCTS_INTEGRATION_TESTING
    
    def setUp(self):
        portal = self.layer['portal']
        setRoles(portal, TEST_USER_ID, ('Manager',))

        portal.invokeFactory('my315ok.socialorgnization.orgnizationfolder', 'orgnizationfolder1')
        portal.invokeFactory('my315ok.socialorgnization.shaoshanshifolder', 'shaoshanshi')
        portal.invokeFactory('my315ok.socialorgnization.xiangxiangshifolder', 'xiangxiangshi')
        portal.invokeFactory('my315ok.socialorgnization.xiangtanxianfolder', 'xiangtanxian')
        portal.invokeFactory('my315ok.socialorgnization.yuetangqufolder', 'yuetangqu')
        portal.invokeFactory('my315ok.socialorgnization.yuhuqufolder', 'yuhuqu')  
        portal.invokeFactory('my315ok.socialorgnization.shibenjifolder', 'shibenji')                                               

        
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization1',
                                                   title="organization1")
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationadministrative','orgnizationadministrative1',
                                                   title="organization1")        
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization2')
        portal['orgnizationfolder1'].invokeFactory('my315ok.socialorgnization.orgnization','orgnization3')        
        portal['orgnizationfolder1']['orgnization1'].invokeFactory('my315ok.socialorgnization.orgnizationsurvey','orgnizationsurvey1',
                                                   title="orgnizationfolder1")
       
        self.portal = portal
                
    def test_marketfolder(self):
        self.assertEqual(self.portal['orgnizationfolder1'].id,'orgnizationfolder1')
        self.assertEqual(self.portal['shaoshanshi'].id,'shaoshanshi')
        self.assertEqual(self.portal['xiangxiangshi'].id,'xiangxiangshi')
        self.assertEqual(self.portal['xiangtanxian'].id,'xiangtanxian')
        self.assertEqual(self.portal['yuhuqu'].id,'yuhuqu')
        self.assertEqual(self.portal['yuetangqu'].id,'yuetangqu')        
        self.assertEqual(self.portal['shibenji'].id,'shibenji')                                             
    

    
    def test_meetapply(self):
        self.assertEqual(self.portal['orgnizationfolder1']['orgnization1'].id,'orgnization1')
        self.assertEqual(self.portal['orgnizationfolder1']['orgnization1']['orgnizationsurvey1'].id,'orgnizationsurvey1')        
        self.assertEqual(self.portal['orgnizationfolder1']['orgnization1']['orgnizationadministrative1'].id,'orgnizationadministrative1')     
    
        