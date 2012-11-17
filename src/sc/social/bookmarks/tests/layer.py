from Testing import ZopeTestCase as ztc

from Products.PloneTestCase import ptc
from Products.PloneTestCase import layer
from Products.Five import zcml
from Products.Five import fiveconfigure

ptc.setupPloneSite(
    extension_profiles=('sc.social.bookmarks:default', )
)

class SocialBookmarksLayer(layer.PloneSite):
    """Configure sc.social.bookmarks"""

    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        import sc.social.bookmarks
        zcml.load_config("configure.zcml", sc.social.bookmarks)
        fiveconfigure.debug_mode = False
        ztc.installPackage("sc.social.bookmarks", quiet=1)

    @classmethod
    def tearDown(cls):
        pass

