import re
import requests

IP_REGEX = re.compile(".*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?")

INCLOAK_URL = "https://incloak.com/proxy-list/"
USPROXYORG_URL = "http://www.us-proxy.org/"
IDCLOAK_URL = "http://www.idcloak.com/proxylist/proxy-list.html"

def get_from_incloak():
    session = requests.session()
    response = session.get(INCLOAK_URL)

    text = "".join([line for line in response.text.encode('utf-8').split('<tr>') if IP_REGEX.match(line)]).split('</table>')[0]
    text = "".join(text)
    text = text.split('<tr')

    return [IP_REGEX.match(x).groups(0)[0] + ':' + x.split('<td>')[1].split('</td>')[0] for x in text]

def get_from_usproxyorg():
    session = requests.session()
    response = session.get(USPROXYORG_URL)

    text = response.text.decode("utf-8")
    index = text.find('<tbody>') + 7
    index2 = text.find('</tbody>')
    text = text[index:index2]
    text = text.split('</tr>')

    result = []

    for line in text:
        elems = line.split('</td>')
        try:
            result.append(elems[0].replace('\n', '').replace('<tr>', '').replace('<td>', '') + ':' + elems[1][4:])
        except:
            break

    return result

def get_from_idcloak():
    session = requests.session()
    response = session.get(IDCLOAK_URL)

    text = unicode(response.text)
    index = text.find('<div class="proxy_table" >') + 7
    text = text[index:]
    text = text.split('</tr>')
    text = text[1:-1]
    text = [x.split('<td') for x in text]

    return [(x[-1] + ':' + x[-2]).replace('</td>', '').replace('>', '') for x in text]
    #return ['<br>'.join(x) for x in text]

def get_proxies():
    proxies = get_from_incloak()
    proxies.extend(get_from_usproxyorg())
    proxies.extend(get_from_idcloak())

    for p in proxies:
        yield p

if __name__ == '__main__':
    for i in get_proxies():
        print i
