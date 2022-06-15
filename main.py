import vkdownloader as vk
import yauploader as yu


if __name__ == '__main__':
    vk_token = input('Enter your VK token: ')
    vk_id = input("Enter VK id (only numbers). If you want download photos from your account, press Enter \n")
    if vk_id == '':
        vk_id = None
    ya_token = input('Enter your Yandex Disk token: ')
    vk_dl = vk.VKDownloader(vk_token, '5.131', vk_id)
    json_path = vk_dl.get_photos()
    ya_upl = yu.YaUploader(ya_token)
    ya_upl.upload_remote_files(json_path)
