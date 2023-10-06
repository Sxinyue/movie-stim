import sys
import time
import os
import socket
from psychopy import gui, visual, event, clock, core

if __name__ == '__main__':

    # socket
    ip = '127.0.0.1'
    port = 9999
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    try:
        s.connect((ip, port))
    except Exception as e:
        print('服务器不在线')
        sys.exit()
    # Ensure that relative paths start from the same directory as this script
    _thisDir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(_thisDir)

    expInfo = {'name': 'xxx',
               'gender': ['m', 'f'], 'age': 18,
               'hair length': ['short', 'median', 'long']
               }
    dlg = gui.DlgFromDict(expInfo, title='EmotionRecognition',
                          order=['name', 'gender', 'age', 'hair length'])
    if dlg.OK:
        pass
    else:
        print('user cancelled!')
        core.quit()

    date = time.strftime('_20%y_%m_%d_%H_%M', time.localtime())
    file_path = 'data/' + expInfo['name'] + '_' + expInfo['gender'] + '_' + date  #
    with open('%s.csv' % file_path, 'a') as file:
        file.write('name' + ',' + 'gender' + ',' + 'age' + ',' + 'hair length' + '\n')
        file.write(
            expInfo['name'] + ',' + expInfo['gender'] + ',' + str(expInfo['age']) + ',' + expInfo['hair length'] + '\n')
        file.write(
            'trial_id' + ',' + 'valence' + ',' + 'arousal' + ',' + 'happy' + ',' + 'neutral' + ',' + 'sad' + '\n')

    # set up the window
    win = visual.Window(size=[2560, 1440], color='#010101', fullscr=False, units='pix')
    # win.mouseVisible = False # hide mouse

    # store frame rate of monitor if we can measure it
    expInfo['frameRate'] = win.getActualFrameRate()
    if expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess

    # Initialize components
    fixation_beg = visual.TextStim(win, text='+', color='white', height=100, bold=True)
    fixation_end = visual.TextStim(win, text='+', color='white', height=100, bold=True)
    instruction = visual.ImageStim(win, image='pic/exp_instruction.png')
    end = visual.ImageStim(win, image='pic/exp_end.png')
    video_path = 'video/{:02d}.mp4'
    text_end = visual.TextStim(win, height=40,
                               text=u'本次trial已经结束，15秒后开始下一个trial')
    text_valence = visual.TextStim(win, height=40,
                                   text=u'你的valence值是？')
    text_arousal = visual.TextStim(win, height=40,
                                   text=u'你的arousal值是？')
    text_happy = visual.TextStim(win, height=40,
                                 text=u'你的happy值是？')
    text_sad = visual.TextStim(win, height=40,
                               text=u'你的sad值是？')
    text_neutral = visual.TextStim(win, height=40,
                                   text=u'你的neutral值是？')
    scale_valence = visual.RatingScale(win, scale=u'1=Negative..5=Positive',
                                       low=1, high=5, precision=1, marker='circle',
                                       showValue=True, acceptPreText=u'请在横线上点击')
    scale_arousal = visual.RatingScale(win, scale=u'1=Calm..5=Active',
                                       low=1, high=5, precision=1, marker='circle',
                                       showValue=True, acceptPreText=u'请在横线上点击')
    scale_happy = visual.RatingScale(win, scale=u'1=Calm.3=Happy.5=Very Happy',
                                     low=1, high=5, precision=1, marker='circle',
                                     showValue=True, acceptPreText=u'请在横线上点击')
    scale_sad = visual.RatingScale(win, scale=u'1=Calm.3=Sad.5=Very Sad',
                                   low=1, high=5, precision=1, marker='circle',
                                   showValue=True, acceptPreText=u'请在横线上点击')
    scale_neutral = visual.RatingScale(win, scale=u'1=Emotional.3=Neutral.5=Very Neutral',
                                       low=1, high=5, precision=1, marker='circle',
                                       showValue=True, acceptPreText=u'请在横线上点击')
    # instruction
    instruction.draw()
    win.flip()
    event.waitKeys()

    i = 1
    # total 15 trial
    for trial in range(i):
        if event.getKeys(keyList=['q']):
            core.quit()
        video = visual.MovieStim(win, video_path.format(trial), size=(2560, 1440))

        s.send('1'.encode('utf-8'))
        print('开始的发送时间{}'.format(time.time()))
        fixation_beg.draw()
        win.flip()
        clock.wait(5)  # 5s fixation

        trigger_start = '2'
        s.send(trigger_start.encode('utf-8'))
        print('video开始的发送时间{}'.format(time.time()))
        while video.status != visual.FINISHED:
            video.draw()
            win.flip()
            # Esc video pause
            if event.getKeys(keyList=['escape']):
                video.pause()
                break
        trigger_end = '3'
        s.send(trigger_end.encode('utf-8'))
        print('video结束的发送时间{}'.format(time.time()))

        scale_valence.reset()
        scale_arousal.reset()
        scale_happy.reset()
        scale_neutral.reset()
        scale_sad.reset()
        while scale_valence.noResponse:
            text_valence.draw()
            scale_valence.draw()
            win.flip()
        with open('%s.csv' % file_path, 'a') as file:
            file.write(str(trial) + ',' + str(scale_valence.getRating()) + ',')

        while scale_arousal.noResponse:
            text_arousal.draw()
            scale_arousal.draw()
            win.flip()
        with open('%s.csv' % file_path, 'a') as file:
            file.write(str(scale_arousal.getRating()) + ',')

        while scale_happy.noResponse:
            text_happy.draw()
            scale_happy.draw()
            win.flip()
        with open('%s.csv' % file_path, 'a') as file:
            file.write(str(scale_happy.getRating()) + ',')

        while scale_neutral.noResponse:
            text_neutral.draw()
            scale_neutral.draw()
            win.flip()
        with open('%s.csv' % file_path, 'a') as file:
            file.write(str(scale_neutral.getRating()) + ',')

        while scale_sad.noResponse:
            text_sad.draw()
            scale_sad.draw()
            win.flip()
        with open('%s.csv' % file_path, 'a') as file:
            file.write(str(scale_sad.getRating()) + '\n')

        fixation_beg.draw()
        win.flip()
        clock.wait(15)
        if i - trial == 1:
            end.draw()
            win.flip()
            clock.wait(3)
        else:
            text_end.draw()
            win.flip()
            clock.wait(15)
    end_data = '9'
    s.send(end_data.encode('utf-8'))
    s.close()