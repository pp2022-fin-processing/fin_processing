from urllib.request import urlretrieve
from urllib.parse import urlencode


def main():
    mydict = {'q': '&%.com/', 'e': 'essa', 'e': 'ues'}
    qstr = urlencode(mydict)
    print(qstr)
    # str resolves to: 'q=whee%21+Stanford%21%21%21&something=else'
    # thing = urlretrieve("https://www.duckduckgo.com/?" + qstr)


if __name__ == '__main__':
    main()