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

    def fill_all(self):
        """
        空の情報を補完する。
        # NOTE: fill_phoneme, syllable, note, phrase を後ろにしたほうがいいかも。
                deepcopyか上書きタイプだった場合に、更新した値が昨日や明日のオブジェクトに反映されない。
        """
        # 音素を補完
        self.fill_phoneme()
        # 音節を補完
        self.fill_syllable()
        # ノートを補完
        self.fill_note()
        # フレーズを補完
        self.fill_phrase()
        return self

    def fill_phoneme(self):
        """
        未登録の音素情報を一括登録
        登録元データ: p1, p4, p9, p12
        登録先データ: p2, p3, p5, p6, p7, p8, p10, p11, p13, p15
        """
        self.fill_phoneme_symbol()  # p2, p3, p5, p6
        self.fill_phoneme_flag()  # p7, p8, p10, p11
        self.fill_phoneme_position_in_syllable()  # p13
        self.fill_phoneme_distance_from_vowel()  # p14, p15
        return self

    def fill_phoneme_symbol(self):
        """
        未登録の音素を一括登録
        登録元: p4 (最初と最後だけ p3, p5)
        登録先: p2, p3, p5, p6
        """
        # 明日のラベルが持つ、「一昨日の音素記号」と「昨日の音素記号」を始まりから順に補完する。
        for i, current_label in enumerate(self[:-1]):
            self[i + 1].phoneme[1] = current_label.phoneme[2]
            self[i + 1].phoneme[2] = current_label.symbol
        # 昨日のラベルが持つ、「明後日の音素記号」と「明日の音素記号」を終わりから順に補完する。
        for i, current_label in enumerate(reversed(self[1:]), 1):
            self[-(i + 1)].phoneme[5] = current_label.phoneme[4]
            self[-(i + 1)].phoneme[4] = current_label.symbol
        return self

    def fill_phoneme_flag(self):
        """
        未登録の音素フラグを一括登録
        登録元:
        """
        # 明日のラベルが持つ、「一昨日の音素フラグ」と「昨日の音素フラグ」を始まりから順に補完する。
        for i, current_label in enumerate(self[:-1]):
            self[i + 1].phoneme[6] = current_label.phoneme[7]
            self[i + 1].phoneme[7] = current_label.phoneme[8]
        # 昨日のラベルが持つ、「明後日の音素記号」と「明日の音素記号」を終わりから順に補完する。
        for i, current_label in enumerate(reversed(self[1:]), 1):
            self[-(i + 1)].phoneme[10] = current_label.phoneme[9]
            self[-(i + 1)].phoneme[9] = current_label.phoneme[8]
        return self

    def fill_phoneme_position_in_syllable(self):
        """
        音節始端からの位置(p14)をもとに、音節終端からの位置(p15)を補完する。
        楽曲終端から掃引する。
        ついでに音節内音素数(b1)をSyllableに登録する。
        登録元: p14
        登録先: p15, b1
        """
        number_of_phonemes = 'xx'
        for current_label in reversed(self):
            # p14
            phoneme_position = current_label.phoneme.position_in_syllable
            # 初期化されていた場合は、音節内音素数を設定しなおす。
            if number_of_phonemes == 'xx':
                number_of_phonemes = phoneme_position
            # set p15
            current_label.phoneme[14] = number_of_phonemes - phoneme_position + 1
            # set b1 音節内音素数をSyllableに登録
            current_label.syllable.number_of_phonemes = number_of_phonemes
            # 処理したのが音節内で最初の音素だった場合は、音節内音素数を初期化する。
            if phoneme_position == 1:
                number_of_phonemes_in_syllable = 'xx'
        return self

    def fill_phoneme_distance_from_vowel(self):
        """
        音節の判定をして、子音が出てきたときに処理をする。
        前からと後ろからで1往復する。
        """
        distance_from_vowel = 0
        # 全ラベル始端から順に、「音素内の、直前の母音から子音までの距離」(p14)を埋める。
        for current_label in self:
            # 音節内の最初の音素は、無条件でスルーする。あとカウントを初期化する。
            if current_label.phoneme.position_in_syllable == 1:
                current_label.phoneme[13] = 'xx'
            # 母音だったら距離を数える基準にする。
            if current_label.phoneme.symbol == 'v':
                distance_from_vowel = 1
                current_label.phoneme[13] = 'xx'
            # 音節内の2番目以降の音素で子音だったときは、距離を登録して、距離を増やす。
            elif current_label.phoneme.symbol == 'c':
                current_label[13] = distance_from_vowel
                distance_from_vowel += 1
            # 母音でも子音でもないときは距離を増やす
            else:
                current_label.phoneme[13] = 'xx'
                distance_from_vowel += 1
        # 全ラベル終端から順に、「音素内の、直前の母音から子音までの距離」(p15)を埋める。
        for current_label in reversed(self):
            # 音節内の最初の音素は、無条件でスルーする。あとカウントを初期化する。
            if current_label.phoneme.position_in_syllable == 1:
                current_label.phoneme[14] = 'xx'
            # 母音だったら距離を数える基準にする。
            if current_label.phoneme.symbol == 'v':
                distance_from_vowel = 1
                current_label.phoneme[14] = 'xx'
            # 音節内の2番目以降の音素で子音だったときは、距離を登録して、距離を増やす。
            elif current_label.phoneme.symbol == 'c':
                current_label[14] = distance_from_vowel
                distance_from_vowel += 1
            # 母音でも子音でもないときは距離を増やす
            else:
                current_label.phoneme[14] = 'xx'
                distance_from_vowel += 1
        return self

    def fill_syllable(self):
        """
        未登録の音節情報を一括登録
        登録元: b1~5
        登録先: a1~5, c1~5
        # DEBUG: ノート区切りの情報がないと、ノート外の音素を拾ってしまう。
        # 進行方向から見て後方のラベルに含まれる音節を監視して、音節の切り替わりを判定する。
        """
        # 現在のラベルが持つ、「昨日の音素」を始まりから順に補完する。
        previous_syllable = self[0].previous_syllable
        for i, current_label in enumerate(self[1:], 1):
            current_syllable = current_label.syllable
            if current_syllable != self[i - 1].syllable:
                previous_syllable = self[i - 1].syllable
            current_label.previous_syllable = previous_syllable
        # 現在のラベルが持つ、「明日の音素」を終わりから順に補完する。
        next_syllable = self[-1].next_syllable
        for i, current_label in enumerate(reversed(self[:-1]), 1):
            current_syllable = current_label.syllable
            if current_syllable != self[-(i - 1)].syllable:
                next_syllable = self[-(i - 1)].syllable
            current_label.next_syllable = next_syllable
        return self

    def fill_syllable_number_of_phonemes(self):
        """
        音節内音素数(b1)をSyllableに登録する。楽曲終端から掃引する。
        登録元: p12
        登録先: b1
        """
        number_of_phonemes = 'xx'
        for current_label in reversed(self):
            # p12
            phoneme_position = current_label.phoneme.position_in_syllable
            # 初期化されていた場合は、音節内音素数を設定しなおす。
            if number_of_phonemes == 'xx':
                number_of_phonemes = phoneme_position
            # 音節内音素数を登録(a1)
            current_label.syllable.number_of_phonemes = number_of_phonemes
            # 処理したのが音節内で最初の音素だった場合は、音節内音素数を初期化する。
            if phoneme_position == 1:
                number_of_phonemes = 'xx'
        return self

    def fill_note(self):
        """
        未登録のノート情報を一括登録
        登録元: e
        登録先: d, f
        eは長いけれど、すべて取得してdとfに渡す。
        # NOTE: 前の音素じゃなくて前のノートの情報なことに注意（Phoneme単位で扱っちゃダメ）
        """
        # 現在のラベルが持つ、「昨日のノート」を始まりから順に補完する。
        previous_note = self[0].previous_note
        for i, current_label in enumerate(self[1:], 1):
            current_note = current_label.note
            if current_note != self[i - 1].note:
                previous_note = self[i - 1].note
            current_label.previous_note = previous_note
        # 現在のラベルが持つ、「明日のノート」を終わりから順に補完する。
        next_note = self[-1].next_note
        for i, current_label in enumerate(reversed(self[:-1]), 1):
            current_note = current_label.note
            if current_note != self[-(i - 1)].note:
                next_note = self[-(i - 1)].note
            current_label.next_note = next_note

    def fill_phrase(self):
        """
        未登録のフレーズ情報を一括登録
        登録元: h
        登録先: g, i
        """
        # 現在のラベルが持つ、「昨日のフレーズ」を始まりから順に補完する。
        previous_phrase = self[0].previous_phrase
        for i, current_label in enumerate(self[1:], 1):
            current_phrase = current_label.phrase
            if current_phrase != self[i - 1].phrase:
                previous_phrase = self[i - 1].phrase
            current_label.previous_phrase = previous_phrase
        # 現在のラベルが持つ、「明日のフレーズ」を終わりから順に補完する。
        next_phrase = self[-1].next_phrase
        for i, current_label in enumerate(reversed(self[:-1]), 1):
            current_phrase = current_label.phrase
            if current_phrase != self[-(i - 1)].phrase:
                next_phrase = self[-(i - 1)].phrase
            current_label.next_phrase = next_phrase


