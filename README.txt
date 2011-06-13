sc.social.bookmarks
===================

Overview
--------

This product adds a Bookmark & Share action to a Plone 4 site. 

It allows an anonymous or registered user to bookmark or share a content from a 
Plone site to a service like Delicious, Digg, Reddit or Twitter (62 providers 
already included).


Requirements
------------

    - Plone 4.x (http://plone.org/products/plone)


Installation
------------
    
To enable this product,on a buildout based installation:

    1. Edit your buildout.cfg and add ``sc.social.bookmarks``
       to the list of eggs to install ::

        [buildout]
        ...
        eggs = 
            sc.social.bookmarks

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

This package has been tested with the following browsers and OS's:

    * Google Chrome (Linux/Win7/WinXP/MacOSX)

    * Internet Explorer 7.0 (WinXP/Vista)
    
    * Firefox 4 beta9 (Linux)
    
    * Firefox 3 (WinXP/Vista/MacOSX)
    
    * Safari 3 (WinXP/MacOSX)


Sponsoring
----------

Development of this product was sponsored by `Simples Consultoria 
<http://www.simplesconsultoria.com.br/>`_.


Contributors
------------

    * Johannes Raggam - Refactoring, portlet and conversion to jQuery

    * Héctor Velarde - Plone 4 support, uninstall profile 

    * Thiago Tamosauskas (thiago at simplesconsultoria dot com dot br) - 
      Implementation
    
    * Erico Andrei (erico at simplesconsultoria dot com dot br) - Packaging and
      plumbing.
    
    * Johannes Raggam - Refactoring, portlet and conversion to jQuery
    
    * Robert Niederreiter - This and that

