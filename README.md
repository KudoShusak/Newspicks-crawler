# Newspicks crawler

Newspicks `https://newspicks.com` から記事を収集します。  
Collect articles from Newspicks `https://newspicks.com` .

## execution

はじめに、`robots.txt` に含まれるサイトマップから、記事のURLを抽出します。  
First, extract the URL of the article from the sitemap contained in the `robots.txt`.
```
% python crawling_sitemap.py
```

抽出されたURLは、カレントディレクトリの `urllist.txt` という名前のファイルに保存されます。  
The extracted URLs are stored in a file named `urllist.txt` in the current directory.

次に、リストアップされたURLから記事を抽出します。  
Next, the articles are extracted from the listed URLs.
```
% python get_data.py
```

抽出された記事のテキストデータは、`xxxxxxxx_xxxxxx_Newspicks.jsonl` というファイルに保存されます。  
The text data of the extracted articles will be saved in a file named `xxxxxxxx_xxxxxx_Newspicks.jsonl`.  
（ `xxxxxxxx_xxxxxx` には、実行した日付と時刻からユニークな文字列が入ります）  
(where `xxxxxxxx_xxxxxx` is a unique string from the date and time of execution)

また、正常に取得できたhtmlは、`xxxxxxxx_xxxxxx_html` というフォルダに保存されます。保存されたファイル名とURLは `xxxxxxxx_xxxxxx_Newspicks_html_list.jsonl` に記録されます。  
The successfully retrieved html will also be saved in a folder named `xxxxxxxx_xxxxxx_html`. The saved file name and URL will be recorded in `xxxxxxxx_xxxxxx_Newspicks_html_list.jsonl`. 

## Saved data format
### xxxxxxxx_xxxxxx_Newspicks.jsonl

１記事につき、１行のJSONフォーマットで保存されます。（JSONLフォーマット）内容は下記の通り。  
One line per article will be saved in JSON format.(JSONL Format) The contents are as follows

Example.
```
{"url": "https://newspicks.com/news/8581413/body/", "text": "米オープンＡＩ、ＡＩソフトのアプリストアを計画＝報道\n[２０日 ロイター] - 対話型人工知能（ＡＩ）「チャットＧＰＴ」の開発元である米オープンＡＩが、自社の技術をベースに構築したＡＩモデルを開発者が販売できるマーケットプレイスの開設を計画していることが分かった。ニュースサイトのジ・インフォメーションが２０日、関係者の話として報じた。\nチャットＧＰＴを利用する法人顧客は、オンライン取引データから金融詐欺を特定したり、内部資料を基に特定の市場に関する質問に答えたりするなど、用途に合わせて変更を加えることが多い。\n報道によると、開発者はオープンＡＩが提案するマーケットプレイスで他社にもこうしたモデルを提供することが可能になる。\nオープンＡＩのサム・アルトマン最高経営責任者（ＣＥＯ）が先月、ロンドンで行った開発者との会合で計画に言及したという。\nこうしたマーケットプレイスは、セールスフォースやマイクロソフトなどオープンＡＩの顧客や技術パートナーが運営するアプリストアと競合し、オープンＡＩの技術がより幅広い顧客層に届くようになる可能性がある。\nオープンＡＩは、ロイターのコメント要請に返答していない。"}
{"url": "https://newspicks.com/news/8581384/body/", "text": "サッカー＝日本がペルーに快勝、三笘や伊東らが得点\n［２０日　ロイター］ - サッカーの日本代表は２０日、大阪・パナソニックスタジアム吹田でペルーと国際親善試合を行い、４─１で快勝した。\n１５日のエルサルバドル戦からメンバー多数を入れ替えて臨んだ日本は前半２２分、伊藤洋輝がペナルティーエリア付近からミドルシュートをたたき込んで先制。さらに同３７分には左サイドでパスを受けた三笘薫がカットインから追加点を奪った。\n日本は後半１８分にもドリブルで運んだ三笘のパスから伊東純也がＧＫをかわして３点目。同３０分には途中出場の前田大然がＤＦラインの背後に飛び出してＧＫとの１対１を制してゴールネットを揺らし、終盤に１失点を喫したものの危なげなく勝利した。\n森保一監督は「収穫は４得点が結果として出ているので、選手たちが目指すべきもの、ゴールというところを積極的にチャレンジしてくれた結果が出たことだと思っています」と手応えを口にした。"}
```

### xxxxxxxx_xxxxxx_Newspicks_html_list.jsonl

`xxxxxxxx_xxxxxx_html` に保存されているhtmlのファイル名と、収集元のURLがJSONL形式で保存されます。  
The html file name stored in `xxxxxxxx_xxxxxx_html` and the URL of the collection source will be saved in JSONL format.

Example.
```
{"filename": "00001_Newspics_article.html", "url": "https://newspicks.com/news/8581413/body/"}
{"filename": "00002_Newspics_article.html", "url": "https://newspicks.com/news/8581384/body/"}
```

### xxxxxxxx_xxxxxx_html

収集したhtmlはこのフォルダに保存されます。  
The collected html is stored in this folder.

### xxxxxxxx_xxxxxx_operation.log

クロールした時刻とURLがJSONL形式で記録されます。URLは、正常にアクセスできた場合は `Access` 、エラーの場合は `Error` というフィールドに記録されます。  
The time and URL of the crawl are recorded in JSONL format. The URL is recorded in the field `Access` in case of successful access and in the field `Error` in case of error.

Example.
```
{"time": "2023.06.26 18:07:31", "Access": "https://newspicks.com/news/8581100/body/"}
{"time": "2023.06.26 18:07:50", "Error": "https://newspicks.com/news/8574466/body/"}
```