python-dandelion
================

Connect to the dandelion.eu API in a very pythonic way!


Beta Disclaimer
---------------

This is a beta package, and may change dramatically. Not all the features are implemented as yet, but many are next to come. Please be patient, and perhaps write us to let us know you're out there, waiting for something.


Installation
------------

The dandelion.eu client is available on PyPI as `dandelion-eu`, so just run

    $ pip install dandelion-eu


Usage
-----

### Retrieve entities

Retrieving entities from dandelion is easy, just instantiate a Datagem and iterate; pagination is implemented automatically for you, so don't worry and just get data.

    >>> from dandelionimport Datagem
    >>> d = Datagem('datagem-slug')
    >>> for obj in d.objects[:10]:
    ...     print obj['acheneID']
    ...
    http://dandelion.eu/resource/158dce3ea58cebda9a14a911cd7574f204f9de72
    http://dandelion.eu/resource/64b258d7bd8bc09d5a9e39c50dc619559e50ede1
    http://dandelion.eu/resource/0c3cf5659edf75d0fe6405ab7536142abe9b5dfd
    http://dandelion.eu/resource/4075688eac71a343555d717850c388d1c423ef47
    http://dandelion.eu/resource/868f8130b42dc3cb183624faaa026ed540e12718
    http://dandelion.eu/resource/84e931e49ea6805dff88adc0d77bdf41a57e1e96
    http://dandelion.eu/resource/ead8025d8bfc2b89d5260760ade83743a86053b4
    http://dandelion.eu/resource/6dd5e613714145c87f99d38a728be90c69a74e87
    http://dandelion.eu/resource/97e3b6fae6bf7ba5c31e1173d1b1ebdbaae55a87
    http://dandelion.eu/resource/c2c7f4f1c49cb49220aaec8028258afbce510c08
    

### Select fields

If you want to reduce the network load, you can retrieve only the fields you will actually use with `select`:

    >>> from dandelionimport Datagem
    >>> d = Datagem('datagem-slug')
    >>> for obj in d.objects.select('acheneID')[:10]:
    ...     print obj
    ...
    {u'acheneID': u'http://dandelion.eu/resource/158dce3ea58cebda9a14a911cd7574f204f9de72'}
    {u'acheneID': u'http://dandelion.eu/resource/64b258d7bd8bc09d5a9e39c50dc619559e50ede1'}
    {u'acheneID': u'http://dandelion.eu/resource/0c3cf5659edf75d0fe6405ab7536142abe9b5dfd'}
    {u'acheneID': u'http://dandelion.eu/resource/4075688eac71a343555d717850c388d1c423ef47'}
    {u'acheneID': u'http://dandelion.eu/resource/868f8130b42dc3cb183624faaa026ed540e12718'}
    {u'acheneID': u'http://dandelion.eu/resource/84e931e49ea6805dff88adc0d77bdf41a57e1e96'}
    {u'acheneID': u'http://dandelion.eu/resource/ead8025d8bfc2b89d5260760ade83743a86053b4'}
    {u'acheneID': u'http://dandelion.eu/resource/6dd5e613714145c87f99d38a728be90c69a74e87'}
    {u'acheneID': u'http://dandelion.eu/resource/97e3b6fae6bf7ba5c31e1173d1b1ebdbaae55a87'}
    {u'acheneID': u'http://dandelion.eu/resource/c2c7f4f1c49cb49220aaec8028258afbce510c08'}
    
It is also possible to rename fields if you need to:

    >>> for obj in d.objects.select('acheneID', 'municipality.name AS "name"')[:10]:
    ...     print obj
    ...
    {u'acheneID': u'http://dandelion.eu/resource/158dce3ea58cebda9a14a911cd7574f204f9de72', u'name': u'Dresano'}
    {u'acheneID': u'http://dandelion.eu/resource/64b258d7bd8bc09d5a9e39c50dc619559e50ede1', u'name': u'Vigolzone'}
    {u'acheneID': u'http://dandelion.eu/resource/0c3cf5659edf75d0fe6405ab7536142abe9b5dfd', u'name': u'Battaglia Terme'}
    {u'acheneID': u'http://dandelion.eu/resource/4075688eac71a343555d717850c388d1c423ef47', u'name': u'Capralba'}
    {u'acheneID': u'http://dandelion.eu/resource/868f8130b42dc3cb183624faaa026ed540e12718', u'name': u'Cittadella'}
    {u'acheneID': u'http://dandelion.eu/resource/84e931e49ea6805dff88adc0d77bdf41a57e1e96', u'name': u'Villa Faraldi'}
    {u'acheneID': u'http://dandelion.eu/resource/ead8025d8bfc2b89d5260760ade83743a86053b4', u'name': u'Latina'}
    {u'acheneID': u'http://dandelion.eu/resource/6dd5e613714145c87f99d38a728be90c69a74e87', u'name': u'Curinga'}
    {u'acheneID': u'http://dandelion.eu/resource/97e3b6fae6bf7ba5c31e1173d1b1ebdbaae55a87', u'name': u"Canale d'Agordo"}
    {u'acheneID': u'http://dandelion.eu/resource/c2c7f4f1c49cb49220aaec8028258afbce510c08', u'name': u'Morozzo'}
    

