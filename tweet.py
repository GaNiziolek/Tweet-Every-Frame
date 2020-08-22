import os

try:
    import traceback
    from configparser import ConfigParser
    import tweepy
    import glob
    import time
    from pathlib import Path

except ModuleNotFoundError:
    os.system("pip install -r requirements.txt")

#dirFiles.sort(key=lambda f: int(re.sub('\D', '', f)))

class tweet_bot():
    def __init__(self):
        self.api            = self.create_api()
        self.prev_post_time = 0

        while True:

            if self.check_time():
                
                self.prev_post_time = time.time()
                img_path = self.grab_next_img()
                if not img_path:
                    break
                
                params = Path(img_path)
                
                params = params.stem.split(';')

                text = f"{params[0]} \nEpisódio {params[1]} \nSegundo {params[2]}/{params[3]}"

                self.make_tweet_with_img(img_path, text)
                
                self.move_img(img_path)

            else:
                time.sleep(60)

    def create_api(self):

        keys = ConfigParser()

        keys.read('config.ini')
        

        API_KEY       = keys.get('API',   'API_KEY')
        API_SECRET    = keys.get('API',   'API_SECRET')
        ACCESS_KEY    = keys.get('ACESS', 'ACCESS_KEY')
        ACCESS_SECRET = keys.get('ACESS', 'ACCESS_SECRET')
        
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET)

        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

        api = tweepy.API(auth)

        try:
            api.verify_credentials()
        except Exception as e:
            print('Error creating API')
            print(traceback.format_exc())
            raise e
        print('API created')

        return api

    def grab_next_img(self):
        try:
            files = glob.glob('Frames\*.jpg')
            files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
            return files[0]
        except:
            return False

    def make_tweet_with_img(self, img_Path, text=''):
        
        print(f'Fazendo post da imagem {img_Path} com o texto "{text}"')
        self.api.update_with_media(img_Path, status=text)

    def check_time(self):

        if time.time() - self.prev_post_time >= 60:
            return True
        else:
            return False

    def move_img(self, img_path):

        new_img_name = img_path.replace('Frames', 'Posted_Frames')

        print(f'O arquivo "{img_path}" será movido para "{new_img_name}"')
        
        os.rename(img_path, new_img_name)

if __name__ == "__main__":
    bot = tweet_bot()