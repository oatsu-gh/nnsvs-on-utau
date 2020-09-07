#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
Python3 module for HTS-full-label.

This code contains the copy of the document of HTS.
Their license is at the bottom of this code.
"""

import re

# from pysnooper import snoop


def load(path, encoding='utf-8'):
    """
    フルコンテキストラベルファイルを読み取ってクラスオブジェクトにする。
    """
    with open(path, mode='r', encoding=encoding) as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    full_label_list = FullLabelList()
    for line in lines:
        full_label = FullLabel()
        l = line.split(maxsplit=2)
        full_label.start = int(l[0])
        full_label.end = int(l[1])
        list_of_str = re.split('/.:', l[2])
        tpl_of_list = (re.split('[{}]'.format(re.escape('=+-~!@#$%^&;_|[]')), s)
                       for s in list_of_str)
        full_label._p,\
            full_label._a,\
            full_label._b,\
            full_label._c,\
            full_label._d,\
            full_label._e,\
            full_label._f,\
            full_label._g,\
            full_label._h,\
            full_label._i,\
            full_label._j \
            = tpl_of_list
        full_label_list.append(full_label)

    return full_label_list


class FullLabelList(list):
    """
    HTSのフルコンテキストラベル全体を扱うクラス
    """
    def __str__(self):
        l = [str(full_label) for full_label in self]
        return '\n'.join(l)

    def write(self, path_output, mode='w', encoding='utf-8'):
        """
        ファイル出力用
        """
        # ファイル出力
        with open(path_output, mode=mode, encoding=encoding) as f:
            f.write(str(self))

    def fill_all_context(self):
        """
        空の情報を補完する。
        """
        # 音素を補完
        self.fill_phoneme_context()
        # 音節を補完
        self.fill_syllable_context()
        # ノートを補完
        self.fill_note_context()
        # フレーズを補完
        self.fill_phrase_context()

    def fill_phoneme_context(self):
        """
        未登録の音素を一括登録
        登録元: p3, p4, p5
        登録先: p2, p3, p5, p6
        """
        # 明日の音素が持つ、「一昨日の音素」と「昨日の音素」を前から順に補完する。
        for i, current_label in enumerate(self[:-1]):
            self[i + 1].phoneme[1] = current_label.phoneme[2]
            self[i + 1].phoneme[2] = current_label.phoneme[3]
            self[i + 1].phoneme[6] = current_label.phoneme[7]
            self[i + 1].phoneme[7] = current_label.phoneme[8]
        # 昨日の音素が持つ、「明後日の音素」と「明日の音素」を後ろから順に補完する。
        for i, current_label in enumerate(reversed(self[1:]), 1):
            self[-(i + 1)].phoneme[5] = current_label.phoneme[4]
            self[-(i + 1)].phoneme[4] = current_label.phoneme[3]
            self[-(i + 1)].phoneme[10] = current_label.phoneme[9]
            self[-(i + 1)].phoneme[9] = current_label.phoneme[8]
        return self

    def fill_syllable_context(self):
        """
        未登録の音節情報を一括登録
        登録元: b1~5
        登録先: a1~5, c1~5
        # DEBUG: ノート区切りの情報がないと、ノート外の音素を拾ってしまう。
        """
        for i, current_label in enumerate(self[1:-1], 1):
            current_syllable = current_label.syllable
            self[i - 1].next_syllable = current_syllable
            self[i + 1].previous_syllable = current_syllable

    def fill_note_context(self):
        """
        未登録のノート情報を一括登録
        登録元: e
        登録先: d, f
        eは長いけれど、すべて取得してdとfに渡す。
        # NOTE: 前の音素じゃなくて前のノートの情報なことに注意（Phoneme単位で扱っちゃダメ）
        """
        for i, current_label in enumerate(self[1:-1], 1):
            current_note = current_label.note
            self[i - 1].next_note = current_note
            self[i + 1].previous_note = current_note

    def fill_phrase_context(self):
        """
        未登録のフレーズ情報を一括登録
        登録元: h
        登録先: g, i
        """
        for i, current_label in enumerate(self[1:-1], 1):
            current_phrase = current_label.phrase
            self[i - 1].next_phrase = current_phrase
            self[i + 1].previous_phrase = current_phrase


class FullLabel:
    """
    HTSのフルコンテキストラベルの、1行分を扱うクラス。
    P を担当する。
    """

    def __init__(self):
        self.start = 0
        self.end = 0
        self._p = Phoneme()   # 一昨日から明後日までの音素(p1-p16)
        self._a = Syllable()  # 昨日の音節(a1-a5)
        self._b = Syllable()  # 今日の音節(b1-b5)
        self._c = Syllable()  # 明日の音節(c1-c5)
        self._d = Note()  # 昨日のノートのピッチ、音高、拍数、テンポ、長さ(d1-d9)
        self._e = Note()  # 今日のノートのピッチ、音高、拍数、テンポ、長さ、ほか音楽記号(e1-e50)
        self._f = Note()  # 明日のノートのピッチ、音高、拍数、テンポ、長さ(f1-f9)
        self._g = Phrase()  # 昨日のフレーズの音節数と音素数(g1-g2)
        self._h = Phrase()  # 今日のフレーズの音節数と音素数(h1-h2)
        self._i = Phrase()  # 明日のフレーズの音節数と音素数(i1-i2)
        self._j = Song()  # 曲全体の(音節あるいは小節数)、音素数、フレーズ数(j1-j3)

    def __str__(self):
        str_time = f'{self.start} {self.end} '
        str_p =\
            '{0}@{1}ˆ{2}-{3}+{4}={5}_{6}%{7}ˆ{8}_{9}∼{10}-{11}!{12}[{13}${14}]{15}'\
            .format(*self._p)
        str_a = '/A:{0}-{1}-{2}@{3}~{4}'.format(*self._a)
        str_b = '/B:{0}_{1}_{2}@{3}|{4}'.format(*self._b)
        str_c = '/C:{0}+{1}+{2}@{3}&{4}'.format(*self._c)
        str_d = '/D:{0}!{1}#{2}${3}%{4}|{5}&{6};{7}-{8}'.format(*self._d)
        str_e =\
            '/E:{0}]{1}ˆ{2}={3}∼{4}!{5}@{6}#{7}+{8}]{9}${10}|{11}[{12}&{13}]{14}={15}ˆ{16}∼{17}#{18}_{19};{20}${21}&{22}%{23}[{24}|{25}]{26}-{27}ˆ{28}+{29}∼{30}={31}@{32}${33}!{34}%{35}#{36}|{37}|{38}-{39}&{40}&{41}+{42}[{43};{44}]{45};{46}∼{47}∼{48}ˆ{49}ˆ{50}@{51}[{52}#{53}={54}!{55}∼{56}+{57}!{58}ˆ{59}'\
            .format(*self._e)
        str_f = '/F:{0}#{1}#{2}-{3}${4}${5}+{6}%{7};{8}'.format(*self._f)
        str_g = '/G:{0}_{1}'.format(*self._g)
        str_h = '/H:{0}_{1}'.format(*self._h)
        str_i = '/I:{0}_{1}'.format(*self._i)
        str_j = '/J:{0}~{1}@{2}'.format(*self._j)

        str_self = ''.join((str_time, str_p, str_a, str_b, str_c, str_d,
                            str_e, str_f, str_g, str_h, str_i, str_j))
        return str_self

    @property
    def phoneme(self):
        """
        現在の音素を取得する。
        """
        return self._p

    @phoneme.setter
    def phoneme(self, phoneme_object):
        """
        現在の音素を上書きする。
        """
        if not isinstance(phoneme_object, Phoneme):
            raise TypeError
        self._p = phoneme_object

    @property
    def previous_syllable(self):
        """
        直前の音節を取得する。
        """
        return self._a

    @previous_syllable.setter
    def previous_syllable(self, syllable_object):
        """
        現在の音節を上書きする。
        """
        if not isinstance(syllable_object, Syllable):
            raise TypeError
        self._a = syllable_object

    @property
    def syllable(self):
        """
        現在の音節を取得する。
        """
        return self._b

    @syllable.setter
    def syllable(self, syllable_object):
        """
        現在の音節を上書きする。
        """
        if not isinstance(syllable_object, Syllable):
            raise TypeError
        self._b = syllable_object

    @property
    def next_syllable(self):
        """
        直前の音節を取得する。
        """
        return self._c

    @next_syllable.setter
    def next_syllable(self, syllable_object):
        """
        現在の音節を上書きする。
        """
        if not isinstance(syllable_object, Syllable):
            raise TypeError
        self._c = syllable_object

    @property
    def previous_note(self):
        """
        直前のノートを取得する。
        """
        return self._d

    @previous_note.setter
    def previous_note(self, note_object):
        """
        現在のノートを上書きする。
        """
        if not isinstance(note_object, Note):
            raise TypeError
        self._d = note_object

    @property
    def note(self):
        """
        現在のノートを取得する。
        """
        return self._e

    @note.setter
    def note(self, note_object):
        """
        現在のノートを上書きする。
        """
        if not isinstance(note_object, Note):
            raise TypeError
        self._e = note_object

    @property
    def next_note(self):
        """
        直前のノートを取得する。
        """
        return self._f

    @next_note.setter
    def next_note(self, note_object):
        """
        現在のノートを上書きする。
        """
        if not isinstance(note_object, Note):
            raise TypeError
        self._f = note_object

    @property
    def previous_phrase(self):
        """
        直前の音節を取得する。
        """
        return self._g

    @previous_phrase.setter
    def previous_phrase(self, phrase_object):
        """
        現在の音節を上書きする。
        """
        if not isinstance(phrase_object, Phrase):
            raise TypeError
        self._g = phrase_object

    @property
    def phrase(self):
        """
        現在の音節を取得する。
        """
        return self._h

    @phrase.setter
    def phrase(self, phrase_object):
        """
        現在の音節を上書きする。
        """
        if not isinstance(phrase_object, Phrase):
            raise TypeError
        self._h = phrase_object

    @property
    def next_phrase(self):
        """
        直前の音節を取得する。
        """
        return self._i

    @next_phrase.setter
    def next_phrase(self, phrase_object):
        """
        現在の音節を上書きする。
        """
        if not isinstance(phrase_object, Phrase):
            raise TypeError('Functional argument \'phrase_object\' must be Phrase instance.')
        self._i = phrase_object


class Phoneme(list):
    """
    1音素を扱うクラス
    p1~p16
    """

    def __init__(self):
        super().__init__(['xx'] * 16)

    @property
    def category(self):
        """現在の音素記号の分類(p1)を取得する。"""
        return self[0]

    @category.setter
    def category(self, phonetic_category):
        """現在の音素記号の分類(p1)を上書きする。"""
        self[0] = phonetic_category

    @property
    def symbol(self):
        """現在の音素記号(p4)を取得する"""
        return self[3]

    @symbol.setter
    def symbol(self, phonetic_symbol):
        """現在の音素記号を上書きする"""
        self[3] = phonetic_symbol

    @property
    def flag(self):
        """現在の音素のフラグ(p8)を取得する"""
        return self[8]

    @flag.setter
    def flag(self, flag):
        """現在の音素記号(p8)を上書きする"""
        self[8] = flag

    @property
    def position(self):
        """
        現在の音素が、音節内で
        前から何番目か (p12) と 後ろから何番目か (p13) を取得する。
        日本語だったら
        V  のとき : [1, 1]
        CV のとき : [1, 2] [2, 1]
        CVVのとき : [1, 3] [2, 2] [3, 3]
        pauなど   : [1, 1]
        """
        return [self[11], self[12]]

    @position.setter
    def position(self, list_of_position):
        """
        現在の音素が、音節内の
        前から何番目か (p12) と 後ろから何番目か (p13) を上書きする。
        日本語だったら
        V  のとき : [1, 1]
        CV のとき : [1, 2] [2, 1]
        CVVのとき : [1, 3] [2, 2] [3, 3]
        pauなど   : [1, 1]
        """
        self[11], self[12] = list_of_position

    @property
    def distance(self):
        """
        現在の音素が、音節内の
        [直前の母音からの距離 (p14), 直後の子音までの距離 (p15)]
        を取得する。
        """
        return [self[13], self[14]]

    @distance.setter
    def distance(self, list_of_position):
        """
        現在の音素が、音節内の
        [直前の母音からの距離 (p14), 直後の子音までの距離 (p15)]
        を上書きする。
        """
        self[13], self[14] = list_of_position

    @property
    def undefined_context(self):
        """
        HTSでは定義されていない、空きのコンテキスト情報を取得する。(p16)
        """
        return self[15]

    @undefined_context.setter
    def undefined_context(self, user_context):
        """
        HTSでは定義されていない、空きのコンテキスト情報を上書きする。(p16)
        """
        self[15] = user_context


class Syllable(list):
    """
    1音節を扱うクラス
    昨日の音節 A (a1~a5)
    今日の音節 B (b1~b5)
    明日の音節 C (c1~c5)
    基本的にはBのみを操作する。
    """

    def __init__(self):
        super().__init__(['xx'] * 5)


class Note(list):
    """
    1ノート（音符と休符）を扱うクラス
    昨日のノート D (d1~d5)
    今日のノート E (e1~e60)
    明日のノート F (f1~f5)
    基本的にはEのみを操作する。
    """

    def __init__(self):
        super().__init__(['xx'] * 60)


class Phrase(list):
    """
    1フレーズ（基準がわからん）を扱うクラス
    昨日のフレーズ G (g1~g2)
    今日のフレーズ H (h1~h2)
    明日のフレーズ I (i1~i2)
    基本的にはHのみを操作する。
    """

    def __init__(self):
        super().__init__(['xx'] * 2)


class Song(list):
    """
    1曲を扱うクラス
    今日の曲(j1-j3)
    """

    def __init__(self):
        super().__init__(['xx'] * 3)


def main():
    """
    デバッグ用
    """
    # full_label_list = load('yuki.lab')
    full_label_list = FullLabelList()
    symbol_list = ['aa', 'bb', 'cc', 'dd', 'ee']
    for i in range(5):
        full_label = FullLabel()
        full_label.phoneme.symbol = symbol_list[i]
        full_label.phoneme.flag = f'{i}{i}'
        full_label_list.append(full_label)

    full_label_list.fill_all_context()
    full_label_list.write('test.full')


if __name__ == '__main__':
    from time import time
    start = time()
    main()
    print(time() - start)


"""
    /* ----------------------------------------------------------------- */
    /*           The HMM-Based Speech Synthesis System (HTS)             */
    /*           developed by HTS Working Group                          */
    /*           http://hts.sp.nitech.ac.jp/                             */
    /* ----------------------------------------------------------------- */
    /*                                                                   */
    /*  Copyright (c) 2001-2015  Nagoya Institute of Technology          */
    /*                           Department of Computer Science          */
    /*                                                                   */
    /*                2001-2008  Tokyo Institute of Technology           */
    /*                           Interdisciplinary Graduate School of    */
    /*                           Science and Engineering                 */
    /*                                                                   */
    /* All rights reserved.                                              */
    /*                                                                   */
    /* Redistribution and use in source and binary forms, with or        */
    /* without modification, are permitted provided that the following   */
    /* conditions are met:                                               */
    /*                                                                   */
    /* - Redistributions of source code must retain the above copyright  */
    /*   notice, this list of conditions and the following disclaimer.   */
    /* - Redistributions in binary form must reproduce the above         */
    /*   copyright notice, this list of conditions and the following     */
    /*   disclaimer in the documentation and/or other materials provided */
    /*   with the distribution.                                          */
    /* - Neither the name of the HTS working group nor the names of its  */
    /*   contributors may be used to endorse or promote products derived */
    /*   from this software without specific prior written permission.   */
    /*                                                                   */
    /* THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND            */
    /* CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,       */
    /* INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF          */
    /* MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE          */
    /* DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS */
    /* BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,          */
    /* EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED   */
    /* TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,     */
    /* DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON */
    /* ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,   */
    /* OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY    */
    /* OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE           */
    /* POSSIBILITY OF SUCH DAMAGE.                                       */
    /* ----------------------------------------------------------------- */

