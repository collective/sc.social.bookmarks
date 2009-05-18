from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from sc.social.bookmarks.config import all_providers

class SocialBookmarksProvidersVocabulary(object):
    """
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        context = getattr(context, 'context', context)
        items = [ SimpleTerm(p.get('id'), p.get('id'), p.get('id'))
                  for p in all_providers]
        return SimpleVocabulary(items)

SocialBookmarksProvidersVocabularyFactory = SocialBookmarksProvidersVocabulary()