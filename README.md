# nnsvs-on-utau

Run nnsvs as UTAU plugin.

**nnsvs-on-utau is now [ENUNU](https://github.com/oatsu-gh/enunu).**

## 計画

- UST → LAB (HTS-full-context-label) をしたい。
- UtauPlugin → LAB もしたい。
- NNSVSを呼び出して音声出力までやりたい。

## 設計

- USTがもつことのできる情報で構成されるhedファイルを使うことを想定。

## Sinsyの仕様との差異

- 休符周辺の仕様が異なります。休符を挟んだ音符同士の音程の比較や音節の取得ができません。具体的には a, c, e56, e57 などがSinsyの仕様と異なります。
- フレーズに関するコンテキストを操作できません。(h, i, j など)
- sil が自動挿入されません。
- pau が自動分割されません。
- 1つのノートに2音節以上入るシーンに対応していません。
  - 「っ」など
- 拍子情報を取得できません。
- スケールを推定できないため、ノートのキーの情報を取得できません。具体的には e2, e3 の値がSinsyと異なります。
  - 専用のモデルを作成する必要がありそうです。
  - e2またはe3にオクターブなしの情報(たとえばノート高さ番号のmod12)を入れる予定です。

## 業務連絡

- hts.py は utaupy に移動しました。
