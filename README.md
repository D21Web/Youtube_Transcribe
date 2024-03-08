# もくじ
1. とっても簡単な操作方法
2. とっても難しい初期設定
3. ざっくりとした動きの説明


# とっても簡単な操作方法
1. venvの起動
venv\Scripts\Activate

2. 開発者モードをON
設定→開発者向け設定→開発者モードをON

3. GPUの接続テスト
python
import torch
torch.cuda.is_avaiulable()
Trueが出たらGPUが使えます
Falseが出たらCPUしか使えない状態なので、原因を突き止めてGPUにつなげるようにするか、恐ろしく時間がかかるのを承知の上でCPUで操作してください

4. 実行
python creator_talk_to_text.py

5. YoutubeのURLと保存したいファイル名を入力
input Youtube URL:(文字起こししたいYoutubeのURL)
input File Name:(テキストファイルに保存したいタイトルを「拡張子なしで」)

6. 待つ
何か色々コマンドラインに出てきますが、「Talk To Text Finisher!!!」と出るまで待ちましょう。結構時間がかかります

7. 完了
txtファイルの中身を確認する


# とっても難しい初期設定
1. cudaのダウンロード（オフィスのPCではダウンロード済み）
今回はcu118を使用
developer.nvidia.com/cuda-11-8-0-download-archive
cuda118をインストール

2. huggingfaceの認証（斎藤のアカウントで認証済み）
huggingfaceにログイン
huggingface.co/pyannote/speaker-diarization→会社名と会社のURLと使用用途を入力→huggingfaceのprofile→settings→Access Token→New token→Nameに「pyannote/speaker-diarization」と入力、roleは「read」→Generate a token
huggingface.co/pyannote/segmeitation→会社名と会社のURLと使用用途を入力（こっちはtoken発行しなくてよし）
creator_talk_textの36行目にある「use_auth_token=」以降にspeaker-diarizationで発行したトークンをコピペ

3. ffmpegのダウンロード（オフィスのPCではダウンロード済み）
ffmpeg.org/download.html→Windows builds by BtbN→ffmpeg-master-latest-win64-gpl.zipをダウンロード→ダウンロードしたzipをわかりやすい場所に展開

4. ffmpegのPATHを通す（オフィスのPCでは設定済み）
設定→システム環境変数の設定→環境変数→ユーザー環境変数→Pathをクリックして「編集」→「新規」→6で展開したフォルダの中にある「bin」を登録して「OK」→PCを再起動→コマンドプロンプトで「ffmpeg -version」と打ってテスト

5. venvの作成（オフィスのPCでは作成済み）
python -m venv venv

6. venvの起動
venv\Scripts\Activate

7. torch関連のインストール（オフィスのPCではインストール済み）
pip install torch==2.0.1+cu118 torchaudio==2.0.2+cu118 --index-url https://download.pytorch.org/whl/cu118

8. requirementsのインストール（オフィスのPCではインストール済み）
pip install -r requirements.txt

9. cudaのテスト
venv\Scripts\Activate→python→import torch→torch.cuda.is_available()→Trueが出たらGPUを使用可能（Falseが出たら原因を調べてください）



# ざっくりとした動きの説明
ただ操作するだけなら読まなくて大丈夫です
1. Youtubeから音声ファイルをダウンロードする
yt-dlpというライブラリを使って指定されたURLの動画にアクセスし、mp3としてダウンロードしています
普通に考えたら著作権的に大丈夫かと思いますが、GitHub曰く著作権法には抵触していないという解釈らしいです
不思議ですね
詳しく知りたい方は調べてみてください

2. mp3をwavに変換する
のちに登場するpyannoteというライブラリがwavしか認識できないお馬鹿さんなので、ffmpegを使ってwavに変換してあげます
1で初めからwavでダウンロードできるならいらない処理なのですが、yt-dlpのpythonでの操作方法解説があまりにも少なくあんまり出てこなかったのでmp3で落としています
コマンドラインからならwavで落とせるらしいですが、親切な斎藤はコマンドラインの操作を最低限にしたのでこの処理を一応挟んでいます

3. pyannoteで話者分離する
音声を認識して話者が何人いていつだれが話しているのかを識別する頭のいいライブラリです（でもwavしか認識できないお馬鹿さんな一面もあります）
これで音声中の話者を認識して何分何秒に誰が話しているのかを識別します
cudaにつなげる状態なら自動でcudaにつないでくれます
本当に頭がいいですね
でもmp3を認識できないお馬鹿さんです

4. whisperで文字起こしする
pyannoteで話者分離した音声を波形データをもとに文字起こしします
無料のオープンソースだと重いわ句読点を打ってくれないわですが、有料のAPIを使うと軽いしプロンプトで句読点を打つように指定できます
ただし確認したところAPIの精度よりオープンソースで一番高精度のモデルで文字起こししたほうが精度が高い気がしています（2024/03/08現在）
OpenAIのことだし精度が高い代わりに使用料も高いモデルが今後出てくるかもしれませんね