# -*- coding: utf-8 -*-
from Products.CMFPlone import PloneMessageFactory as _
from z3c.table import batch
from zope.i18n import translate
from ZTUtils import make_query
from ZTUtils import url_query
from six.moves import range


try:
    from plone.batching.utils import calculate_pagerange, calculate_pagenumber
    calculate_pagerange
    calculate_pagenumber
except ImportError:
    from Products.CMFPlone.PloneBatch import calculate_pagenumber
    from Products.CMFPlone.PloneBatch import calculate_pagerange


LINK = '<a href="{url:s}" title="{label:s}">{label:s}</a>'


class PloneBatch(object):

    def __init__(self, batch, pagerange=7):
        self.batch = batch

        # Set up the total number of pages
        self.numpages = calculate_pagenumber(len(self.batch.sequence),
                                             self.batch.size)

        # Set up the current page number
        self.pagenumber = calculate_pagenumber(self.batch.start + 1,
                                               self.batch.size)

        # Set up pagerange for the navigation quick links
        self.pagerange, self.pagerangestart, self.pagerangeend = (
            calculate_pagerange(self.pagenumber, self.numpages, pagerange))

        # Set up the lists for the navigation: 4 5 [6] 7 8
        #  navlist is the complete list, including pagenumber
        #  prevlist is the 4 5 in the example above
        #  nextlist is 7 8 in the example above
        self.navlist = self.prevlist = self.nextlist = []
        if self.pagerange and self.numpages >= 1:
            self.navlist = list(range(self.pagerangestart, self.pagerangeend))
            self.prevlist = list(range(self.pagerangestart, self.pagenumber))
            self.nextlist = list(range(self.pagenumber + 1, self.pagerangeend))

    @property
    def showfirst(self):
        return 1 not in self.navlist

    @property
    def dotsafterfirst(self):
        return 2 not in self.navlist

    @property
    def dotsbeforelast(self):
        return self.batch.total - 1 not in self.navlist

    @property
    def showlast(self):
        return self.batch.total not in self.navlist


class BatchProvider(batch.BatchProvider):

    def update(self):
        self.plonebatch = PloneBatch(self.batch)

    def render(self):
        results = []
        results.append('<nav class="pagination">')
        results.append('<ul>')
        results.extend(self.previousItemsLink())
        results.extend(self.firstLink())
        results.extend(self.previousLinks())
        results.extend(self.current())
        results.extend(self.nextLinks())
        results.extend(self.lastLink())
        results.extend(self.nextItemsLink())
        results.append('</ul>')
        results.append('</nav>')
        return '\n'.join(results)

    def previousItemsLink(self):
        result = []
        if self.batch.previous:
            result.append('<li class="previous">')
            index = self.batch.index - 1
            numberitems = len(self.batches[index])
            label = '&laquo; '
            messageid = _('batch_previous_x_items',
                          default='Previous ${number} items',
                          mapping=dict(number=str(numberitems)))
            label += translate(messageid, context=self.request)
            url = self.makeUrl(index)
            link = self.makeLink(url, label)
            result.append(link)
            result.append('</li>')
        return result

    def nextItemsLink(self):
        result = []
        if self.batch.next:
            result.append('<li class="next">')
            index = self.batch.index + 1
            numberitems = len(self.batches[index])
            messageid = _('batch_next_x_items',
                          default='Next ${number} items',
                          mapping=dict(number=str(numberitems)))
            label = translate(messageid, context=self.request)
            label += ' &raquo;'
            url = self.makeUrl(index)
            link = self.makeLink(url, label)
            result.append(link)
            result.append('</li>')
        return result

    def makeLink(self, url, label):
        return LINK.format(url=url, label=label)

    def makeUrl(self, index):
        batch = self.batches[index]
        query = {self.table.prefix + '-batchStart': batch.start,
                 self.table.prefix + '-batchSize': batch.size}
        querystring = make_query(query)
        base = url_query(self.request, omit=list(query.keys()))
        return '{0:s}&{1:s}'.format(base, querystring)

    def firstLink(self):
        result = []
        if self.plonebatch.showfirst:
            result.append('<li>')
            url = self.makeUrl(0)
            label = '1'
            result.append(self.makeLink(url, label))
            result.append('</li>')
            if self.plonebatch.dotsafterfirst:
                result.append('<li>')
                result.append('<span>')
                result.append('&hellip;')
                result.append('</span>')
                result.append('</li>')
        return result

    def previousLinks(self):
        result = []
        for number in self.plonebatch.prevlist:
            url = self.makeUrl(number - 1)
            label = str(number)
            result.append('<li>')
            result.append(self.makeLink(url, label))
            result.append('</li>')
        return result

    def current(self):
        return [
            '<li class="active">',
            '<span>',
            str(self.batch.number),
            '</span>',
            '</li>'
        ]

    def nextLinks(self):
        result = []
        for number in self.plonebatch.nextlist:
            url = self.makeUrl(number - 1)
            label = str(number)
            result.append('<li>')
            result.append(self.makeLink(url, label))
            result.append('</li>')
        return result

    def lastLink(self):
        result = []
        if self.plonebatch.showlast:
            if self.plonebatch.dotsbeforelast:
                result.append('<li>')
                result.append('<span>')
                result.append('&hellip;')
                result.append('</span>')
                result.append('</li>')
            result.append('<li>')
            url = self.makeUrl(self.batch.total - 1)
            label = str(self.batch.total)
            result.append(self.makeLink(url, label))
            result.append('</li>')
        return result
