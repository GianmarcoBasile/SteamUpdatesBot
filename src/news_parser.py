"""Module providing parsing for the game news"""

from utils import get_game_name_by_id

def parser(news):
    news_to_return = {}
    news_to_return.update({'game' : get_game_name_by_id(news['appid'])})
    news_to_return.update({'title' : news['title']})
    news_to_return.update({'url' : news['url']})
    new_content = filter_contents(crop_content(news['contents']))
    news_to_return.update({'content' : new_content})
    return create_message(news_to_return)

def filter_contents(content):
    string_to_remove = ''
    is_append = False  
    #print(content) 
    for char in content:
        if char == '{':
            is_append = True
        if is_append:
            string_to_remove += (char)
        if char == '.':
            is_append = False
            if string_to_remove+'png ' in content:
                content = content.replace(string_to_remove+'png ', '')
            elif string_to_remove+'jpg ' in content:
                content = content.replace(string_to_remove+'jpg ', '')
            string_to_remove = ''    
    return content

def crop_content(content):
    index = 2048
    if len(content) > 2048:
        while content[index] != ' ':
            index+=1
        content = content[:index] + '...'
    return content

def create_message(news):
    game_name = "Game news for " + news['game'] + '\n'
    news_url = "<a href =\"" + news['url'] + '\">Check full news here</a>' + '\n' 
    news_title = '<b>' + news['title'] + '</b>' + '\n\n'
    news_content = news['content'] + '\n'
    
    return game_name + news_url + news_title + news_content
     