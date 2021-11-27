import moviepy.editor as mpy
from moviepy.audio.io.AudioFileClip import AudioFileClip

v_codec = "libx264"

video_quality = "24"

compression = "slow"

load_title = input("Enter the Title of the Clip: ")

save_format = input("Enter the file format for the final clip: ")

save_title = load_title[0:-4] + "_clipped." + save_format

audio_clip = input("Enter the name of an audio file: ")

cuts = [('00:00:10.00', '00:00:25.00')]


def edit_video(load_title, save_title, cuts):
    video = mpy.VideoFileClip(load_title)

    # The Cuts
    clips = []
    for cut in cuts:
        clip = video.subclip(cut[0], cut[1])
        clips.append(clip)

    final_clip = mpy.concatenate_videoclips(clips)

    # Test Texts
    txt = mpy.TextClip("Just Some Test Text!!", font='Arial',
                       fontsize=72, color='white', bg_color='transparent')
    txt = txt.set_position(('center', 0.6), relative=True)
    txt = txt.set_start((0, 4))  # (minutes, seconds)
    txt = txt.set_duration(3)
    txt = txt.crossfadein(0.5)
    txt = txt.crossfadeout(0.5)

    final_clip = mpy.CompositeVideoClip([final_clip, txt])

    final_clip_new_audio = final_clip.set_audio(AudioFileClip(audio_clip)).subclip(0, 14)

    # Saving the Final Clip
    final_clip_new_audio.write_videofile(save_title,
                                         threads=4, fps=60,
                                         codec=v_codec,
                                         preset=compression,
                                         ffmpeg_params=["-crf", video_quality])

    video.close()


if __name__ == "__main__":
    edit_video(load_title, save_title, cuts)
