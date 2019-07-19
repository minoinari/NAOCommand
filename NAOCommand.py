#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

"""
 @file NAOCommand.py
 @brief Enter commands
 @date $Date$


"""
import sys
import time
import numpy as np
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

import NAO_idl

# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
import ssr, ssr__POA
import ssr, ssr__POA
import ssr, ssr__POA
import ssr, ssr__POA
import ssr, ssr__POA
import ssr, ssr__POA


# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
naocommand_spec = ["implementation_id", "NAOCommand", 
		 "type_name",         "NAOCommand", 
		 "description",       "Enter commands", 
		 "version",           "1.0.0", 
		 "vendor",            "M.Toyoda", 
		 "category",          "Category", 
		 "activity_type",     "STATIC", 
		 "max_instance",      "1", 
		 "language",          "Python", 
		 "lang_type",         "SCRIPT",
		 ""]
# </rtc-template>

##
# @class NAOCommand
# @brief Enter commands
# 
# 
class NAOCommand(OpenRTM_aist.DataFlowComponentBase):
	
	##
	# @brief constructor
	# @param manager Maneger Object
	# 
	def __init__(self, manager):
		OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        	"""
        	"""
        	self._NAO_motionSrvPort = OpenRTM_aist.CorbaPort("NAO_motion")

                self._NAO_speechSrvPort = OpenRTM_aist.CorbaPort("NAO_speech")

        	
		"""
		"""
 		self._motion = OpenRTM_aist.CorbaConsumer(interfaceType=ssr.ALMotion)
		"""
		"""
	        self._textToSpeech = OpenRTM_aist.CorbaConsumer(interfaceType=ssr.ALTextToSpeech)
		"""
		"""
		#self._behaviorManager = OpenRTM_aist.CorbaConsumer(interfaceType=ssr.ALBehaviorManager)
		"""
		"""
		self._videoDevice = OpenRTM_aist.CorbaConsumer(interfaceType=ssr.ALVideoDevice)
		"""
		"""
		self._memory = OpenRTM_aist.CorbaConsumer(interfaceType=ssr.ALMemory)
		"""
		"""
		self._leds = OpenRTM_aist.CorbaConsumer(interfaceType=ssr.ALLeds)

		# initialize of configuration-data.
		# <rtc-template block="init_conf_param">
		
		# </rtc-template>



		 
	##
	#
	# The initialize action (on CREATED->ALIVE transition)
	# formaer rtc_init_entry() 
	# 
	# @return RTC::ReturnCode_t
	# 
	#
	def onInitialize(self):
		# Bind variables and configuration variable
		
		# Set InPort buffers
		
		# Set OutPort buffers
		
		# Set service provider to Ports
		
		# Set service consumers to Ports
		
		self._NAO_motionSrvPort.registerConsumer("ALMotion", "ssr::ALMotion", self._motion)
		self._NAO_speechSrvPort.registerConsumer("ALTextToSpeech", "ssr::ALTextToSpeech", self._textToSpeech)

		# Set CORBA Service Ports
		self.addPort(self._NAO_motionSrvPort)
		self.addPort(self._NAO_speechSrvPort)


		return RTC.RTC_OK
	
	###
	## 
	## The finalize action (on ALIVE->END transition)
	## formaer rtc_exiting_entry()
	## 
	## @return RTC::ReturnCode_t
	#
	## 
	#def onFinalize(self):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The startup action when ExecutionContext startup
	## former rtc_starting_entry()
	## 
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onStartup(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The shutdown action when ExecutionContext stop
	## former rtc_stopping_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onShutdown(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The activated action (Active state entry action)
	## former rtc_active_entry()
	##
	## @param ec_id target ExecutionContext Id
	## 
	## @return RTC::ReturnCode_t
	##
	##
	#def onActivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The deactivated action (Active state exit action)
	## former rtc_active_exit()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onDeactivated(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	##
	#
	# The execution action that is invoked periodically
	# former rtc_active_do()
	#
	# @param ec_id target ExecutionContext Id
	#
	# @return RTC::ReturnCode_t
	#
	#

	def show_help(self):
		print """
help : Show This Help
say : [Usage] "say Hello world", then say "Hello world"
moveTo : Move to the specific position (initial position is (0,0,0)), [Usage] "moveTo x y vtheta"
moveToward : Move Specific speed (vx, vy, vtheta), [Usage] "moveToward vx, vy, vtheta"
stop : Stop moving
behave : Call Behavior which is saved with Choregraph a priori
shakeHead : Shake its head
openHand : Open its right hand
closeHand : Close its right hand
"""

	def onExecute(self, ec_id):
		try:
			c = raw_input("# Input Command: (help for help)")
			cmds = c.split()

			if cmds[0] == "help":
				self.show_help()
			elif cmds[0] == "say":
				text = ""
				for c in cmds[1:]:
					text = text + " " + c
				self._textToSpeech._ptr().say(text)
			#elif cmds[0] == "behave":
			#	self._behaviorManager._ptr().runBehavior(cmds[1])
			elif cmds[0] == "stop":
				self._motion._ptr().stopMove()
			elif cmds[0] == "moveToward":
				if len(cmds) == (1+3):
					vx = float(cmds[1])
					vy = float(cmds[2])
					vz = float(cmds[3])
					self._motion._ptr().moveToward(vx, vy, vz)
			elif cmds[0] == "moveTo":
				if len(cmds) == (1+3):
					x = float(cmds[1])
					y = float(cmds[2])
					z = float(cmds[3])
					self._motion._ptr().moveTo(x, y, z)
			elif cmds[0] == "shakeHead":
				self._motion._ptr().setAngles(ssr.StringArray(["HeadYaw", "HeadPitch"]), ssr.FloatArray([0.2, -0.2]), 0.8)
				time.sleep(1.0)
				self._motion._ptr().setAngles(ssr.StringArray(["HeadYaw"]), ssr.FloatArray([-0.2]), 0.8)
				#self._motion._ptr().setAngles(ssr.StringArray(["RElbowYaw"]), ssr.FloatArray([-0.2]), 0.8)
			elif cmds[0] == "openHand":
				self._motion._ptr().openHand("RHand")
			elif cmds[0] == "closeHand":
				self._motion._ptr().closeHand("RHand")

		except Exception, e:
			print e

		return RTC.RTC_OK
	
	###
	##
	## The aborting action when main logic error occurred.
	## former rtc_aborting_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onAborting(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The error action in ERROR state
	## former rtc_error_do()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onError(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The reset action that is invoked resetting
	## This is same but different the former rtc_init_entry()
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onReset(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The state update action that is invoked after onExecute() action
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##

	##
	#def onStateUpdate(self, ec_id):
	#
	#	return RTC.RTC_OK
	
	###
	##
	## The action that is invoked when execution context's rate is changed
	## no corresponding operation exists in OpenRTm-aist-0.2.0
	##
	## @param ec_id target ExecutionContext Id
	##
	## @return RTC::ReturnCode_t
	##
	##
	#def onRateChanged(self, ec_id):
	#
	#	return RTC.RTC_OK
	



def NAOCommandInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=naocommand_spec)
    manager.registerFactory(profile,
                            NAOCommand,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    NAOCommandInit(manager)

    # Create a component
    comp = manager.createComponent("NAOCommand")

def main():
	mgr = OpenRTM_aist.Manager.init(sys.argv)
	mgr.setModuleInitProc(MyModuleInit)
	mgr.activateManager()
	mgr.runManager()

if __name__ == "__main__":
	main()

