#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
USTファイルをHTSフルラベルに変換する。
コンテキストは最低限。
Musicオブジェクトを経由せずにOneLineオブジェクトを直接生成していく。

適用するコンテキストは
[jp_qst_crazy_mono_005.hed](https://github.com/oatsu-gh/nnsvs-custom-stripts/tree/master/hed)
を参考とする。

対象
    CQS:
        p11, p12, p13, p14
        a1, a2, a3,
        b1, b2, b3,
        c1, c2, c3,
        d1, d2, d3, d6, d7, d8,
        e1, e2, e3, e6, e7, e8, e57, e58,
        f1, f2, f3, f6, f7, f8
    QS:
        p1, p3, p4, p5
"""

from os.path import basename, splitext

import utaupy as up
from hts2json import hts2json


def language_independent_phoneme_identity(phoneme):
    """
    音素の分類 (c, v, p, s)
    """
    vowels = ('a', 'i', 'u', 'e', 'o', 'A', 'I', 'U', 'E', 'O')
    if phoneme in vowels:
        return 'v'
    if phoneme == 'pau':
        return 'p'
    if phoneme == 'sil':
        return 's'
    # どれも当てはまらない場合は子音とみなす
    return 'c'


def convert_ustobj_to_htsfulllabelobj(ust: up.ust.Ust, d_table: dict) -> up.hts.HTSFullLabel:
    """
    Ustオブジェクトをノートごとに処理して、HTS用に変換する。
    日本語歌詞を想定するため、音節数は1とする。促音に注意。
    """
    # TODO: 促音が入っている(音節が複数になる)ときの処理を追加
    # e3 に対応する数値で、曲ごとに決まっている。スケール判定の結果っぽい。
    key_of_the_note = 0
    full_label = up.hts.HTSFullLabel()

    t_start = 0
    t_end = 0
    for note in ust.notes:
        t_end = t_start + (note.length_ms * 10000)
        phonemes = d_table[note.lyric]
        for idx, phoneme in enumerate(phonemes):
            ol = up.hts.OneLine()
            # 時刻の処理
            ol.start = int(t_start)
            ol.end = int(t_end)
            # oneline.p: 音素の処理-------------
            temp_p = ol.p
            # 音素分類
            temp_p[0] = language_independent_phoneme_identity(phoneme)
            # 音素記号
            temp_p[3] = phoneme
            # 音素の音節内位置
            temp_p[11] = idx + 1
            temp_p[12] = len(phonemes) - idx
            temp_p[13] = 'xx'
            temp_p[14] = 'xx' if idx == 0 else len(phonemes) - idx - 1
            ol.p = temp_p
            # oneline.b: 音節の処理-------------
            # 音節内音素数
            ol.b[0] = len(phonemes)
            # ノート内音節位置
            ol.b[1] = 1
            ol.b[2] = 1
            # oneline.e: ノートの処理-----------
            if not phoneme in ('pau', 'sil'):
                # 音程C0-G9
                ol.e[0] = up.ust.notenum_as_abc(note.notenum)
                # relative pitch
                ol.e[1] = (note.notenum - key_of_the_note) % 12
                # key
                ol.e[2] = key_of_the_note
            # テンポ
            ol.e[4] = int(note.tempo)
            # ノート内音節数
            ol.e[5] = 1
            # ノート長(0.01s)
            ol.e[6] = note.length_ms // 10
            # ノート長(32分音符の1/3, つまり96分音符いくつぶんか, 4分音符なら8*3=24)
            # utaupy.ust.Note.length は4分音符で480なので、20で割ればよい。
            ol.e[7] = note.length // 20
            full_label.append(ol)
        t_start = t_end
    return full_label


def main():
    path_table = 'dic/kana2romaji_utf-8_for_oto2lab .table'
    d_table = up.table.load(path_table, encoding='sjis')

    path_ust = input('path_ust: ').strip('"')
    path_hts = splitext(basename(path_ust))[0] + '_ust2hts.lab'
    path_json = splitext(basename(path_ust))[0] + '_ust2hts.json'
    ust = up.ust.load(path_ust)

    # Ust → HTSFullLabel
    full_label = convert_ustobj_to_htsfulllabelobj(ust, d_table)
    # HTSFullLabel中の重複データを削除して整理
    full_label.generate_songobj()
    full_label.fill_contexts_from_songobj()
    # 音素数などの整合性をチェック
    full_label.song.check()
    # ファイル出力
    full_label.write(path_hts)
    hts2json(path_hts, path_json)



if __name__ == '__main__':
    main()
    input('press enter')
