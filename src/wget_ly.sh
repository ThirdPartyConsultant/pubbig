#!/bin/bash


for i in 2 3 4 5 6 7 8
do
  wget -o tmp.html -X POST --header="Host: www.ly.gov.tw" \
  --header="User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36 " \
  --header="Accept: */*" \
  --header="Referer: http://www.ly.gov.tw/03_leg/0301_main/legList.action" \
  --header="Cookie: itrix_ns_id_1_200=l/tOo9RTVPjZGnTFK7VoQ3jfwUAA010; citrix_ns_id_1_200_.ly.gov.tw_%2F_wat=SlNFU1NJT05JRF9f?jPPS99iv4WkiTOJzkQug2FVqpo0A#AYWUS1kOziwagS0e1kKpvHTFjCkA&; JSESSIONID=33ABA21194F3BEEA7F93C2A813507522.jvm1; font=medium; style=null" \
  --post-data "queryFlag=true&searchValues%5B0%5D=&searchValues%5B1%5D=$i&searchValues%5B2%5D=&searchValues%5B3%5D=&searchValues%5B4%5D=&searchValues%5B5%5D=name&searchValues%5B6%5D=asc" \
  http://www.ly.gov.tw/03_leg/0301_main/legList.action

  sleep 2

done
