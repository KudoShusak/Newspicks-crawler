import requests
from bs4 import BeautifulSoup
import time
import os
from datetime import datetime
import json

# 取得済みの記事のURLリスト
listfile = 'new_articlelist.txt'

# URLアクセス前の待ち時間
sleeptime = 0.5

prefix = '{:%Y%m%d_%H%M%S}_'.format(datetime.now())

# テキストデータ保存ファイル
text_file = f"{prefix}Newspicks.jsonl"

# 取得したhtmlのリストを保存するファイル
logfile = f"{prefix}Newspicks_html_list.jsonl"

# htmlファイルの名前
sub_filename = "_Newspics_article.html"

# htmlファイルを保存するディレクトリ（フォルダ）
directory = f'{prefix}html'
os.mkdir(directory)

# ログファイル
log = f'{prefix}operation.log'

url_list = []
count = 299052
with open(listfile, mode='r') as f :
    url_list = f.readlines()

for url_n in url_list :
    try :
        url = url_n.replace('\n','')
        count += 1
        print(f'-- {count}:{url} --') # 動作確認用

        time.sleep(sleeptime)
        html = requests.get(url)
        soup = BeautifulSoup(html.content, "html.parser")

        text_list = []
        ### urlに"body"を含む記事のみ
        if '/body/' in url :
            artcount = 0
            ## タイトル ##
            title = soup.find(['h1','h2','h3'], class_='title')
            if title != None :
                ## 無料記事
                text_list.append(title.text)

            ## 本文 ##
            clearfix = soup.find('div', class_='clearfix')
            if clearfix != None :
                article = clearfix.find_all('p')
                if article != [] :
                    ## 無料記事
                    for cont in article :
                        artcount += 1
                        text_list.append(cont.text)
                elif title != None :
                    article = soup.find('div', class_='clearfix')
                    for cont in article.contents :
                        textdata = cont.text.replace(' ','')
                        if textdata != '' and textdata != '\n':
                            artcount += 1
                            text_list.append(textdata)

                else:
                    ## 会員記事の無料部分
                    article = soup.find('div', id='container-v2')
                    if article != None :
                        for cont in article :
                            contsoup = BeautifulSoup(str(cont), "html.parser")
                            if contsoup.find(class_='np-heading-index') != None :
                                artcount += 1
                                text_list.append(contsoup.find(class_='index-header').text.replace(' ',''))
                                for li in contsoup.find_all('li') :
                                    artcount += 1
                                    text_list.append(li.text)
                            else :
                                textdata = cont.text.replace(' ','')
                                if textdata != '' :
                                    artcount += 1
                                    if article.find('div', class_='np-image fill-all'):
                                        # 図解記事
                                        artcount -= 1
                                    text_list.append(textdata)
                    else :
                        article = soup.find('div', class_='container')
                        header = article.find('div', class_='page-header')
                        for cont in header :
                            textdata = cont.text.replace(' ','').replace('　','').replace('\n','')
                            if textdata != '' :
                                text_list.append(textdata)
                        body = article.find('div', class_='clearfix')
                        textdata = body.text.replace(' ','').replace('　','').replace('\n','')
                        artcount += 1
                        text_list.append(textdata)

            else :
                header = soup.find('header')
                if header != None :
                    like_header_box = header.find('div', class_='like-header-box')
                    if like_header_box != None :
                        like_header_box.decompose()
                    for cont in header :
                        textdata = cont.text.replace(' ','').replace('\n', '')
                        if textdata != '' :
                            text_list.append(textdata)
                body = soup.find('main')
                if body != None :
                    for cont in body :
                        contdata =  str(cont).replace(' ','').replace('\n', '')
                        contdata = contdata.replace('<br/>', '\n')
                        contsoup = BeautifulSoup(contdata, 'html.parser')
                        textdata = contsoup.text
                        if textdata != '' :
                            artcount += 1
                            text_list.append(textdata)
            
            if artcount <= 0 :
                text_list.append('###NO_CONTENTS### コンテンツのテキストデータが取得できません')


        elif '/posts/' in url :
            header = soup.find('header')
            text_list.append(header.find('h1').text)

            main = soup.find('main')
            for p in main.find_all(['p', 'blockquote']) :
                textdata = p.text.replace('\n','').replace(' ','')
                if textdata != '' :
                    text_list.append(textdata)

        elif '/news/' in url :
            title = soup.find(['h1','h2','h3'], class_='title')
            text_list.append(title.text)

            comments = soup.find('div', class_='comments')
            commcount = 0
            for comment_block in comments :
                block_soup = BeautifulSoup(str(comment_block), "html.parser")
                comment_container = block_soup.find('div', class_='comment-container')
                if comment_container != None :
                    comment_row = comment_container.find_all('div', class_='comment-row')
                    for row in comment_row :
                        commcount += 1
                        text_list.append(row.find('div', class_='name').text)
                        text_list.append(row.find('div', class_='job').text)
                        comment_soup = BeautifulSoup(str(row.find('div', class_='comment')).replace('<br/>', '\n'), "html.parser")
                        text_list.append(comment_soup.text.replace('\n\n','\n'))
                        text_list.append('')

            if commcount == 0 :
                text_list.append('###NO_CONTENTS### コメントがありません')
        
        ### 取得完了 ###

        ### テキストデータの保存
        print(text_list) # 動作確認用
        save_data = {'url': url, 'text': '\n'.join(text_list)}
        with open(text_file, 'a', encoding='utf-8') as f_text:
            f_text.write(json.dumps(save_data, ensure_ascii=False) + '\n')
        f_text.close()

        ### htmlデータの保存
        filename = str(count).zfill(5) + sub_filename
        filepath = os.path.join(directory,filename)
        with open(filepath, 'w', encoding='utf-8') as f_html:
            f_html.write(str(html.text))
        f_html.close()

        ### 取得したhtmlのリストを保存
        logdata = {'filename': filename, 'url': url}
        with open(logfile, 'a', encoding='utf-8') as f_list:
            f_list.write(json.dumps(logdata)+'\n')
        f_list.close()

        ### ログファイルにアクセス時間を記録
        now = '{:%Y.%m.%d %H:%M:%S}'.format(datetime.now())
        message = {'time': now, 'Access': url}
        with open(log, 'a', encoding='utf-8') as f_log:
            f_log.write(json.dumps(message)+'\n')
        f_log.close()

    except :
        ### エラーの場合もログファイルにアクセス時間を記録
        now = '{:%Y.%m.%d %H:%M:%S}'.format(datetime.now())
        message = {'time': now, 'Error': url}
        with open(log, 'a', encoding='utf-8') as f_log:
            f_log.write(json.dumps(message)+'\n')
        f_log.close()
        