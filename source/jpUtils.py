# coding: UTF-8
# jpUtils.py
# NVDA Japanese Team
# A part of NonVisual Desktop Access (NVDA)
# for unittest, see ../jptools/jpDicTest.py

import characterProcessing
import languageHandler
import config
import re
import collections
import unicodedata
from dataclasses import dataclass
from logHandler import log

RE_HIRAGANA = re.compile(u'^[\u3041-\u309e]+$')

def getLongDesc(s):
	try:
		lang = languageHandler.getLanguage()[:2]
		if len(s) == 1 and ord(s) < 128 and lang != 'ja':
			d = characterProcessing.getCharacterDescription(lang, s)
			log.debug(repr([s, d, 0]))
			if d:
				r = '  '.join(d)
				return r
		d = characterProcessing.getCharacterDescription('ja', s)
		log.debug(repr([s, d, 1]))
		if d:
			r = '  '.join(d)
			return r
	except Exception as e:
		log.debug(repr(e))
	log.debug(repr([s, 2]))
	return s

def getShortDesc(s):
	lang = languageHandler.getLanguage()[:2]
	if len(s) == 1 and ord(s) < 128 and lang != 'ja':
		return characterProcessing.processSpeechSymbol(lang, s)
	s2 = characterProcessing.processSpeechSymbol('ja', s)
	if s != s2:
		return s2
	return characterProcessing.getCharacterReading('ja', s.lower())

# characters which use dictionary for spelling reading
SMALL_ZEN_KATAKANA = u'ァィゥェォッャュョヮヵヶ'
SMALL_KANA_CHARACTERS = SMALL_ZEN_KATAKANA + u'ぁぃぅぇぉっゃゅょゎｧｨｩｪｫｬｭｮｯ'
SPECIAL_KANA_CHARACTERS = SMALL_KANA_CHARACTERS + u'をヲｦはへー'
FIX_NEW_TEXT_CHARS = SMALL_ZEN_KATAKANA + u'ー'

def isJa(locale=None):
	if locale is None:
		return languageHandler.getLanguage()[:2] == 'ja'
	return locale[:2] == 'ja'

def isZenkakuHiragana(c):
	return re.search('[ぁ-ゞ]', c) is not None

def isZenkakuKatakana(c):
	if c == u'ー':
		return False
	return re.search('[ァ-ヾ]', c) is not None

def isHankakuKatakana(c):
	return re.search('[ｦ-ﾝ｢｣､｡ｰ]', c) is not None

def isHalfShape(c):
	return len(c) == 1 and (32 < ord(c)) and (ord(c) < 128)

def isFullShapeAlphabet(c):
	return re.search('[ａ-ｚＡ-Ｚ]', c) is not None

def isHalfShapeAlphabet(c):
	return re.search('[a-zA-Z]', c) is not None

def isFullShapeNumber(c):
	return re.search('[０-９]', c) is not None

def isHalfShapeNumber(c):
	return re.search('[0-9]', c) is not None

def isKanaCharacter(c):
	return isZenkakuHiragana(c) or isZenkakuKatakana(c) or isHankakuKatakana(c)

def isLatinCharacter(c):
	return isFullShapeAlphabet(c) or isHalfShapeAlphabet(c)

def isFullShapeSymbol(c):
	return c in u'　、。，．・：；？！´｀¨＾￣＿ー―／＼～∥｜‘’“”（）〔〕［］「」｛｝〈〉＋－＝＜＞￥＄％＃＆＊＠＇＂゙゚゛゜'

def isUpper(c):
	return (len(c) == 1) and (re.search('[A-ZＡ-Ｚ]', c) is not None)

def replaceSpecialKanaCharacter(c):
	if c in SPECIAL_KANA_CHARACTERS:
		c = getShortDesc(c)
	return c

CharAttr = collections.namedtuple('CharAttr', 'upper hira kata half full latin')

def getAttrDesc(a):
	d = []
	if a.hira:
		# Translators: character attribute name
		d.append(_('hiragana'))
	if a.kata:
		# Translators: character attribute name
		d.append(_('katakana'))
	if a.half:
		# Translators: character attribute name
		d.append(_('half shape'))
	if a.full:
		# Translators: character attribute name
		d.append(_('full shape'))
	if a.latin:
		# Translators: character attribute name
		d.append(_('latin'))
	if a.upper:
		# Translators: cap will be spoken before the given letter when it is capitalized.
		capMsg = _("cap %s")
		(capMsgBefore, capMsgAfter) = capMsg.split('%s')
		d.append(capMsgBefore)
	return ' '.join(d)