class FullLabel:
    """
    HTSのフルコンテキストラベルの、1行分を扱うクラス。
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
        """直前の音節を取得する。"""
        return self._a

    @previous_syllable.setter
    def previous_syllable(self, syllable_object):
        if not isinstance(syllable_object, Syllable):
            raise TypeError
        self._a = syllable_object

    @property
    def syllable(self):
        """現在の音節"""
        return self._b

    @syllable.setter
    def syllable(self, syllable_object):
        if not isinstance(syllable_object, Syllable):
            raise TypeError
        self._b = syllable_object

    @property
    def next_syllable(self):
        """直後の音節"""
        return self._c

    @next_syllable.setter
    def next_syllable(self, syllable_object):
        if not isinstance(syllable_object, Syllable):
            raise TypeError
        self._c = syllable_object

    @property
    def previous_note(self):
        """直前のノート"""
        return self._d

    @previous_note.setter
    def previous_note(self, note_object):
        if not isinstance(note_object, Note):
            raise TypeError
        self._d = note_object

    @property
    def note(self):
        """現在のノート"""
        return self._e

    @note.setter
    def note(self, note_object):
        if not isinstance(note_object, Note):
            raise TypeError
        self._e = note_object

    @property
    def next_note(self):
        """直前のノート"""
        return self._f

    @next_note.setter
    def next_note(self, note_object):
        if not isinstance(note_object, Note):
            raise TypeError
        self._f = note_object

    @property
    def previous_phrase(self):
        """直前のフレーズ"""
        return self._g

    @previous_phrase.setter
    def previous_phrase(self, phrase_object):
        if not isinstance(phrase_object, Phrase):
            raise TypeError
        self._g = phrase_object

    @property
    def phrase(self):
        """現在のフレーズ"""
        return self._h

    @phrase.setter
    def phrase(self, phrase_object):
        if not isinstance(phrase_object, Phrase):
            raise TypeError
        self._h = phrase_object

    @property
    def next_phrase(self):
        """直後のフレーズ"""
        return self._i

    @next_phrase.setter
    def next_phrase(self, phrase_object):
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
        """現在の音素記号の分類(p1)"""
        return self[0]

    @category.setter
    def category(self, phonetic_category):
        self[0] = phonetic_category

    @property
    def symbol(self):
        """現在の音素記号(p4)"""
        return self[3]

    @symbol.setter
    def symbol(self, phonetic_symbol):
        self[3] = phonetic_symbol

    @property
    def flag(self):
        """現在の音素のフラグ(p8)"""
        return self[8]

    @flag.setter
    def flag(self, flag):
        self[8] = flag

    @property
    def position_in_syllable(self):
        """
        現在の音素が、音節内で
        前から何番目か (p12)

        日本語だったら
        V  のとき : 1
        CV のとき : C:1, V:2
        CVVのとき : C:1, V:2, V;3
        pauなど   : 1
        """
        return int(self[11])

    @position_in_syllable.setter
    def position_in_syllable(self, position_in_syllable):
        self[11] = int(position_in_syllable)

    @property
    def undefined_context(self):
        """
        HTSでは定義されていない、空きのコンテキスト情報(p16)
        """
        return self[15]

    @undefined_context.setter
    def undefined_context(self, user_context):
        self[15] = user_context

    # def is_first_phoneme_in_syllable(self):
    #     """音節内で最初の音素かどうかを判定する。"""
    #     return self.position_in_syllable == 1


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

    @property
    def number_of_phonemes(self):
        """音節内の音素数"""
        return int(self[0])

    @number_of_phonemes.setter
    def number(self, number_of_phonemes_in_syllable):
        self[0] = int(number_of_phonemes_in_syllable)

    @property
    def position_in_note(self):
        """ノート内での位置"""
        return int(self[1])

    @position_in_note.setter
    def position_in_note(self, position_in_note):
        self[1] = int(position_in_note)

    @property
    def language(self):
        """音節の言語"""
        return self[3]

    @language.setter
    def language(self, language):
        self[3] = language

    @property
    def language_dependent_context(self):
        """
        音節の言語依存コンテキスト
        0らしいけどよくわからん。個数か？
        """
        return self[4]

    @language_dependent_context.setter
    def language_dependent_context(self, language_dependent_context):
        self[4] = language_dependent_context


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
    t_start = time()
    main()
    t_stop = time()
    print(t_stop - t_start)
