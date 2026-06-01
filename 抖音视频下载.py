import os
import re
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


class DouyinDownloader:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
            'Referer': 'https://www.douyin.com/',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        self.base_url = "https://www.douyin.com/web/api/v2/aweme/post/"
        self.video_dir = f"douyin_{self.user_id}"
        os.makedirs(self.video_dir, exist_ok=True)

    def get_sec_uid(self):
        """通过抖音号获取sec_uid"""
        search_url = f"https://www.douyin.com/web/api/v2/user/info/?user_id={self.user_id}"
        response = self.session.get(search_url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('user_info', {}).get('sec_user_id')
        raise Exception("无法获取sec_uid，请检查抖音号是否正确")

    def get_video_list(self, max_cursor=0):
        """获取视频列表（分页处理）"""
        params = {
            'user_id': self.user_id,
            'count': 20,
            'max_cursor': max_cursor,
            'aid': 1128,
            '_signature': '_02B4Z6wo00f01'  # 需动态获取，此处为示例
        }
        response = self.session.get(self.base_url, params=params, headers=self.headers)
        if response.status_code == 200:
            return response.json().get('aweme_list', []), response.json().get('has_more')
        return [], False

    def get_video_url(self, video_data):
        """提取无水印视频地址"""
        play_addr = video_data.get('video', {}).get('play_addr', {})
        if play_addr.get('url_list'):
            return play_addr['url_list'][0].replace('playwm', 'play')
        return None

    def download_video(self, video_url, title):
        """多线程下载视频"""
        try:
            response = self.session.get(video_url, stream=True, timeout=30)
            if response.status_code == 200:
                filename = f"{self.video_dir}/{title}.mp4"
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            f.write(chunk)
                return f"成功: {title}"
        except Exception as e:
            return f"失败: {title} - {str(e)}"

    def run(self):
        """主执行流程"""
        print(f"开始处理用户: {self.user_id}")
        sec_uid = self.get_sec_uid()
        print(f"获取到sec_uid: {sec_uid}")

        all_videos = []
        max_cursor = 0
        with tqdm(total=100, desc="获取视频列表") as pbar:
            while True:
                videos, has_more = self.get_video_list(max_cursor)
                all_videos.extend(videos)
                max_cursor = videos[-1].get('cursor', 0) if videos else 0
                pbar.update(10)
                if not has_more:
                    break

        print(f"共找到 {len(all_videos)} 个视频，开始下载...")
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for idx, video in enumerate(all_videos):
                title = re.sub(r'[^\w\-_\. ]', '_', video.get('desc', f'video_{idx}'))
                video_url = self.get_video_url(video)
                if video_url:
                    futures.append(executor.submit(self.download_video, video_url, title))

            for future in tqdm(futures, total=len(futures), desc="下载进度"):
                print(future.result())


if __name__ == "__main__":
    user_id = input("请输入抖音号（不带@）：")
    downloader = DouyinDownloader(user_id)
    downloader.run()