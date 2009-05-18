from zope.schema import Int
from zope.schema import TextLine
from zope.schema import Tuple
from zope.schema import Choice
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase

from zope.formlib.form import FormFields
from plone.app.controlpanel.form import ControlPanelForm
from zope.app.form.browser.itemswidgets import MultiSelectWidget as BaseMultiSelectWidget
from zope.app.form.browser.itemswidgets import OrderedMultiSelectWidget as BaseOrderedMultiSelectWidget
from plone.app.controlpanel.widgets import MultiCheckBoxThreeColumnWidget, MultiCheckBoxVocabularyWidget

from sc.social.bookmarks.config import default_providers
from sc.social.bookmarks import SocialBookmarksMessageFactory as _

class MultiSelectWidget(BaseMultiSelectWidget):
    """ """

    def __init__(self, field, request):
        """Initialize the widget."""
        super(MultiSelectWidget, self).__init__(field,
            field.value_type.vocabulary, request)

class OrderedMultiSelectWidget(BaseOrderedMultiSelectWidget):
    """ """

    def __init__(self, field, request):
        """Initialize the widget."""
        super(OrderedMultiSelectWidget, self).__init__(field,
            field.value_type.vocabulary, request)
            
class IProvidersSchema(Interface):
    
    bookmark_providers = Tuple(
        title=u'Bookmark providers',
        description=_(u'help_selected_providers',
            default=u"Please check any provider you want to be enabled to your visitors.",
        ),
        value_type=Choice(vocabulary="plone.app.vocabularies.SocialBookmarksProviders")
    )

    enabled_portal_types = Tuple(
        title=u'Content types',
        description=_(u'help_portal_types',
            default=u"Please select content types in which the viewlet will be applied.",
        ),
        value_type=Choice(vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
    )
    
class ProvidersControlPanelAdapter(SchemaAdapterBase):
    
    adapts(IPloneSiteRoot)
    implements(IProvidersSchema)
    
    def __init__(self, context):
        super(ProvidersControlPanelAdapter, self).__init__(context)
        portal_properties = getToolByName(context, 'portal_properties')
        self.context = portal_properties.sc_social_bookmarks_properties
    
    bookmark_providers = ProxyFieldProperty(IProvidersSchema['bookmark_providers'])
    enabled_portal_types = ProxyFieldProperty(IProvidersSchema['enabled_portal_types'])

class ProvidersControlPanel(ControlPanelForm):

    form_fields = FormFields(IProvidersSchema)
    form_fields['bookmark_providers'].custom_widget = OrderedMultiSelectWidget
    form_fields['enabled_portal_types'].custom_widget = MultiSelectWidget
    
    label = _('Social Bookmark Providers settings')
    description = _('Select Social Bookmarks Providers available for this site.')
    form_name = _('Providers')