FORMAT and DEFINITION of parameters
(copy of the HTS document
 'An example of context-dependent label format for HMM-based singing voice synthesis')
--------------------------------------------------------------------------
    p1@p2ˆp3-p4+p5=p6_p7%p8ˆp9_p10∼p11-p12!p13[p14$p15]p16
    /A:a1-a2-a3@a4∼a5
    /B:b1_b2_b3@b4|b5
    /C:c1+c2+c3@c4&c5
    /D:d1!d2#d3$d4%d5|d6&d7;d8-d9
    /E:e1]e2ˆe3=e4∼e5!e6@e7#e8+e9]e10$e11|e12[e13&e14]e15=e16ˆe17∼e18#e19 e20;e21$e22&e23%e24[e25|e26]e27-e28ˆe29+e30∼e31=e32@e33$e34!e35%e36#e37|e38|e39-e40&e41&e42+e43[e44;e45]e46;e47∼e48∼e49ˆe50ˆe51@e52[e53#e54=e55!e56∼e57+e58!e59ˆe60
    /F:f1#f2#f3-f4$f5$f6+f7%f8;f9
    /G:g1_g2
    /H:h1_h2
    /I:i1_i2
    /J:j1∼j2@j3

    p1 the language independent phoneme identity
    p2 the phoneme identity before the previous phoneme
    p3 the previous phoneme identity
    p4 the current phoneme identity
    p5 the next phoneme identity
    p6 the phoneme idendity after the next phoneme
    p7 the phoneme flag before the previous phoneme
    p8 the previous phoneme flag
    p9 the current phoneme flag
    p10 the next phoneme flag
    p11 the phoneme flag after the next phoneme
    p12 position of the current phoneme identity in the syllable (forward)
    p13 position of the current phoneme identity in the syllable (backward)
    p14 the distance from the previous vowel in the current syllable to the current consonant
    p15 the distance from the current consonant to the next vowel in the current syllable
    p16 undefined context
    a1 the number of phonemes in the previous syllable
    a2 position of the previous syllable identity in the note (forward)
    a3 position of the previous syllable identity in the note (backward)
    a4 the language of the previous syllable
    a5 the language dependent context of the previous syllable
    b1 the number of phonemes in the current syllable
    b2 position of the current syllable identity in the note (forward)
    b3 position of the current syllable identity in the note (backward)
    b4 the language of the current syllable
    b5 the language dependent context of the current syllable
    c1 the number of phonemes in the next syllable
    c2 position of the next syllable identity in the note (forward)
    c3 position of the next syllable identity in the note (backward)
    c4 the language of the next syllable
    c5 the language dependent context of the next syllable
    d1 the absolute pitch of the previous note (C0-G9)
    d2 the relative pitch of the previous note (0-11)
    d3 the key of the previous note (the number of sharp)
    d4 the beat of the previous note
    d5 the tempo of the previous note
    d6 the length of the previous note by the syllable
    d7 the length of the previous note by 0.01 second
    d8 the length of the previous note by one-third of the 32nd note
    d9 undefined context
    e1 the absolute pitch of the current note (C0-G9)
    e2 the relative pitch of the current note (0-11)
    e3 the key of the current note (the number of sharp)
    e4 the beat of the current note
    e5 the tempo of the current note
    e6 the length of the current note by the syllable
    e7 the length of the current note by 0.01 second
    e8 the length of the current note by one-third of the 32nd note
    e9 undefined context
    e10 position of the current note identity in the current measure by the note (forward)
    e11 position of the current note identity in the current measure by the note (backword)
    e12 position of the current note identity in the current measure by 0.01 second (forward)
    e13 position of the current note identity in the current measure by 0.01 second (backward)
    e14 position of the current note identity in the current measure by one-third of the 32nd note (forward)
    e15 position of the current note identity in the current measure by one-third of the 32nd note (backward)
    e16 position of the current note identity in the current measure by % (forward)
    e17 position of the current note identity in the current measure by % (backward)
    e18 position of the current note identity in the current phrase by the note (forward)
    e19 position of the current note identity in the current phrase by the note (backward)
    e20 position of the current note identity in the current phrase by 0.01 second (forward)
    e21 position of the current note identity in the current phrase by 0.01 second (backward)
    e22 position of the current note identity in the current phrase by one-third of the 32nd note (forward)
    e23 position of the current note identity in the current phrase by one-third of the 32nd note (backward)
    e24 position of the current note identity in the current phrase by % (forward)
    e25 position of the current note identity in the current phrase by % (backward)
    e26 whether slur or not in between the current note and the previous note
    e27 whether slur or not in between the current note and the next note
    e28 dynamic mark of the current note
    e29 the distance between the current note and the next accent by the note
    e30 the distance between the current note and the previous accent by the note
    e31 the distance between the current note and the next accent by 0.01 second
    e32 the distance between the current note and the previous accent by 0.01 second
    e33 the distance between the current note and the next accent by one-third of the 32nd note
    e34 the distance between the current note and the previous accent by one-third of the 32nd note
    e35 the distance between the current note and the next staccato by the note
    e36 the distance between the current note and the previous staccato by the note
    e37 the distance between the current note and the next staccato by 0.01 second
    e38 the distance between the current note and the previous staccato by 0.01 second
    e39 the distance between the current note and the next staccato by one-third of the 32nd note
    e40 the distance between the current note and the previous staccato by one-third of the 32nd note
    e41 position of the current note in the current crescendo by the note (forward)
    e42 position of the current note in the current crescendo by the note (backward)
    e43 position of the current note in the current crescendo by 1.0 second (forward)
    e44 position of the current note in the current crescendo by 1.0 second (backward)
    e45 position of the current note in the current crescendo by one-third of the 32nd note (forward)
    e46 position of the current note in the current crescendo by one-third of the 32nd note (backward)
    e47 position of the current note in the current crescendo by % (forward)
    e48 position of the current note in the current crescendo by % (backward)
    e49 position of the current note in the current decrescendo by the note (forward)
    e50 position of the current note in the current decrescendo by the note (backward)
    e51 position of the current note in the current decrescendo by 1.0 second (forward)
    e52 position of the current note in the current decrescendo by 1.0 second (backward)
    e53 position of the current note in the current decrescendo by one-third of the 32nd note (forward)
    e54 position of the current note in the current decrescendo by one-third of the 32nd note (backward)
    e55 position of the current note in the current decrescendo by % (forward)
    e56 position of the current note in the current decrescendo by % (backward)
    e57 pitch difference between the current and previous notes
    e58 pitch difference between the current and next notes
    f1 the absolute pitch of the next note (C0-G9)
    f2 the relative pitch of the next note (0-11)
    f3 the key of the next note (the number of sharp)
    f4 the beat of the next note
    f5 the tempo of the next note
    f6 the length of the next note by the syllable
    f7 the length of the next note by 0.01 second
    f8 the length of the next note by one-third of the 32nd note
    f9 undefined context
    g1 the number of syllables in the previous phrase
    g2 the number of phonemes in the previous phrase
    h1 the number of syllables in the current phrase
    h2 the number of phonemes in the current phrase
    i1 the number of syllables in the next phrase
    i2 the number of phonemes in the next phrase
    j1 the number of syllables in this song / the number of measures in this song
    j2 the number of phonemes in this song / the number of measures in this song
    j3 the number of phrases in this song
--------------------------------------------------------------------------
"""
