import os


def main(segments):
    ffmpeg_cmd_t = 'ffmpeg -y -loglevel repeat+level+warning -ss %s -t %s -i %s -vcodec copy -acodec copy %s'
    for seg in segments:
        m, s = divmod(seg['start'], 60)
        h, m = divmod(m, 60)
        start = "{:0>2}:{:0>2}:{:0>2}.000".format(h, m, s)
        m, s = divmod(seg['duration'], 60)
        h, m = divmod(m, 60)
        duration = "{:02d}:{:02d}:{:02d}.300".format(h, m, s)
        exec_cmd = ffmpeg_cmd_t % (start, duration, seg['source'], seg['out'])
        print(exec_cmd)
        os.system(exec_cmd)

if __name__ == '__main__':
    segments = [
        {
            'start': 79,
            'duration': 20,
            'out': '外观_79_20.mp4',
            'source': "./data/videos/E14DA7631F7A7E2A.mp4"
        },
        {
            'start': 237,
            'duration': 45,
            'out': '动力_237_45.mp4',
            'source': "./data/videos/E14DA7631F7A7E2A.mp4"
        },
        {
            'start': 298,
            'duration': 60,
            'out': '操控_298_60.mp4',
            'source': "./data/videos/E14DA7631F7A7E2A.mp4"
        },
        {
            'start': 402,
            'duration': 133,
            'out': '内饰_402_133.mp4',
            'source': "./data/videos/E14DA7631F7A7E2A.mp4"
        },
    ]
    main(segments)
