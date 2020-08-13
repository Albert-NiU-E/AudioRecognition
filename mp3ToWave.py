from pydub import AudioSegment


def trans(filepath, inputName):
    # mp3转wav
    song = AudioSegment.from_mp3(filepath)
    song.export("./songsDataWav/%s.wav" % inputName, format="wav")
