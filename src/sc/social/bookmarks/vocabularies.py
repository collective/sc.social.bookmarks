# -*- coding: utf-8 -*-
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class SBProvidersVocabulary(object):
    """Vocabulary factory for existing bookmark providers

    >>> from zope.component import queryUtility

    >>> name = 'plone.app.vocabularies.SocialBookmarksProviders'
    >>> util = queryUtility(IVocabularyFactory, name)

    >>> providers = util()
    >>> providers
    <zope.schema.vocabulary.SimpleVocabulary object at ...>

    >>> len(providers.by_token) > 0
    True

    >>> doc = providers.by_token['Reddit']
    >>> doc.title, doc.token, doc.value
    ('Reddit', 'Reddit', 'Reddit')
    """

    def __call__(self, context=None):
        reg = getUtility(IRegistry)
        providers_keys = [
            k
            for k in reg.records.keys()
            if k.startswith("sc.social.bookmarks.providers")
        ]
        providers_keys.sort()
        providers = [reg[k] for k in providers_keys]
        items = [SimpleTerm(p.get("id"), p.get("id"), p.get("id")) for p in providers]
        return SimpleVocabulary(items)


SocialBookmarksProvidersVocabularyFactory = SBProvidersVocabulary()
