import asyncio
import vk_api
from config import VK_API_KEY, VK_GROUP_ID
from db.db_interval import get_time_interval
from vk_back.timers.converter import convert_time

#########################---VKAPI---##########################
async def send_post(photo):
    vk_session = vk_api.VkApi(token=VK_API_KEY)
    bot = vk_session.get_api()
    upload = vk_api.VkUpload(bot)
    photos = upload.photo_wall(photo, group_id=int(VK_GROUP_ID))
    attachment = f'photo{photos[0]["owner_id"]}_{photos[0]["id"]}'
    push = vk_session.method('wall.post', {'owner_id': f'-{VK_GROUP_ID}', 'from_group': 1, 'attachments': attachment})
    post = f'https://vk.com/wall-{VK_GROUP_ID}_{push["post_id"]}'
    return post

async def delay_post(photo, user_id):

    vk_session = vk_api.VkApi(token=VK_API_KEY)
    bot = vk_session.get_api()
    upload = vk_api.VkUpload(bot)
    photos = upload.photo_wall(photo, group_id=int(VK_GROUP_ID))
    attachment = f'photo{photos[0]["owner_id"]}_{photos[0]["id"]}'
    date = convert_time(user_id)
    push = vk_session.method('wall.post', {'owner_id': f'-{VK_GROUP_ID}', 'from_group': 1, 'publish_date': date, 'attachments': attachment})
    post = f'https://vk.com/wall-{VK_GROUP_ID}_{push["post_id"]}'
    return {"post": post, "date": date}


#########################---VKAPI---##########################