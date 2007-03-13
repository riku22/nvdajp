#appModules/_default.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2007 Michael Curran <mick@kulgan.net>
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import gc
import comtypesClient
import datetime
from keyUtils import key
import IAccessibleHandler
import api
import debug
import audio
import sayAllHandler
import virtualBuffers
import NVDAObjects
import globalVars
import synthDriverHandler
import gui
import core
import config
import winUser
import appModuleHandler

class appModule(appModuleHandler.appModule):

	def event_switchStart(self,obj,nextHandler):
		audio.cancel()

	def event_switchEnd(self,obj,nextHandler):
		audio.cancel()

	def script_keyboardHelp(self,keyPress,nextScript):
		"""Turns keyboard help on and off. When on, pressing a key on the keyboard will tell you what script is associated with it, if any."""
		if not globalVars.keyboardHelp:
 			state=_("on")
			globalVars.keyboardHelp=True
		else:
			state=_("off")
			globalVars.keyboardHelp=False
		audio.speakMessage(_("keyboard help %s")%state)

	def script_dateTime(self,keyPress,nextScript):
		"""Reports the current date and time"""
		text=datetime.datetime.today().strftime("%I:%M %p on %A %B %d, %Y")
		if text[0]=='0':
			text=text[1:]
		audio.speakMessage(text)

	def script_increaseRate(self,keyPress,nextScript):
		"""Increases the speech rate by 5 percent"""
		synthDriverHandler.setRate(synthDriverHandler.getRate()+5)
		audio.speakMessage(_("rate %d%%")%synthDriverHandler.getRate())

	def script_decreaseRate(self,keyPress,nextScript):
		"""Decreases the speech rate by 5 percent"""
		synthDriverHandler.setRate(synthDriverHandler.getRate()-5)
		audio.speakMessage(_("rate %d%%")%synthDriverHandler.getRate())

	def script_toggleSpeakTypedCharacters(self,keyPress,nextScript):
		"""Toggles on and off the speaking of typed characters"""
		if config.conf["keyboard"]["speakTypedCharacters"]:
			onOff=_("off")
			config.conf["keyboard"]["speakTypedCharacters"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakTypedCharacters"]=True
		audio.speakMessage(_("speak typed characters")+" "+onOff)

	def script_toggleSpeakTypedWords(self,keyPress,nextScript):
		"""Toggles on and off the speaking of typed words"""
		if config.conf["keyboard"]["speakTypedWords"]:
			onOff=_("off")
			config.conf["keyboard"]["speakTypedWords"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakTypedWords"]=True
		audio.speakMessage(_("speak typed words")+" "+onOff)

	def script_toggleSpeakCommandKeys(self,keyPress,nextScript):
		"""Toggles on and off the speaking of other keys that are not specifically characters. This Also includes key combinations that use control and alt and shift."""
		if config.conf["keyboard"]["speakCommandKeys"]:
			onOff=_("off")
			config.conf["keyboard"]["speakCommandKeys"]=False
		else:
			onOff=_("on")
			config.conf["keyboard"]["speakCommandKeys"]=True
		audio.speakMessage(_("speak command keys")+" "+onOff)

	def script_toggleSpeakPunctuation(self,keyPress,nextScript):
		"""Toggles on and off the speaking of punctuation. When on NVDA will say the names of punctuation symbols, when off it will be up to the synthesizer as to how it speaks punctuation"""
		if config.conf["speech"]["speakPunctuation"]:
			onOff=_("off")
			config.conf["speech"]["speakPunctuation"]=False
		else:
			onOff=_("on")
			config.conf["speech"]["speakPunctuation"]=True
		audio.speakMessage(_("speak punctuation")+" "+onOff)

	def script_moveMouseToNavigatorObject(self,keyPress,nextScript):
		"""Moves the mouse pointer to the current navigator object."""
		audio.speakMessage("Move mouse to navigator")
		api.moveMouseToNVDAObject(api.getNavigatorObject())

	def script_moveNavigatorObjectToMouse(self,keyPress,nextScript):
		"""Sets the navigator object to the object that is directly under the mouse pointer"""
		audio.speakMessage("Move navigator object to mouse")
		(x,y)=winUser.getCursorPos()
		obj=NVDAObjects.IAccessible.getNVDAObjectFromPoint(x,y)
		if obj:
			api.setNavigatorObject(obj)
			obj.speakObject()

	def script_navigatorObject_current(self,keyPress,nextScript):
		"""Reports the current navigator object"""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject.speakObject()
		return False

	def script_navigatorObject_currentDimensions(self,keyPress,nextScript):
		"""Reports the hight, width and position of the current navigator object""" 
		obj=api.getNavigatorObject()
		if not obj:
			audio.speakMessage(_("no navigator object"))
		location=obj.location
		if not location:
			audio.speakMessage(_("No location information for navigator object"))
		(left,top,width,height)=location
		audio.speakMessage(_("%d wide by %d high, located %d from left and %d from top")%(width,height,left,top))
   
	def script_navigatorObject_toFocus(self,keyPress,nextScript):
		"""Sets the navigator object to the current focus"""
		obj=api.getFocusObject()
		if not isinstance(obj,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no focus"))
		api.setNavigatorObject(obj)
		audio.speakMessage(_("move to focus"))
		obj.speakObject()

	def script_navigatorObject_parent(self,keyPress,nextScript):
		"""Sets the navigator object to the parent of the object it is currently on."""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.parent
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No parents"))

	def script_navigatorObject_next(self,keyPress,nextScript):
		"""Sets the navigator object to the next object to the one it is currently on"""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.next
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No next"))

	def script_navigatorObject_previous(self,keyPress,nextScript):
		"""Sets the navigator object to the previous object to the one it is currently on"""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.previous
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No previous"))

	def script_navigatorObject_firstChild(self,keyPress,nextScript):
		"""Sets the navigator object to the first child object to the one it is currently on"""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.firstChild
		if curObject is not None:
			api.setNavigatorObject(curObject)
			curObject.speakObject()
		else:
			audio.speakMessage(_("No children"))

	def script_navigatorObject_doDefaultAction(self,keyPress,nextScript):
		"""Performs the default action on the current navigator object (example: presses it if it is a button)."""
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject.doDefaultAction()

	def script_navigatorObject_where(self,keyPress,nextScript):
		"""Reports where the current navigator object is by reporting each of its ancestors""" 
		curObject=api.getNavigatorObject()
		if not isinstance(curObject,NVDAObjects.baseType.NVDAObject):
			audio.speakMessage(_("no navigator object"))
			return
		curObject=curObject.parent
		while curObject is not None:
			audio.speakMessage("in")
			curObject.speakObject()
			curObject=curObject.parent

	def script_review_top(self,keyPress,nextScript):
		"""Moves the review cursor to the top line of the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_top(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_bottom(self,keyPress,nextScript):
		"""Moves the review cursor to the bottom line of the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_bottom(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_previousLine(self,keyPress,nextScript):
		"""Moves the review cursor to the previous line of the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevLine(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_currentLine(self,keyPress,nextScript):
		"""Reports the line of the current navigator object where the review cursor is situated"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentLine(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_nextLine(self,keyPress,nextScript):
		"""Moves the review cursor to the next line of the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextLine(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_previousWord(self,keyPress,nextScript):
		"""Moves the review cursor to the previous word of the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevWord(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_currentWord(self,keyPress,nextScript):
		"""Speaks the word of the current navigator object where the review cursor is situated"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentWord(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_nextWord(self,keyPress,nextScript):
		"""Moves the review cursor to the next word of the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextWord(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_previousCharacter(self,keyPress,nextScript):
		"""Moves the review cursor to the previous character of the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_prevCharacter(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_currentCharacter(self,keyPress,nextScript):
		"""Reports the character of the current navigator object where the review cursor is situated"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_currentCharacter(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_nextCharacter(self,keyPress,nextScript):
		"""Moves the review cursor to the next character of the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_nextCharacter(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_startOfLine(self,keyPress,nextScript):
		"""Moves the review cursor to the start of the line where it is situated, in the current navigator object""" 
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_startOfLine(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_endOfLine(self,keyPress,nextScript):
		"""Moves the review cursor to the end of the line where it is situated, in the current navigator object""" 
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_endOfLine(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_review_moveToCaret(self,keyPress,nextScript):
		"""Moves the review cursor to the position of the system caret, in the current navigator object"""
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.baseType.NVDAObject):
			obj.script_text_review_moveToCaret(keyPress,None)
		else:
			audio.speakMessage(_("no navigator object"))

	def script_speechMode(self,keyPress,nextScript):
		"""Toggles between the speech modes of off, beep and talk. When set to off NVDA will not speak anything. If beeps then NVDA will simply beep each time it its supposed to speak something. If talk then NVDA wil just speak normally.""" 
		curMode=audio.speechMode
		audio.speechMode=audio.speechMode_talk
		newMode=(curMode+1)%3
		if newMode==audio.speechMode_off:
			name=_("off")
		elif newMode==audio.speechMode_beeps:
			name=_("beeps")
		elif newMode==audio.speechMode_talk:
			name=_("talk")
		audio.speakMessage(_("speech mode %s")%name)
		audio.speechMode=newMode

	def script_toggleVirtualBufferPassThrough(self,keyPress,nextScript):
		"""Toggles virtualBuffer pass-through mode on and off. When on, keys will pass straight through the current virtualBuffer, allowing you to interact with a control with out the virtualBuffer doing something else with the key."""
		api.toggleVirtualBufferPassThrough()

	def script_quit(self,keyPress,nextScript):
		"""Quits NVDA!"""
		gui.quit()

	def script_showGui(self,keyPress,nextScript):
		"""Shows the NVDA interface window"""
		gui.showGui()

	def script_sayAll_review(self,keyPress,nextScript):
		o=api.getNavigatorObject()
		sayAllHandler.sayAll(o.text_reviewOffset,o.text_characterCount,o.text_getNextFieldOffsets,o.text_getText,o.text_reportNewPresentation,o._set_text_reviewOffset)

	def script_sayAll_caret(self,keyPress,nextScript):
		o=api.getFocusObject()
		v=virtualBuffers.getVirtualBuffer(o)
		if v and not api.isVirtualBufferPassThrough():
			sayAllHandler.sayAll(v.text_reviewOffset,v.text_characterCount,v.text_getNextLineOffsets,v.text_getText,v.text_reportNewPresentation,v._set_text_reviewOffset)
		else:
			sayAllHandler.sayAll(o.text_caretOffset,o.text_characterCount,o.text_getNextFieldOffsets,o.text_getText,o.text_reportNewPresentation,o._set_text_caretOffset)

	def script_review_reportPresentation(self,keyPress,nextScript):
		o=api.getFocusObject()
		v=virtualBuffers.getVirtualBuffer(o)
		if v and not api.isVirtualBufferPassThrough():
			o=v
		o.text_reportPresentation(o.text_reviewOffset)

	def script_reportCurrentFocus(self,keyPress,nextScript):
		focusObject=api.getFocusObject()
		if isinstance(focusObject,NVDAObjects.baseType.NVDAObject):
			focusObject.speakObject()
		else:
			audio.speakMessage(_("no focus"))

	def script_reportStatusLine(self,keyPress,nextScript):
		foregroundObject=api.getForegroundObject()
		if not foregroundObject:
			audio.speakMessage(_("no foreground object"))
			return
		statusBarObject=foregroundObject.statusBar
		if not statusBarObject:
			audio.speakMessage(_("no status bar found"))
			return
		statusBarObject.speakObject()
		api.setNavigatorObject(statusBarObject)

	def script_toggleReportObjectUnderMouse(self,keyPress,nextScript):
		config.conf["mouse"]["reportObjectUnderMouse"]=not config.conf["mouse"]["reportObjectUnderMouse"]
		if config.conf["mouse"]["reportObjectUnderMouse"]:
			audio.speakMessage(_("speak object under mouse"))
		else:
			audio.speakMessage(_("don't speak object under mouse"))

	def script_title(self,keyPress,nextScript):
		"""Reports the title of the current application or foreground window"""
		obj=api.getForegroundObject()
		if obj:
			obj.speakObject()

	def script_speakForeground(self,keyPress,nextScript):
		obj=api.getForegroundObject()
		if obj:
			obj.speakObject()
			obj.speakDescendantObjects()

	def script_test_navigatorWindowInfo(self,keyPress,nextScript):
		NVDAObjectCount=0
		virtualBufferCount=0
		appModuleCount=0
		accessibleObjectCount=0
		for o in gc.get_objects():
			if isinstance(o,NVDAObjects.baseType.NVDAObject):
				NVDAObjectCount+=1
			elif isinstance(o,virtualBuffers.baseType.virtualBuffer):
				virtualBufferCount+=1
			elif isinstance(o,appModuleHandler.appModule):
				appModuleCount+=1
			elif isinstance(o,IAccessibleHandler.pointer_IAccessible):
				accessibleObjectCount+=1
		audio.speakMessage("NVDAObject count: %s"%NVDAObjectCount)
		audio.speakMessage("virtualBuffer count: %s"%virtualBufferCount)
		audio.speakMessage("appModule count: %s"%appModuleCount)
		audio.speakMessage("accessible object count: %s"%accessibleObjectCount)
		obj=api.getNavigatorObject()
		if isinstance(obj,NVDAObjects.window.NVDAObject_window):
			audio.speakMessage("handle: %s"%obj.windowHandle)
			audio.speakMessage("Owner: %s"%winUser.getAncestor(obj.windowHandle,winUser.GA_ROOTOWNER))
			audio.speakMessage("Control ID: %s"%winUser.getControlID(obj.windowHandle))
			audio.speakMessage("Class: %s"%obj.windowClassName)
			for char in obj.windowClassName:
				audio.speakSymbol("%s"%char)
			audio.speakMessage("internal text: %s"%winUser.getWindowText(obj.windowHandle))
			audio.speakMessage("text: %s"%obj.windowText)

	def script_toggleBeepOnProgressBarUpdates(self,keyPress,nextScript):
		"""Toggles on and off the beeping on progress bar updates"""
		if config.conf["presentation"]["beepOnProgressBarUpdates"]:
			onOff=_("off")
			config.conf["presentation"]["beepOnProgressBarUpdates"]=False
		else:
			onOff=_("on")
			config.conf["presentation"]["beepOnProgressBarUpdates"]=True
		audio.speakMessage(_("Beep on progress bar updates")+" "+onOff)