@dataclass
class JpAttr:
	jpZenkakuHiragana: bool
	jpZenkakuKatakana: bool
	jpHankakuKatakana: bool
	jpLatinCharacter: bool
	nonJpLatinCharacter: bool
	jpFullShapeAlphabet: bool
	nonJpFullShapeAlphabet: bool
	jpFullShapeSymbol: bool
	jpFullShape: bool
	halfShape: bool
	usePhoneticReadingLatin: bool
	usePhoneticReadingKana: bool


def getJpAttr(locale, char, useDetails):
	"""
	"""
	_isJa = isJa(locale)
	jpZenkakuHiragana = _isJa and isZenkakuHiragana(char)
	jpZenkakuKatakana = _isJa and isZenkakuKatakana(char)
	jpHankakuKatakana = _isJa and isHankakuKatakana(char)
	jpLatinCharacter = _isJa and isLatinCharacter(char)
	nonJpLatinCharacter = (not _isJa) and isLatinCharacter(char)
	jpFullShapeAlphabet = _isJa and isFullShapeAlphabet(char)
	nonJpFullShapeAlphabet = (not _isJa) and isFullShapeAlphabet(char)
	jpFullShapeSymbol = _isJa and isFullShapeSymbol(char)
	jpFullShape = jpFullShapeAlphabet or jpFullShapeSymbol
	halfShape = _isJa and isHalfShape(char)
	usePhoneticReadingLatin = useDetails and config.conf["language"]["jpPhoneticReadingLatin"]
	usePhoneticReadingKana = useDetails and config.conf["language"]["jpPhoneticReadingKana"]
	jpAttr = JpAttr(
		jpZenkakuHiragana,
		jpZenkakuKatakana,
		jpHankakuKatakana,
		jpLatinCharacter,
		nonJpLatinCharacter,
		jpFullShapeAlphabet,
		nonJpFullShapeAlphabet,
		jpFullShapeSymbol,
		jpFullShape,
		halfShape,
		usePhoneticReadingLatin,
		usePhoneticReadingKana,
	)
	return jpAttr


def getCharDesc(locale, char, jpAttr):
	"""
	"""
	if jpAttr.jpLatinCharacter and not jpAttr.usePhoneticReadingLatin:
		charDesc = (getShortDesc(char.lower()),)
	elif jpAttr.nonJpLatinCharacter and not jpAttr.usePhoneticReadingLatin:
		charDesc = (char.lower(),)
	elif jpAttr.nonJpFullShapeAlphabet and not jpAttr.usePhoneticReadingLatin:
		charDesc = (unicodedata.normalize('NFKC', char.lower()),)
	elif jpAttr.nonJpFullShapeAlphabet and jpAttr.usePhoneticReadingLatin:
		charDesc = characterProcessing.getCharacterDescription(locale, unicodedata.normalize('NFKC', char.lower()))
	elif (jpAttr.jpZenkakuHiragana or jpAttr.jpZenkakuKatakana or jpAttr.jpHankakuKatakana) and not jpAttr.usePhoneticReadingKana:
		charDesc = (getShortDesc(char),)
	else:
		charDesc = characterProcessing.getCharacterDescription(locale,char.lower())
	log.debug(repr([locale, char, ("%0x" % getOrd(char)), charDesc]))
	return charDesc


def getPitchChangeForCharAttr(uppercase, jpAttr, capPitchChange):
	"""
	"""
	if not capPitchChange:
		return 0
	if uppercase:
		return capPitchChange
	elif jpAttr.jpZenkakuKatakana and config.conf['language']['jpKatakanaPitchChange']:
		return config.conf['language']['jpKatakanaPitchChange']
	elif jpAttr.jpHankakuKatakana and config.conf['language']['halfShapePitchChange']:
		return config.conf['language']['halfShapePitchChange']
	elif jpAttr.halfShape and config.conf['language']['halfShapePitchChange']:
		return config.conf['language']['halfShapePitchChange']
	return 0


