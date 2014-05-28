The datagem API
===============

The main class for accessing the datagem API is ``dandelion.Datagem``.

Get entities
------------

Retrieving entities from dandelion is easy, just instantiate a datagem and iterate; pagination is implemented automatically for you, so don't worry and just get data::

    >>> from dandelion import Datagem
    >>> d = Datagem('administrative-regions')
    >>> for obj in d.items[:10]:
    ...     print(obj.acheneID)
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


Select fields
-------------

If you want to reduce the network load, you can retrieve only the fields you will actually use with ``select``::

    >>> from dandelion import Datagem
    >>> d = Datagem('administrative-regions')
    >>> for obj in d.items.select('acheneID')[:10]:
    ...     print(obj)
    ...
    {'acheneID': 'http://dandelion.eu/resource/158dce3ea58cebda9a14a911cd7574f204f9de72'}
    {'acheneID': 'http://dandelion.eu/resource/64b258d7bd8bc09d5a9e39c50dc619559e50ede1'}
    {'acheneID': 'http://dandelion.eu/resource/0c3cf5659edf75d0fe6405ab7536142abe9b5dfd'}
    {'acheneID': 'http://dandelion.eu/resource/4075688eac71a343555d717850c388d1c423ef47'}
    {'acheneID': 'http://dandelion.eu/resource/868f8130b42dc3cb183624faaa026ed540e12718'}
    {'acheneID': 'http://dandelion.eu/resource/84e931e49ea6805dff88adc0d77bdf41a57e1e96'}
    {'acheneID': 'http://dandelion.eu/resource/ead8025d8bfc2b89d5260760ade83743a86053b4'}
    {'acheneID': 'http://dandelion.eu/resource/6dd5e613714145c87f99d38a728be90c69a74e87'}
    {'acheneID': 'http://dandelion.eu/resource/97e3b6fae6bf7ba5c31e1173d1b1ebdbaae55a87'}
    {'acheneID': 'http://dandelion.eu/resource/c2c7f4f1c49cb49220aaec8028258afbce510c08'}

It is also possible to rename fields if you need to::

    >>> for obj in d.items.select('acheneID', 'name AS "label"')[:10]:
    ...     print(obj)
    ...
    {'acheneID': 'http://dandelion.eu/resource/158dce3ea58cebda9a14a911cd7574f204f9de72', 'label': 'Dresano'}
    {'acheneID': 'http://dandelion.eu/resource/64b258d7bd8bc09d5a9e39c50dc619559e50ede1', 'label': 'Vigolzone'}
    {'acheneID': 'http://dandelion.eu/resource/0c3cf5659edf75d0fe6405ab7536142abe9b5dfd', 'label': 'Battaglia Terme'}
    {'acheneID': 'http://dandelion.eu/resource/4075688eac71a343555d717850c388d1c423ef47', 'label': 'Capralba'}
    {'acheneID': 'http://dandelion.eu/resource/868f8130b42dc3cb183624faaa026ed540e12718', 'label': 'Cittadella'}
    {'acheneID': 'http://dandelion.eu/resource/84e931e49ea6805dff88adc0d77bdf41a57e1e96', 'label': 'Villa Faraldi'}
    {'acheneID': 'http://dandelion.eu/resource/ead8025d8bfc2b89d5260760ade83743a86053b4', 'label': 'Latina'}
    {'acheneID': 'http://dandelion.eu/resource/6dd5e613714145c87f99d38a728be90c69a74e87', 'label': 'Curinga'}
    {'acheneID': 'http://dandelion.eu/resource/97e3b6fae6bf7ba5c31e1173d1b1ebdbaae55a87', 'label': u"Canale d'Agordo"}
    {'acheneID': 'http://dandelion.eu/resource/c2c7f4f1c49cb49220aaec8028258afbce510c08', 'label': 'Morozzo'}


Filter entities
---------------

You can powerfully filter the result set with the ``where`` method::

    >>> for obj in d.items.where(level=60)[:10]:
    ...     print(obj.acheneID, obj.level)
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

More complex filters can be achieved with the ``__`` (dunder) operator::

    >>> for obj in d.items.where(level__gte=50)[:10]:
    ...     print(obj.acheneID, obj.parentNames.country)
    ...
    http://dandelion.eu/resource/c59b12fe31ac36662552c95d51cbf15b792094c0 ITALIA
    http://dandelion.eu/resource/bb5639dce81c1ba03dc2d91dee48fcf27d957b0d MAGYARORSZÁG
    http://dandelion.eu/resource/54a816ec3feb61a248aafced467b4a0c93525fd2 DEUTSCHLAND
    http://dandelion.eu/resource/a6af690fa57270328d9fb408729b78146fe36980 FRANCE
    http://dandelion.eu/resource/658a1e613bc710b41a731a4ceef57debd95dc017 DEUTSCHLAND
    http://dandelion.eu/resource/a97988a63d59dc8ca32e04b5fcbeeced78b36cf7 DEUTSCHLAND
    http://dandelion.eu/resource/d856e0303f3e7ac4970b809ee00d1d699702234d FRANCE
    http://dandelion.eu/resource/6e4f87ccea7f16bef46d22b3064dcb3664115175 DEUTSCHLAND
    http://dandelion.eu/resource/8ce01d5b914f712bf1a0c8ef586390e13790d9e9 DEUTSCHLAND
    http://dandelion.eu/resource/5c463680561d053fee0e653a0410b29b3f5b36b3 FRANCE


The available comparators are:
  * lte (lower-than-equals, ``<=``)
  * lt  (lower-than, ``<``)
  * gte (greater-than-equals, ``>=``)
  * gt  (greater-than, ``>``)
  * not (not, ``<>``)


Sort entities
-------------

Sorting is easy as everything else, with the ``order`` method::

    >>> for obj in d.items.select('acheneID').order('acheneID')[:5]:
    ...     print(obj.acheneID)
    ...
    http://dandelion.eu/resource/00017329d07750b26ffc0efb08c3a862b1898a0d
    http://dandelion.eu/resource/00026440c06c9774bfbb08e770167c9ad09124a1
    http://dandelion.eu/resource/0002abf01d8bdfcb13e5d01625c806ad2b3a06f3
    http://dandelion.eu/resource/0002e35e46df47106976c746606cc7188d1a039e
    http://dandelion.eu/resource/0003080a25b86105ba3f538b5d857b6a31b6646d


    >>> for obj in d.items.select('acheneID').order('acheneID DESC')[:5]:
    ...     print(obj.acheneID)
    ...
    http://dandelion.eu/resource/ffff40dff5241feb1ecc394e79bfd820d54d43d8
    http://dandelion.eu/resource/ffff31c2ec23ff3a18da4804cdbd869c11120ca7
    http://dandelion.eu/resource/fffb71883dbeaf8511f58a6d5260c5cb1c52be74
    http://dandelion.eu/resource/fffb636f2df4a5be30e3d56da3df2dc388a534a5
    http://dandelion.eu/resource/fffacd9ff1bdaca8107642a1048be2bef5796a53


Get the datagem version
-----------------------

Each datagem comes with a version that can be used to check whether the
data changed from the last query. This is available on the datagem itself:

    >>> d.version
    'b882dee6af3597804f2ed48bd27da798d3f114e6'

Please notice that calling ``d.version`` will effectively submit a query
to dandelion.eu, but the version itself will be cached for future calls.
