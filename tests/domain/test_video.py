from summarizer.domain.model.video import Video

def test_video():
    test = Video(url="tests/1.mp4")
    images = test._read_video()
    idx = 0
    for image in images:
        #temp = image.extract()
        idx += 1
    print(idx)
    assert images is  None