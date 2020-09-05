#! /usr/bin/env python3
# coding: utf-8
# Copyright (c) 2020 oatsu
"""
Python3 module for HTS-full-lab.

This code contains the copy of the document of HTS.
Their license follows:

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

import re
from collections import UserList


def load(path, encode='utf8'):
    """
    フルコンテキストラベルファイルを読み取ってクラスオブジェクトにする。
    """
    with open(path, mode='r', encode=encode) as f:
        lines = [line.rstrip('\n') for line in f.readlines()]

    full_label = FullLabel()
    for line in lines:
        ph = Phoneme()
        l = line.split(maxsplit=2)
        ph.start = int(l[0])
        ph.end = int(l[1])
        ph.p, ph.a, ph.b, ph.c, ph.d, ph.e, ph.f, ph.g, ph.h, ph.i, ph.j = re.split('/.:', l[2])
        full_label.append(ph)
    return full_label


class FullLabel(UserList):
    """
    HTSのフルコンテキストラベルを扱うクラス
    """

    def __init__(self):
        super().__init__()

    def __str__(self):
        return '\n'.join(self.data)


class Phoneme:
    """
    HTSのフルコンテキストラベルの、1行分を扱うクラス
    """

    def __init__(self):
        self.start = 0
        self.end = 0
        self.p = ParamP()  # 音素情報
        self.a = ParamA()  # 昨日のノートの音素情報
        self.b = ParamB()  # 今日のノートの音素情報
        self.c = ParamC()  # 明日のノートの音素情報
        self.d = ParamD()  # 昨日のノートのピッチ、音高、拍数、テンポ、長さ
        self.e = ParamE()  # 今日のノートのピッチ、音高、拍数、テンポ、長さ、ほか音楽記号
        self.f = ParamF()  # 明日のノートのピッチ、音高、拍数、テンポ、長さ
        self.g = ParamG()  # 昨日のフレーズの音節数と音素数
        self.h = ParamH()  # 今日のフレーズの音節数と音素数
        self.i = ParamI()  # 明日のフレーズの音節数と音素数
        self.j = ParamJ()  # 曲全体の(音節あるいは小節数)、音素数、フレーズ数

    def __str__(self):
        tpl = (self.p, self.a, self.b, self.c, self.d,
               self.e, self.f, self.g, self.h, self.i, self.j)
        return ''.join(map(str, tpl))

    @property
    def symbol(self):
        """現在の音素記号を取得する"""
        return self.p[8]

    @symbol.setter
    def symbol(self, phonetic_symbol):
        """現在の音素記号を上書きする"""
        self.p[8] = str(phonetic_symbol)


class ParamP(UserList):
    """
    the phoneme identities
    音素記号を取り扱うクラス。

    FORMAT:
        p1@p2ˆp3-p4+p5=p6 p7%p8ˆp9 p10∼p11-p12!p13[p14$p15]p16
    DEFINITION:
        p1 the language independent phoneme identity （子音・母音・休符などの区別）
        p2 the phoneme identity before the previous phoneme (一昨日の音素記号)
        p3 the previous phoneme identity （昨日の音素記号）
        p4 the current phoneme identity （今日の音素記号）
        p5 the next phoneme identity （明日の音素記号）
        p6 the phoneme idendity after the next phoneme （明後日の音素記号）
        p7 the phoneme flag before the previous phoneme （一昨日の音素フラグ）
        p8 the previous phoneme flag （昨日の音素フラグ）
        p9 the current phoneme flag （今日の音素フラグ）
        p10 the next phoneme flag （明日の音素フラグ）
        p11 the phoneme flag after the next phoneme （明後日の音素フラグ）
        p12 position of the current phoneme identity in the syllable (forward) （土曜日までの音素距離）
        p13 position of the current phoneme identity in the syllable (backward) （日曜日からの音素距離）
        p14 the distance from the previous vowel in the current syllable to the current consonant （直前の母音からの音素距離）
        p15 the distance from the current consonant to the next vowel in the current syllable （次の母音までの音素距離）
        p16 undefined context
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 16
        self.data[8] = '00'

    def __str__(self):
        return\
            '{0}@{1}ˆ{2}-{3}+{4}={5}_{6}%{7}ˆ{8}_{9}∼{10}-{11}!{12}[{13}${14}]{15}'\
            .format(*self)


class ParamA(UserList):
    """
    FORMAT:
        /A:a1-a2-a3@a4∼a5
    DEFINITION:
        a1 the number of phonemes in the previous syllable
        a2 position of the previous syllable identity in the note (forward)
        a3 position of the previous syllable identity in the note (backward)
        a4 the language of the previous syllable
        a5 the language dependent context of the previous syllable
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 5

    def __str__(self):
        return '/A:{0}-{1}-{2}@{3}~{4}'.format(*self)


class ParamB(UserList):
    """
    FORMAT:
        /B:b1_b2_b3@b4|b5
    DEFINITION:
        b1 the number of phonemes in the current syllable
        b2 position of the current syllable identity in the note (forward)
        b3 position of the current syllable identity in the note (backward)
        b4 the language of the current syllable
        b5 the language dependent context of the current syllable
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 5

    def __str__(self):
        return '/B:{0}_{1}_{2}@{3}|{4}'.format(*self)


