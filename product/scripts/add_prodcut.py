from ..models import Product, Categorie
from ..serializers import AddProductSerializer
from urllib.parse import urlparse

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


def get_random_user_agent():
    
    software_names = [SoftwareName.CHROME.value, SoftwareName.FIREFOX.value, SoftwareName.BRAVE.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agents = user_agent_rotator.get_user_agents()
    user_agent = user_agent_rotator.get_random_user_agent()
    return user_agent





def AddProduct(prod, store, cate, maxVal, more, less):
    user_agent = get_random_user_agent()

    if prod['price'] > maxVal:
        prod['price'] += more
    else:
        prod['price'] += less
    prod['store'] = store.lower()
    prod['categorie'] = cate

    instc = Product.objects.filter(name=prod.get('full_name',None)).first()
    if instc:
        update = AddProductSerializer(instc, data=prod)
        if update.is_valid():
            update.save()
    else:
        prod_serilizer = AddProductSerializer(data=prod)
        if prod_serilizer.is_valid():
                prod_serilizer.save()

 