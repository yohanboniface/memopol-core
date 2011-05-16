#!/usr/bin/env python

from lxml.html.soupparser import parse
import json

import sys
tree=parse(sys.stdin)

res=[]
for issue in tree.xpath('//div[@name="Heading 1"]'):
    # get rapporteur, report id and report type
    tmp=issue.xpath('string()').strip()
    (tmp1, issue_type)=tmp.split(' - ')
    tmp=tmp1.split(' ')
    vote={'rapporteur': ' '.join(tmp[1:-1]),
          'report': tmp[-1],
          'issue_type': issue_type}
    # get timestamp
    vote['ts']=issue.xpath('following::td')[0].xpath('string()').strip()
    for decision in issue.xpath('ancestor::table')[0].xpath("following::table")[0:3]:
        total,k=[x.strip() for x in decision.xpath('.//text()') if x.strip()]
        vote[k]={'total': total, 'groups': {} }
        for cur in decision.xpath('../following-sibling::*'):
            if cur.xpath('.//table'):
                break
            group=cur.xpath('.//b/text()')
            if group:
                group=group[0].strip()
                vote[k][group]=[x.strip() for x in cur.xpath('.//b/following-sibling::text()')[0].split(', ')]
    cor=issue.xpath('ancestor::table')[0].xpath("following::table")[3]
    for row in cor.xpath('tr')[1:]:
        k,voters=[x.xpath('string()').strip() for x in row.xpath('td')]
        vote[k]['correctional']=[x.strip() for x in voters.split(', ')]
    res.append(vote)
print json.dumps(res)

