import urllib.request


urls = ['http://docs.python.org/', 'https://www.google.com/1']

for url in urls:
    try:
        response = urllib.request.urlopen(url)
        if response.getcode() == 200:
            print('Bingo')
        else:
            print('The response code was not 200, but: {}'.format(
                response.get_code()))
    except urllib.error.HTTPError as e:
        print('''An error occurred: {}
    The response code was {}'''.format(e, e.getcode()))

    except ValueError:
        print('''Wrong URL: {}'''.format(url))
