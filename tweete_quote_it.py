import requests

from html2image import Html2Image


hti = Html2Image()

# replace with your bearer token from twitter api v2
BEARER_TOKEN = ""


def get_html(text, username): return f"""
<main>
    <div class="card">
        <div class="row">
            <div class="quote">
                {text}
            </div>
        </div>
        <div class="row">
            <div class="border">

            </div>
        </div>
        <div class="row">
            {username}
        </div>
    </div>
</main>
"""


CSS = """
*{
    margin: 0;
    padding: 0;
}
main{
    width: 1920px;
    height: 1080px;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #FFFFFF;
}
        .card{
            font-family: 'Poppins', sans-serif;
            border-radius: 50px;
      background: #e0e0e0;
      box-shadow:  20px 20px 60px #bebebe,
             -20px -20px 60px #ffffff;
      margin: 6.8%;
      padding: 30px;

        }
        .row{
            display: flex;
      justify-content: center;
        }
        .quote{
            font-size: 2rem;
        }
        .quote::before{
        content: '"';
        font-size: 2.5rem;
        }
        .quote::after{
        content: '"';
        font-size: 2.5rem;
        }

        .border {
            margin-top: 2rem;
            margin-bottom: 2rem;
            width: 30%;
            height: 5px;
            background: #494949;
        }
"""


def get_user_by_name(username, bearer_token=BEARER_TOKEN):
    """ Returns the user details with given user name, or a dict with key errors if any errors present
    """
    headers = {"Authorization": f"Bearer {bearer_token}"}

    url = f"https://api.twitter.com/2/users/by/username/{username}"

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def get_tweets_by_user(user_id, max_results=100, bearer_token=BEARER_TOKEN):
    """ Returns the list of tweets by given user having the user id.
    """
    headers = {"Authorization": f"Bearer {bearer_token}"}

    url = f"https://api.twitter.com/2/users/{user_id}/tweets?max_results={max_results}"

    response = requests.request("GET", url, headers=headers)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def generate_quote_image(username, quote, filename):
    hti.screenshot(html_str=get_html(quote, username),
                   css_str=CSS, save_as=filename)


def main():
    try:
        while True:
            print('''
             #######                             #####                             ###       
                #    #    # ###### ###### ##### #     # #    #  ####  ##### ######  #  ##### 
                #    #    # #      #        #   #     # #    # #    #   #   #       #    #   
                #    #    # #####  #####    #   #     # #    # #    #   #   #####   #    #   
                #    # ## # #      #        #   #   # # #    # #    #   #   #       #    #   
                #    ##  ## #      #        #   #    #  #    # #    #   #   #       #    #   
                #    #    # ###### ######   #    #### #  ####   ####    #   ###### ###   # 
                
                Save your tweets as quotes!
            ''')
            username = input('Enter username to search(CTL+C to quit):')
            user = get_user_by_name(username)['data']
            tweets = get_tweets_by_user(user_id=user['id'])['data']
            print('Select Tweet By', user['name'])
            for i, tweet in enumerate(tweets, start=1):
                print(f'{i}. {tweet["text"]}')
            index = int(input(f'Select tweet number(1-{len(tweets)}):')) - 1
            tweet = tweets[index]['text']
            filename = input('Enter file name to save:')
            generate_quote_image(user['name'], tweet, filename)
            print(f'Quote saved as {filename}')

    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
