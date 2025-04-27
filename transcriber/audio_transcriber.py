import numpy as np
import whisper # free and open-source, runs locally

from transcriber import os, h5py, get_file_path

class AudioTranscriber:
    def __init__(self, audio_filename, directory=None, language=None):
        self.audio_filename = audio_filename # WITH EXTENSION
        self.path = get_file_path(audio_filename, directory=directory)

        h5_name = ".metadata"
        self.h5_path = get_file_path(h5_name, 'h5', directory)

        try:
            audio_name = self.audio_filename.rsplit('.', 1)[0]
        except IndexError:
            raise ValueError("The audio file must have an extension")
        
        self.text_path = get_file_path(audio_name, 'txt', directory)
        
        if language is not None:
            self.language = language
        else:
            self.language = 'es' # default language
        
        # languages = ['en', 'es', 'fr', 'ca']
        
    def process(self):
        '''Transcribe the audio file to text'''
        model = whisper.load_model("base", device="cpu")
        self.result = model.transcribe(self.path, language=self.language, fp16=False)
        return self.result

    def h5save(self, result=None):
        '''Save the result dictionary to an h5 file'''
        result = self.result if result is None else result
        mode = 'r+' if os.path.exists(self.h5_path) else 'x' # read/write if exists, else create file
        
        with h5py.File(self.h5_path, mode) as f:
            # Create a group for the audio file
            transcription_gr = f.create_group(self.audio_filename)

            # Store the transcription text & language
            transcription_gr.create_dataset('text', data=result['text'])
            # transcription_gr.attrs['language'] = result['language']
            transcription_gr.create_dataset('language', data=result['language'])
            
            # Store the segments data
            segments_gr = transcription_gr.create_group('segments')
            last_segment = result['segments'][-1]
            width = len(str(last_segment['id'])) # number of digits of the last segment id
            for segment in result['segments']:
                id_w0 = f'{segment['id']:0{width}}' # id with leading zeros
                segment_gr = segments_gr.create_group(id_w0)

                for key, value in segment.items():
                    data = np.array(value) if isinstance(value, list) else value
                    segment_gr.create_dataset(key, data=data)

    @staticmethod
    def decode(element):
        '''Decode bytes to utf-8'''
        if isinstance(element, bytes):
            return element.decode('utf-8')
        elif isinstance(element, np.ndarray):
            return element.tolist()
        else:
            return element

    def h5load(self):
        '''Load the result dictionary from an h5 file'''
        with h5py.File(self.h5_path, 'r') as f:
            transcription_gr = f[self.audio_filename]
            result = {
                'text': transcription_gr['text'][()].decode('utf-8'),
                'language': transcription_gr['language'][()].decode('utf-8'),
                'segments': []
            }
            for segment_id in transcription_gr['segments']:
                segment_gr = transcription_gr['segments'][segment_id]
                segment = {}
                for key in segment_gr:
                    segment[key] = self.decode(segment_gr[key][()])
                result['segments'].append(segment)
        return result
    
    def txtsave(self, result=None):
        '''Save the transcription text to a txt file'''
        result = self.result if result is None else result
        with open(self.text_path, "w") as f:
            f.write(result["text"])