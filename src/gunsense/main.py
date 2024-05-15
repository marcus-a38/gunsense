from gsutil import handle
#from argparse import ArgumentParser

def main():
    handle(
        video_input='src/gunsense/test.mp4',
        fps=None,
        cons_thresh=2,
        log_frames=True
    )
    return 0

if __name__ == "__main__":
    main()