def getJaCharAttrDetails(char, sayCapForCapitals):
	r = getDiscriminantReading(char, attrOnly=True, capAnnounced=sayCapForCapitals).rstrip()
	log.debug(repr(r))
	return r


def code2kana(code):
	"""
	input 0x123a
　	output 'イチニーサンエー'
	"""
	s = ''
	src = hex(code)[2:]
	src = ("0000" + src)[-5:]
	if src[0] == '0':
		src = src[1:]
	for c in src:
		if c == '2':
			s += u'ニー'
		elif c == '5':
			s += u'ゴー'
		else:
			s += getShortDesc(c)
	return s

def code2hex(code):
	"""
	input 0x123a
　	output 'u+0123a'
	"""
	s = ''
	src = hex(code)[2:]
	src = ("0000" + src)[-5:]
	if src[0] == '0':
		src = src[1:]
	return 'u+' + src

def getCandidateCharDesc(c, a, forBraille=False):
	d = ''
	if forBraille and (isLatinCharacter(c) or isZenkakuHiragana(c) or isZenkakuKatakana(c) or isFullShapeNumber(c) or isHalfShapeNumber(c) or c == u'．'):
		d = c
	elif a.half or isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c):
		d = getShortDesc(c)
		log.debug(u"shortdesc (%s) %s" % (c, d))
	elif a.hira or a.kata:
		d = replaceSpecialKanaCharacter(c)
		log.debug(u"kana (%s) %s" % (c, d))
	else:
		d = getLongDesc(c)
		if d != c:
			log.debug(u"longdesc (%s) %s" % (c, d))
		else:
			d2 = characterProcessing.processSpeechSymbol('ja', c)
			if d != d2:
				log.debug(u"sym (%s) %s" % (c, d2))
				d = d2
			elif (0xd800 <= ord(c[0]) <= 0xdbff) and len(c) == 2:
				uc = (ord(c[0]) - 0xd800) * 0x800 + (ord(c[1]) - 0xdc00)
				d = code2hex(uc)
				log.debug(u"sp (%s) %s" % (c, d))
			else:
				d = code2hex(ord(c[0]))
				log.debug(u"code (%s) %s" % (c, d))
	if len(d) > 1:
		return ' ' + d + ' '
	return d

def useAttrDesc(a):
	if a[0] == u'ー':
		return False
	if a[1].half or a[1].upper or a[1].hira or a[1].kata or a[1].full:
		return True
	return False

def getOrd(s):
	# handle surrogate pairs
	if len(s) == 1:
		return ord(s)
	if len(s) != 2:
		raise Exception
	o0 = ord(s[0])
	o1 = ord(s[1])
	uc = (o0 - 0xd800) * 0x800 + (o1 - 0xdc00)
	return uc

def splitChars(name):
	# handle surrogate pairs
	nameChars = []
	n = len(name)
	p = 0
	while p < n:
		o0 = ord(name[p])
		if (0xd800 <= o0 <= 0xdbff) and (p + 1 < n):
			#o1 = ord(name[p+1])
			# assert 0xdc00 <= o1 <= 0xdfff:
			#uc = (o0 - 0xd800) * 0x800 + (o1 - 0xdc00)
			c = name[p] + name[p+1]
			nameChars.append(c)
			#log.info(u"%d %d %d (%s)" % (n, p, p+1, c))
			p += 2
		else:
			c = name[p]
			nameChars.append(c)
			#log.info(u"%d %d (%s)" % (n, p, c))
			p += 1
	#log.info(repr(nameChars))
	return nameChars