class ParamC(UserList):
    """
    FORMAT:
        /C:c1+c2+c3@c4&c5
    DEFINITION:
        c1 the number of phonemes in the next syllable
        c2 position of the next syllable identity in the note (forward)
        c3 position of the next syllable identity in the note (backward)
        c4 the language of the next syllable
        c5 the language dependent context of the next syllable
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 5

    def __str__(self):
        return '/B:{0}+{1}+{2}@{3}&{4}'.format(*self)


class ParamD(UserList):
    """
    FORMAT:
        /D:d1!d2#d3$d4%d5|d6&d7;d8-d9
    DEFINITION:
        d1 the absolute pitch of the previous note (C0-G9)
        d2 the relative pitch of the previous note (0-11)
        d3 the key of the previous note (the number of sharp)
        d4 the beat of the previous note
        d5 the tempo of the previous note
        d6 the length of the previous note by the syllable
        d7 the length of the previous note by 0.01 second
        d8 the length of the previous note by one-third of the 32nd note
        d9 undefined context
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 9

    def __str__(self):
        return '/D:{0}!{1}#{2}${3}%{4}|{5}&{6};{7}-{8}'.format(*self)


class ParamE(UserList):
    """
    FORMAT:
        /E:e1]e2ˆe3=e4∼e5!e6@e7#e8+e9]e10$e11|e12[e13&e14]e15=e16ˆe17∼e18#e19 e20;e21$e22&e23%e24[e25|e26]e27-e28ˆe29+e30∼e31=e32@e33$e34!e35%e36#e37|e38|e39-e40&e41&e42+e43[e44;e45]e46;e47∼e48∼e49ˆe50ˆe51@e52[e53#e54=e55!e56∼e57+e58!e59ˆe60
    DEFINITION:
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
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 60

    def __str__(self):
        return\
            'E:{0}]{1}ˆ{2}={3}∼{4}!{5}@{6}#{7}+{8}]{9}$\
            {10}|{11}[{12}&{13}]{14}={15}ˆ{16}∼{17}#{18}_{19};\
            {20}${21}&{22}%{23}[{24}|{25}]{26}-{27}ˆ{28}+{29}∼\
            {30}={31}@{32}${33}!{34}%{35}#{36}|{37}|{38}-{39}&\
            {40}&{41}+{42}[{43};{44}]{45};{46}∼{47}∼{48}ˆ{49}ˆ\
            {50}@{51}[{52}#{53}={54}!{55}∼{56}+{57}!{58}ˆ{59}'\
            .format(*self)


class ParamF(UserList):
    """
    FORMAT:
        /F:f1#f2#f3-f4$f5$f6+f7%f8;f9
    DEFINITION:
        f1 the absolute pitch of the next note (C0-G9)
        f2 the relative pitch of the next note (0-11)
        f3 the key of the next note (the number of sharp)
        f4 the beat of the next note
        f5 the tempo of the next note
        f6 the length of the next note by the syllable
        f7 the length of the next note by 0.01 second
        f8 the length of the next note by one-third of the 32nd note
        f9 undefined context
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 9

    def __str__(self):
        return '/F:{0}#{1}#{2}-{3}${4}${5}+{6}%{7};{8}'.format(*self)


class ParamG(UserList):
    """
    FORMAT:
        /G:g1_g2
    DEFINITION:
        g1 the number of syllables in the previous phrase
        g2 the number of phonemes in the previous phrase
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 2

    def __str__(self):
        return '/G:{0}_{1}'.format(*self)


class ParamH(UserList):
    """
    FORMAT:
        /H:g1_g2
    DEFINITION:
        h1 the number of syllables in the current phrase
        h2 the number of phonemes in the current phrase
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 2

    def __str__(self):
        return '/H:{0}_{1}'.format(*self)


class ParamI(UserList):
    """
    FORMAT:
        /I:i1_i2
    DEFINITION:
        i1 the number of syllables in the next phrase
        i2 the number of phonemes in the next phrase
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 2

    def __str__(self):
        return '/I:{0}_{1}'.format(*self)


class ParamJ(UserList):
    """
    FORMAT:
        /J:j1∼j2@j3
    DEFINITION:
        j1 the number of syllables in this song / the number of measures in this song
        j2 the number of phonemes in this song / the number of measures in this song
        j3 the number of phrases in this song
    """

    def __init__(self):
        super().__init__()
        self.data = ['xx'] * 3

    def __str__(self):
        return '/J:{0}~{1}@{2}'.format(*self)
