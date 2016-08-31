/*
 * Vokaturi.h
 *
 * Copyright (C) 2016 Paul Boersma
 * version 1.1, 2016-04-29
 *
 * This code is part of Open Vokaturi and of Vokaturi Enterprise.
 *
 * Open Vokaturi is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or (at
 * your option) any later version.
 *
 * Open Vokaturi is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
 * See the GNU General Public License for more details.
 *
 * If you use the open-source edition of this software (i.e. Open Vokaturi),
 * you should have received a copy of the GNU General Public License
 * along with this software. If not, see http://www.gnu.org/licenses/.
 */

#ifdef __cplusplus
	extern "C" {
#endif

typedef struct structVokaturiVoice *VokaturiVoice;

VokaturiVoice VokaturiVoice_create (
	double sample_rate,
	int buffer_length
);

void VokaturiVoice_fill (
	VokaturiVoice voice,
	int num_samples,
	double samples []
);

typedef struct {
	int valid;   // 1 = "there were voiced frames, so that the measurements are valid"; 0 = "no voiced frames found"
	int num_frames_analyzed;
	int num_frames_lost;
} VokaturiQuality;

typedef struct {
	double pitAve;   // average pitch, in semitones
	double pitSlo;   // pitch slope for voiced parts, in semitones per second
	double intAve;   // average intensity, in dB
	double intSlo;   // intensity slope for voice parts, in dB per second
	double spcSlo;   // spectral slope
} VokaturiCueStrengths;

typedef struct {
	double neutrality;
	double happiness;
	double sadness;
	double anger;
	double fear;
} VokaturiEmotionProbabilities;

void VokaturiVoice_extract (
	VokaturiVoice voice,
	VokaturiQuality *quality,
	VokaturiCueStrengths *cueStrengths,
	VokaturiEmotionProbabilities *emotionProbabilities
);

void VokaturiVoice_destroy (VokaturiVoice voice);

const char *Vokaturi_versionAndLicense ();

#ifdef __cplusplus
	}
#endif

/* End of file Vokaturi.h */
