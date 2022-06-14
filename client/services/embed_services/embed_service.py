from client.services.embed_services.economy_embed_service import EconomyEmbedService
from client.services.embed_services.generic_embed_service import GenericEmbedService
from client.services.embed_services.inventory_embed_service import InventoryEmbedService
from client.services.embed_services.pet_embed_service import PetEmbedService
from client.services.embed_services.utils_embed_service import UtilsEmbedService


class EmbedService:
    def __init__(self, client):
        self.economy   = EconomyEmbedService(client)
        self.generic   = GenericEmbedService(client)
        self.inventory = InventoryEmbedService(client)
        self.utils     = UtilsEmbedService(client)
        self.pets      = PetEmbedService(client)
