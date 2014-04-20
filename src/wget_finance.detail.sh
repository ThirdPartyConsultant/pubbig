#!/bin/bash

wget -O $2 -o tmp.html -X GET --header="Host: sunshine.cy.gov.tw" \
--header="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36 " \
--header="Accept: */*" \
--header="Referer: http://sunshine.cy.gov.tw/GipOpenWeb/wSite/sp?xdUrl=/wSite/SpecialPublication/SpecificLP.jsp" http://sunshine.cy.gov.tw/GipOpenWeb/wSite/SpecialPublication/fileDownload.jsp?id=$1

