import vkdownloader as vk


if __name__ == '__main__':
    with open('VK_token.txt') as vkt:
        vk_token = vkt.readline().strip()
    vk_dl = vk.VKDownloader(vk_token, '5.131')
    vk_dl.get_photos()
    # vk_dl.make_photos_data_json()

