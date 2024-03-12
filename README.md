# もくじ
1. プログラムの概要
2. 動作環境
3. 操作方法
4. 初期設定
5. 動きの説明
6. 今後の展望

  
# プログラムの概要
youtubeのURLを入力し、指定された動画で話されている内容を話者分離したうえで文字起こしします

  
# 動作環境
1. windows 10
2. python 3.11
3. cuda 11.8

  
# 操作方法  
## 1. venvの起動  
コマンドラインでの操作  
`venv\Scripts\Activate`  
  
## 2. 開発者モードをON  
PCのスタートメニューを選択　　
設定→開発者向け設定→開発者モードをON　　
　　
## 3. GPUの接続テスト  
コマンドラインでの操作  
`python`  
`import torch`  
`torch.cuda.is_avaiulable()`  
Trueが出たらGPUが使えます  
Falseが出たらCPUしか使えない状態なので、原因を突き止めてGPUにつなげるようにしてください  
>主な原因はcudaがインストールされていない、  
>cudaに対応しているtorchをインストールしていない、  
>インストールされたcudaとtorchのバージョンが合わないなどです  
  
## 4. 実行  
コマンドラインでの操作  
`python creator_talk_to_text.py`  
  
## 5. YoutubeのURLと保存したいファイル名を入力  
コマンドラインでの操作  
`input Youtube URL:(文字起こししたいYoutubeのURL)`  
`input File Name:(テキストファイルに保存したいタイトルを「拡張子なしで」)`  
  
## 6. 待つ  
コマンドラインに各ライブラリの動作状況が表示されます  
「Talk To Text Finished!!!」と出るまで待ちましょう  
結構時間がかかります（5-10分くらい）  
  
## 7. 完了  
txtファイルの中身を目視で確認してください  
出力結果では話者が「SPEAKER_○○（数字）」と表示されます  
インタビュイーやインタビュアーが誰かは動画の冒頭などを直接見て確認してください  
  
# 初期設定  
## 1. cudaのインストール（オフィスのPCではダウンロード済み）  
ブラウザからのダウンロード  
cu118を使用  
https://developer.nvidia.com/cuda-11-8-0-download-archive   
windows→x86_64→10の順にクリックしてダウンロード  
インストーラーのexeがダウンロードされるので、起動してインストールしてください  
>参照：https://note.com/hcanadli12345/n/nb8cf59ca2596  
  
## 2. huggingfaceの認証（斎藤のアカウントで認証済み）  
ブラウザでの認証  
huggingfaceにログイン（https://huggingface.co/）  
https://huggingface.co/pyannote/speaker-diarization  
→会社名と会社のURLと使用用途を入力  
→huggingfaceのprofile  
→settings  
→Access Token  
→New token  
→Nameに「pyannote/speaker-diarization」と入力、roleは「read」  
→Generate a token  
https://huggingface.co/pyannote/segmeitation  
→会社名と会社のURLと使用用途を入力 （こっちはtoken発行しなくてよし）  
creator_talk_textの36行目にある「use_auth_token=」以降にspeaker-diarizationで発行したトークンをコピペ  
>githubに上がっているスクリプトでは斎藤のアカウントで認証したトークンが書かれており、そのまま使用できます
  
## 3. ffmpegのダウンロード（オフィスのPCではダウンロード済み）
ブラウザで操作  
https://ffmpeg.org/download.html  
→Windows builds by BtbN  
→ffmpeg-master-latest-win64-gpl.zipをダウンロード  
→ダウンロードしたzipをわかりやすい場所に展開  
  
## 4. ffmpegのPATHを通す（オフィスのPCでは設定済み）
PCのスタートメニューから操作  
設定  
→システム環境変数の設定  
→環境変数  
→ユーザー環境変数  
→Pathをクリックして「編集」  
→「新規」  
→6で展開したフォルダの中にある「bin」を登録して「OK」 
→PCを再起動  
→コマンドプロンプトで`ffmpeg -version`と打ってテスト
成功すればffmpegのバージョンがコマンドプロンプトに表示されます  
  
## 5. venvの作成（オフィスのPCでは作成済み）
コマンドラインでの操作  
`python -m venv venv`  
  
## 6. venvの起動
コマンドラインでの操作  
`venv\Scripts\Activate`
  
## 7. torch関連のインストール（オフィスのPCではインストール済み）  
コマンドラインでの操作  
`pip install torch==2.0.1+cu118 torchaudio==2.0.2+cu118 --index-url https://download.pytorch.org/whl/cu118`  
  
## 8. requirementsのインストール（オフィスのPCではインストール済み）  
コマンドラインでの操作  
`pip install -r requirements.txt`  
  
## 9. cudaのテスト
コマンドラインでの操作  
`venv\Scripts\Activate`  
`python`  
`import torch`  
`torch.cuda.is_available()`  
Trueが出たらGPUが使えます  
Falseが出たらCPUしか使えない状態なので、原因を突き止めてGPUにつなげるようにしてください  
>主な原因はcudaがインストールされていない、  
>cudaに対応しているtorchをインストールしていない、  
>インストールされたcudaとtorchのバージョンが合わないなどです  

  
# 動きの説明
## 1. Youtubeから音声ファイルをダウンロードする  
yt-dlpというライブラリを使って指定されたURLの動画にアクセスし、mp3としてダウンロードしています
GitHub曰く著作権法には抵触していないという解釈らしいです  
  
## 2. mp3をwavに変換する
のちに登場するpyannoteというライブラリがwavしか認識できないので、ffmpegを使ってwavに変換してあげます  
1で初めからwavでダウンロードできるならいらない処理なのですが、yt-dlpのpythonでの操作方法解説があまりにも少なくあんまり出てこなかったのでmp3で落としています  
コマンドラインからならwavで落とせるらしいですが、コマンドラインの操作を最低限にしたいのでこの処理を一応挟んでいます  
  
## 3 pyannoteで話者分離する  
音声を認識して話者が何人いていつだれが話しているのかを識別するライブラリです  
これで音声中の話者を認識して何分何秒に誰が話しているのかを識別します  
cudaにつなげる状態なら自動でcudaにつないでくれます  
  
## 4. whisperで文字起こしする
pyannoteで話者分離した音声を波形データをもとに文字起こしします  
無料のオープンソースだと重いわ句読点を打ってくれないわですが、有料のAPIを使うと軽いしプロンプトで句読点を打つように指定できます  
ただし確認したところAPIの精度よりオープンソースで一番高精度のモデルで文字起こししたほうが精度が高い気がしています（2024/03/08現在）
OpenAIのことだし精度が高い代わりに使用料も高いモデルが今後出てくるかもしれませんね  

  
# 今後の展望
## 1. コマンドライン上で関数を入力できるようにする
現時点だとbat化できないので、コマンドラインでURLを入力できるようにします  
  
## 2. Youtubeから直接wavにしてダウンロードできるようにする  
mp3をffmpegで変換する動作が無駄な気がするので、yt-dlpで直接wavをダウンロードする方法を探します

## 3. オンライン上での稼働
現時点だとcudaを使う都合上オフィスのPCでしか動作できません  
依頼の件数が増えることを見越して、API化やdjango化などをして誰でも操作できるようにしたいです
