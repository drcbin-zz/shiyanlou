from task import send_pic_task

def screen_shot(file_name='screen_shot', file_type='png'):
    print('3秒后截图')

    time.sleep(3)

    ret = commends.getstatusoutput('scrot' + file_name + 'tmp.' + file_type)

    if ref[0] != 0:
        print('图片类型不支持,请换用png,jpg等常用格式')
        return

    with open(file_name + 'tmp.' + file_type, 'wb') as f:
        send_pic_task(f.read(), file_name, file_type)
    # os.remove(file_name + 'tmp.' + file_type)
    print('截图完成')



