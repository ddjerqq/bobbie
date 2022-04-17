import os
import sys

TOKEN = "OTU4MTA3OTA1NzkyNTQ0ODA5.YkIhhQ.YduxqTYY1SVVhQ84C_Ev_WBVC1M"
DEV_TEST_TOKEN = "OTYzNDU3MTI4MzM1NTUyNTUy.YlWXXw.n7uo7VtPt_4VRUDMiaqYYlzWUx0"
PREFIX = "!"

DELETE_MESSAGE_LOG    = 939534645798793247
CONFESSION_CHANNEL_ID = 958456199148343436
LOG_CHANNEL_ID        = 958311400047001600
LEAVE_CHANNEL_ID      = 942800528822370315

PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))

_LOG_FILE = r".\logs\logs.yandr"

DEV_TEST = len(sys.argv) == 2 and sys.argv[1] == "--dev-test"

GUILD_IDS = [935886444109631510, 965308417185021982]  # campfire, dev-test

STATUSES = [
    "მიეც გლახაკთა საჭურჭლე,",
    "ათავისუფლე მონები.",
    "ddjerqq#2005",
    "სიკვდილი ყველას გვაშინებს,",
    "სხვას თუ ჰკვლენ, ცქერა გვწადიან.",
    "დღეს სტუმარია ეგ ჩემი,",
    "თუნდ ზღვა ემართოს სისხლისა.",
]
