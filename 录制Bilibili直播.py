import requests
import time
import subprocess
import os

# 配置信息
UP_UID = "你的up主uid"  # 替换为目标主播的UID
SAVE_PATH = "./recordings"  # 视频保存路径
FFMPEG_PATH = "ffmpeg"  # ffmpeg可执行文件路径，如果在PATH中可以直接使用


def get_live_info(uid):
    """获取主播直播状态"""
    url = f"https://api.bilibili.com/x/space/acc/info?mid={uid}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Window NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
    }
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        if data['code'] == 0:
            return {
                'live_status': data['data']['live_status'],  # 1为直播中，0为未直播
                'title': data['data']['title'],
                'cover': data['data']['cover']
            }
    except Exception as e:
        print(f"获取主播信息失败：{e}")
    return {'live_status': 0}


def start_recording(stream_url, filename):
    """启动录制"""
    output_path = os.path.join(SAVE_PATH, f"{filename}.mp4")
    command = [
        FFMPEG_PATH,
        '-i', stream_url,
        '-c', 'copy',
        '-f', 'mp4',
        output_path
    ]

    try:
        print(f"开始录制：{output_path}")
        subprocess.run(command, check=True)
    except Exception as e:
        print(f"录制过程中出现：{e}")


def main():
    """主程序"""
    if not os.path.exists(SAVE_PATH):
        os.makedirs(SAVE_PATH)

    last_status = 0
    while True:
        live_info = get_live_info(UP_UID)
        current_status = live_info['live_status']

        if current_status == 1 and last_status != 1:
            # 检测到直播开始
            print(f"检测到{UP_UID}开播：{live_info['title']}")

            # 获取直播流地址（这里需要进一步获取）
            # 注意：实际中可能需要通过其他API获取直播流地址，比如https：//api.bilibili.com/x/live/web(room)
            stream_url = "替换为实际的直播流地址"  # 需要根据实际情况获取
            filename = time.strftime("%Y%m%d_%H%M%S", time.localtime())

            start_recording(stream_url, filename)

        last_status = current_status
        time.sleep(30)  # 每隔30秒检查一次


if __name__ == '__main__':
    main()