#TODO: merge _get_description() and getDiscriminantReading().
#nvdajp must modify locale/ja/characterDescriptions.dic and jpUtils.py.
def getDiscriminantReading(name, attrOnly=False, sayCapForCapitals=False, forBraille=False):
	if not name: return ''
	nameChars = splitChars(name)
	attrs = []
	for uc in nameChars:
		c = uc[0]
		ca = CharAttr(
			isUpper(c) if (not sayCapForCapitals and not forBraille) else False,
			isZenkakuHiragana(c),
			isZenkakuKatakana(c),
			isHalfShape(c) or isHankakuKatakana(c),
			isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c),
			isLatinCharacter(c) and not forBraille)
		if not attrOnly:
			log.debug(u"(%s) %d %s" % (uc, len(c), getAttrDesc(ca)))
		attrs.append((uc, ca))
	if attrOnly:
		s = ''
		for a in attrs:
			s += getAttrDesc(a[1]) + ' '
		return s
	s = ''
	prevAttr = None
	prevChar = None
	for a in attrs:
		# attribute unchanged
		if prevAttr == a[1]:
			s += getCandidateCharDesc(a[0], a[1], forBraille=forBraille)
			prevAttr = a[1]
		else:
			if s:
				s += u' '
			if useAttrDesc(a):
				s += getAttrDesc(a[1]) + ' '
			s += getCandidateCharDesc(a[0], a[1], forBraille=forBraille)
			prevAttr = a[1]
		prevChar = a[0]
	s = s.replace('  ', ' ')
	r = s.strip(' ')
	log.debug(repr(r))
	return r

def processHexCode(locale, msg):
	if isJa(locale):
		try:
			msg = re.sub(r"u\+([0-9a-f]{4})", lambda x: "u+" + code2kana(int("0x"+x.group(1),16)), str(msg))
		except Exception as e:
			log.debug(e)
			pass
	return msg

def fixNewText(newText, isCandidate=False):
	log.debug(newText)
	if RE_HIRAGANA.match(newText):
		newText = ''.join([chr(ord(c) + 0x60) for c in newText])
		log.debug('convert hiragana to katakana: ' + newText)
	if not isCandidate:
		for c in FIX_NEW_TEXT_CHARS:
			newText = newText.replace(c, ' ' + getShortDesc(c) + ' ')
	return newText


from typing import Optional, Generator
from speech import (
	speak,
	getCurrentLanguage,
	getCharDescListFromText,
	LANGS_WITH_CONJUNCT_CHARS,
)
from speech.priorities import Spri
from speech.types import SequenceItemT
from speech.commands import (
	LangChangeCommand,
	EndUtteranceCommand,
	PitchCommand,
	BeepCommand,
	CharacterModeCommand,
)
import textInfos
from synthDriverHandler import getSynth


def _getSpellingCharAddCapNotification(
		speakCharOrg: str,
		speakCharAs: str,
		sayCapForCapitals: bool,
		capPitchChange: int,
		beepForCapitals: bool,
) -> Generator[SequenceItemT, None, None]:
	"""This function produces a speech sequence containing a character to be spelt as well as commands
	to indicate that this character is uppercase if applicable.
	@param speakCharOrg: The character.
	@param speakCharAs: The character as it will be spoken by the synthesizer.
	@param sayCapForCapitals: indicates if 'cap' should be reported along with the currently spelt character.
	@param capPitchChange: pitch offset to apply while spelling the currently spelt character.
	@param beepForCapitals: indicates if a cap notification beep should be produced while spelling the currently
	spellt character.
	"""
	capMsgBefore = getJaCharAttrDetails(speakCharOrg, sayCapForCapitals)
	capMsgAfter = None
	if capPitchChange:
		yield PitchCommand(offset=capPitchChange)
	if beepForCapitals:
		yield BeepCommand(2000, 50)
	if capMsgBefore:
		yield capMsgBefore
	yield speakCharAs
	if capMsgAfter:
		yield capMsgAfter
	if capPitchChange:
		yield PitchCommand()