### Filter elements

You can powerfully filter the result set with the `where` method:

    >>> for obj in d.objects.where(level=60)[:10]:
    ...     print obj['acheneID'], obj['level']
    ...
    http://dandelion.eu/resource/a7d36ba742d54e8a97f187cf3d33a3beb6043057 60
    http://dandelion.eu/resource/d85a893151f0c9a9a1c051c551055edf41407352 60
    http://dandelion.eu/resource/f448261a110513dde5180cf3be0305a15fe28330 60
    http://dandelion.eu/resource/e2741382cd6cde34bfebd431bfc9f0548c9f1ac9 60
    http://dandelion.eu/resource/7d3f8fe92130f34831c5a82f13770f58f5e3ac81 60
    http://dandelion.eu/resource/da5ee9e7d3338e89fd5c7320aaca308c31c0dbe1 60
    http://dandelion.eu/resource/0b248956924d31a074847f79143c827cf04ed0e0 60
    http://dandelion.eu/resource/241ffa8191ac887462cff37cbf422afb4c70e227 60
    http://dandelion.eu/resource/eee2414d9fb3f4bd8064cb7d5f56e5184adf8c40 60
    http://dandelion.eu/resource/1fcf480584ce8b0ef1fe8b776f7c8811ea1405b3 60
    
More complex filters can be achieved with the `__` (dunder) operator:

    >>> for obj in d.objects.where(level__lt=30)[:10]:
    ...     print obj['acheneID'], obj['country']['name']
    ...
    http://dandelion.eu/resource/3058697c2d534d13b48f20e1d530dea1794d58b2 FRANCE
    http://dandelion.eu/resource/40b70d14ef12aaef8a90faaa0968ba627043c6ac EESTI
    http://dandelion.eu/resource/0d33fdb63fd80f69fa00984bd829583ec71e08b2 ROMÂNIA
    http://dandelion.eu/resource/00167ef9677650a7ac7c230e298eed31442a83d2 ESPAÑA
    http://dandelion.eu/resource/f96621f3eb48c77627377ccefb566e229350db12 БЪЛГАРИЯ / BULGARIA
    http://dandelion.eu/resource/94b06ea96c1f9c9fc8e92ff3df24930de87184d0 ΕΛΛΑΔΑ / ELLADA
    http://dandelion.eu/resource/ba58d9e420f50e0f8c0973cab82e6f5886fb3c26 MAGYARORSZÁG
    http://dandelion.eu/resource/b186379b8be70eabf5a03c41ebfeb85a6dedd5ed SVERIGE
    http://dandelion.eu/resource/b2889388bcd0207fc72437a1fd277de465bcf9d8 ÖSTERREICH
    http://dandelion.eu/resource/dbf4ee5bd5858878c543c6b6148b568de42a8d30 LATVIJA

Available comparators are:
  
  * lte (lower-than-equals, `<=`)
  * lt  (lower-than, `<`)
  * gte (greater-than-equals, `>=`)
  * gt  (greater-than, `>`)
  * not (not, `<>`)


### Sort elements

Sorting is easy as everything else, with the `sort` method:

    >>> for obj in d.objects.select('acheneID').order('acheneID')[:5]:
    ...     print obj['acheneID']
    ...
    http://dandelion.eu/resource/00017329d07750b26ffc0efb08c3a862b1898a0d
    http://dandelion.eu/resource/00026440c06c9774bfbb08e770167c9ad09124a1
    http://dandelion.eu/resource/0002abf01d8bdfcb13e5d01625c806ad2b3a06f3
    http://dandelion.eu/resource/0002e35e46df47106976c746606cc7188d1a039e
    http://dandelion.eu/resource/0003080a25b86105ba3f538b5d857b6a31b6646d


    >>> for obj in d.objects.select('acheneID').order('acheneID DESC')[:5]:
    ...     print obj['acheneID']
    ...
    http://dandelion.eu/resource/ffff40dff5241feb1ecc394e79bfd820d54d43d8
    http://dandelion.eu/resource/ffff31c2ec23ff3a18da4804cdbd869c11120ca7
    http://dandelion.eu/resource/fffb71883dbeaf8511f58a6d5260c5cb1c52be74
    http://dandelion.eu/resource/fffb636f2df4a5be30e3d56da3df2dc388a534a5
    http://dandelion.eu/resource/fffacd9ff1bdaca8107642a1048be2bef5796a53
