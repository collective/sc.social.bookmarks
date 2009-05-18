sc.social.bookmarks
===================

Overview
--------

This product adds a Bookmark & Share action to a Plone 3 site. 

It allows an anonymous or registered user to bookmark or share a content from a 
Plone site to a service like Delicious, Digg, Reddit or Twitter (62 providers 
already included).

Requirements
------------

    - Plone 3.1.x (http://plone.org/products/plone)

    - Plone 3.2.x (http://plone.org/products/plone)
    
Installation
------------
    
To enable this product,on a buildout based installation:

    1. Edit your buildout.cfg and add ``sc.social.bookmarks``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            sc.social.bookmarks

    2. Tell the plone.recipe.zope2instance recipe to install a ZCML slug::

        [instance]
        ...
        zcml = 
            ...
            sc.social.bookmarks
    

If another package depends on the sc.social.bookmarks egg or 
includes its zcml directly you do not need to specify anything in the 
buildout configuration: buildout will detect this automatically.

After updating the configuration you need to run the ''bin/buildout'',
which will take care of updating your system.

Go to the 'Site Setup' page in the Plone interface and click on the
'Add/Remove Products' link.

Choose the product (check its checkbox) and click the 'Install' button.

Uninstall -- This can be done from the same management screen, but only
if you installed it from the quick installer.

Note: You may have to empty your browser cache and save your resource registries
in order to see the effects of the product installation.

Browsers and OS's
-----------------

    * Internet Explorer 7.0 (WinXP/Vista)
    
    * Firefox 3 (WinXP/Vista/MacOSX)
    
    * Safari 3 (WinXP/MacOSX)

Sponsoring
----------

Development of this product was sponsored by `Simples Consultoria 
<http://www.simplesconsultoria.com.br/>`_.


Credits
-------

    * Thiago Tamosauskas (thiago at simplesconsultoria dot com dot br) - 
      Implementation
    
    * Erico Andrei (erico at simplesconsultoria dot com dot br) - Packaging and
      plumbing.