def _getSpellingSpeechWithoutCharMode(
		text: str,
		locale: str,
		useCharacterDescriptions: bool,
		useDetails: bool,
		sayCapForCapitals: bool,
		capPitchChange: int,
		beepForCapitals: bool,
) -> Generator[SequenceItemT, None, None]:
	
	defaultLanguage=getCurrentLanguage()
	if not locale or (not config.conf['speech']['autoDialectSwitching'] and locale.split('_')[0]==defaultLanguage.split('_')[0]):
		locale=defaultLanguage

	if not text:
		# Translators: This is spoken when NVDA moves to an empty line.
		yield _("blank")
		return
	if not text.isspace():
		text=text.rstrip()

	textLength=len(text)
	count = 0
	localeHasConjuncts = True if locale.split('_',1)[0] in LANGS_WITH_CONJUNCT_CHARS else False
	charDescList = getCharDescListFromText(text,locale) if localeHasConjuncts else text
	for item in charDescList:
		if localeHasConjuncts:
			# item is a tuple containing character and its description
			speakCharOrg = item[0]
			charDesc = item[1]
		else:
			# item is just a character.
			speakCharOrg = item
			if useCharacterDescriptions:
				charDesc=characterProcessing.getCharacterDescription(locale,speakCharAs.lower())
		uppercase = speakCharOrg.isupper()
		jpAttr = getJpAttr(locale, speakCharOrg, useDetails)
		speakCharAs = speakCharOrg
		pitchChange = getPitchChangeForCharAttr(uppercase, jpAttr, capPitchChange)
		if isJa(locale) and useCharacterDescriptions:
			charDesc = getCharDesc(locale, speakCharOrg, jpAttr)
		if useCharacterDescriptions and charDesc:
			IDEOGRAPHIC_COMMA = u"\u3001"
			speakCharAs=charDesc[0] if textLength>1 else IDEOGRAPHIC_COMMA.join(charDesc)
		else:
			speakCharAs=characterProcessing.processSpeechSymbol(locale,speakCharAs)
		if config.conf['speech']['autoLanguageSwitching']:
			yield LangChangeCommand(locale)
		yield from _getSpellingCharAddCapNotification(
			speakCharOrg,
			speakCharAs,
			uppercase and sayCapForCapitals,
			pitchChange,
			uppercase and beepForCapitals,
		)
		yield EndUtteranceCommand()


def _getSpellingSpeechAddCharMode(
		seq: Generator[SequenceItemT, None, None],
) -> Generator[SequenceItemT, None, None]:
	"""Inserts CharacterMode commands in a speech sequence generator to ensure any single character
	is spelt by the synthesizer.
	@param seq: The speech sequence to be spelt.
	"""
	charMode = False
	for item in seq:
		if isinstance(item, str):
			if len(item) == 1:
				if not charMode:
					yield CharacterModeCommand(True)
					charMode = True
			elif charMode:
				yield CharacterModeCommand(False)
				charMode = False
		yield item


def getSpellingSpeech(
		text: str,
		locale: Optional[str] = None,
		useCharacterDescriptions: bool = False,
		useDetails: bool = False,
) -> Generator[SequenceItemT, None, None]:
	
	synth = getSynth()
	synthConfig = config.conf["speech"][synth.name]
	
	if synth.isSupported("pitch"):
		capPitchChange = synthConfig["capPitchChange"]
	else:
		capPitchChange = 0
	seq = _getSpellingSpeechWithoutCharMode(
		text,
		locale,
		useCharacterDescriptions,
		useDetails,
		sayCapForCapitals=synthConfig["sayCapForCapitals"],
		capPitchChange=capPitchChange,
		beepForCapitals=synthConfig["beepForCapitals"],
	)
	if synthConfig["useSpellingFunctionality"]:
		seq = _getSpellingSpeechAddCharMode(seq)
	yield from seq


def speakSpelling(
		text: str,
		locale: Optional[str] = None,
		useCharacterDescriptions: bool = False,
		useDetails: bool = False,
		priority: Optional[Spri] = None
) -> None:
	seq = list(getSpellingSpeech(
		text,
		locale=locale,
		useCharacterDescriptions=useCharacterDescriptions,
		useDetails=useDetails,
	))
	log.info(repr(seq))
	speak(seq, priority=priority)


def spellTextInfo(
		info: textInfos.TextInfo,
		useCharacterDescriptions: bool = False,
		useDetails: bool = False,
		priority: Optional[Spri] = None
) -> None:
	if not config.conf['speech']['autoLanguageSwitching']:
		speakSpelling(info.text,useCharacterDescriptions=useCharacterDescriptions,useDetails=useDetails,priority=priority)
		return
	curLanguage=None
	for field in info.getTextWithFields({}):
		if isinstance(field,str):
			speakSpelling(field,curLanguage,useCharacterDescriptions=useCharacterDescriptions,useDetails=useDetails,priority=priority)
		elif isinstance(field,textInfos.FieldCommand) and field.command=="formatChange":
			curLanguage=field.field.get('language')
