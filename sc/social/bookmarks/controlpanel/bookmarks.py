from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import Tuple

from sc.social.bookmarks import _


class IProvidersSchema(Interface):

    bookmark_providers = Tuple(
        title=_(u'Bookmark providers'),
        description=_(u'help_selected_providers',
            default=u"Please check any provider you want to be enabled to your visitors.",
        ),
        value_type=Choice(vocabulary="plone.app.vocabularies.SocialBookmarksProviders")
    )

    enabled_portal_types = Tuple(
        title=_(u'Content types'),
        description=_(u'help_portal_types',
            default=u"Please select content types in which the viewlet will be applied.",
        ),
        value_type=Choice(vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes")
    )

    use_as_action = Bool(
        title=_(u'Use as a content action?'),
        description=_(u'help_use_as_content_action',
            default=u"Check this if you want the social bookmarks to appear as an action for contents.",
        ),
    )

    show_icons_only = Bool(
        title=_(u'Show icons only?'),
        description=_(u'help_show_icons_only',
            default=u"Check this if you want the social bookmarks to be rendered as icons only.",
        ),
    )



class ProvidersControlPanelEditForm(RegistryEditForm):
    schema = IProvidersSchema
    schema_prefix = 'sc.social.bookmarks'

    label = _(u'Social Bookmark Providers settings')
    description = _(u"""Select Social Bookmarks Providers available for this
                        site.""")

ProvidersControlPanel = layout.wrap_form(ProvidersControlPanelEditForm,
                                         ControlPanelFormWrapper)
