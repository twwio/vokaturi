# Vokaturi.py
# Copyright (C) 2016 Vokaturi B.V.
# version 2016-04-14

# This file is the Python interface to the Vokaturi library.
# The declarations are parallel to those in Vokaturi.h.

import ctypes

class Quality(ctypes.Structure):
	_fields_ = [
		("num_frames_analyzed",  ctypes.c_int),
		("num_frames_lost",      ctypes.c_int)]

class CueStrengths(ctypes.Structure):
	_fields_ = [
		("pit_ave",  ctypes.c_double),
		("pit_slo",  ctypes.c_double),
		("int_ave",  ctypes.c_double),
		("int_slo",  ctypes.c_double),
		("spc_slo",  ctypes.c_double)]

class EmotionProbabilities(ctypes.Structure):
	_fields_ = [
		("neutrality",  ctypes.c_double),
		("happiness",   ctypes.c_double),
		("sadness",     ctypes.c_double),
		("anger",       ctypes.c_double),
		("fear",        ctypes.c_double)]

_library = None

def load(path_to_Vokaturi_library):
	global _library

	_library = ctypes.CDLL(path_to_Vokaturi_library)

	_library.VokaturiVoice_create.restype = ctypes.c_void_p
	_library.VokaturiVoice_create.argtypes = [
		ctypes.c_double,                           # sample_rate
		ctypes.c_int]                              # buffer_length

	_library.VokaturiVoice_fill.restype = None
	_library.VokaturiVoice_fill.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.c_int,                              # num_samples
		ctypes.POINTER (ctypes.c_double)]          # samples

	_library.VokaturiVoice_extract.restype = None
	_library.VokaturiVoice_extract.argtypes = [
		ctypes.c_void_p,                           # voice
		ctypes.POINTER (Quality),                  # quality
		ctypes.POINTER (CueStrengths),             # cueStrengths
		ctypes.POINTER (EmotionProbabilities)]     # emotionProbabilities

	_library.VokaturiVoice_destroy.restype = None
	_library.VokaturiVoice_destroy.argtypes = [
		ctypes.c_void_p]                           # voice

	_library.Vokaturi_versionAndLicense.restype = ctypes.c_char_p
	_library.Vokaturi_versionAndLicense.argtypes = []

class Voice:

	def __init__(self, sample_rate, buffer_length):
		self._voice = _library.VokaturiVoice_create(sample_rate, buffer_length)

	def fill(self, num_samples, samples):
		_library.VokaturiVoice_fill(self._voice, num_samples, samples)

	def extract(self, quality, cueStrengths, emotionProbabilities):
		_library.VokaturiVoice_extract(self._voice, quality, cueStrengths, emotionProbabilities)

	def destroy(self):
		if not _library is None:
			_library.VokaturiVoice_destroy(self._voice)

def versionAndLicense():
	return _library.Vokaturi_versionAndLicense().decode("UTF-8")

def SampleArrayC(size):
	return (ctypes.c_double * size)()
