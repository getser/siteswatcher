import json
import urllib.request
import smtplib


def load_from_json(jsonfile):
    """
    jsonfile - string() filename

    Returns:
        dict() or list() data loaded from file.
    """

    try:
        with open(jsonfile) as loaded_file:
            loaded = json.loads(loaded_file.read())
    except IOError:
        print("The data is not loaded! Please, check if file {} is present in working directory.".format(jsonfile))
        raise IOError
    return loaded


def send_email(settings, msg):
    """
    settings: google smtp setings as a dict() with appropriate keys.
    msg: Message to be sent in a letter.
    return: None, just sends mail.
    """


    # !!! If using gmail, we need to unlock Captcha to anable script to send
    # for you: https://accounts.google.com/displayunlockcaptcha !!!

    full_message = 'Subject: URLs problems report\n\n' + msg
    toaddrs = settings["RECIPIENTS_ADDRESS"]
    username = fromaddr = settings["EMAIL_HOST_USER"]
    password = settings["EMAIL_HOST_PASSWORD"]
    server = smtplib.SMTP(':'.join([settings["EMAIL_HOST"], str(settings["EMAIL_PORT"])]))
    server.ehlo()
    server.starttls()
    server.login(username, password)
    server.sendmail(fromaddr, toaddrs, full_message)
    server.quit()


def main():
    urls = load_from_json('sitesurls.json')
    email_settings = load_from_json('mail_settings.json')
    message = ''

    for url in urls:
        try:
            response = urllib.request.urlopen(url)
            if response.getcode() == 200:
                # print(url, 'Bingo')
                pass
            else:
                print('The response code was not 200, but: {}'.format(response.get_code()))
                message += '\nThe site at URL {} is probably broken. The response code was not 200, but: {}.\n'.format(
                    url, response.get_code())

        except urllib.error.HTTPError as e:
            print('The site at URL {} is probably broken. An error occurred: {}. The response code was {}.'.format(
                url, e, e.getcode()))
            message += '\nThe site at URL {} is probably broken. An error occurred: {}. The response code was {}.\n'.format(
                url, e, e.getcode())

        except ValueError:
            print('Wrong URL entered: {}'.format(url))
            message += 'Wrong URL entered: {}'.format(url)

    if message:
        send_email(email_settings, message)

if __name__ == '__main__':
    main()
