# Generic proxy to an INCF DAI hub

import urllib
import httplib2
import logging

from incf.dai.response import Response

logger = logging.getLogger('incf.dai')

class HubProxy(object):
    """ Generic proxy to an INCF DAI hub """

    def __init__(self, base_url, decorate=False):
        self.base_url = base_url
        # no cache for the time being
        # self.proxy = httplib2.Http('.cache')   
        self.proxy = httplib2.Http()
        if decorate:
            self._addCapabilities()

    def __call__(self, service_id, version=None, **kw):
        """Generic call method invoking
        <base_url>&version=<version>&request=<service_id><querystring>
        where the <querystring> is constructed from the keyword arguments"""
        url = self.base_url
        if version is not None:
            v = "&version=%s" % version
            url += v
        url = url + '&request=' + service_id +'&'
        qs = urllib.urlencode(kw)
        url += qs
        logger.info("Calling %s" % url)
        return Response(self.proxy.request(url, "GET"))

    # Every hub is required to provide this

    def GetCapabilities(self, output='xml'):
        """A list of all services provided by the hub"""
        return self('GetCapabilities', output=output)

    def DescribeProcess(self, version="1.0.0", output='xml'):
        """Detailed description of services at the hub"""
        return self('DescribeProcess', version=version, output=output)

    
    # some private helper methods

    def _addCapabilities(self):
        r =  self('GetCapabilities', output='xml')
        k1 = 'wps_ProcessOfferings'
        k2 = 'wps_Process'
        self.capabilities = tuple([l['ows_Identifier']
                                   for l in r[k1][k2]])
    
