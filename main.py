from typing import Final
import discord
from dotenv import load_dotenv
from discord import Intents, Embed, app_commands
from discord.ext import commands
from format_data import FormattedMoveData
import json
import os
import asyncio
import smtplib
from email.message import EmailMessage


# BE WARNED THIS CODE IS VERY SPAGHETTI! IT SUCKS!

# Load environment variables
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
APP_ID = int(os.getenv("APP_ID"))

# Setup Discord bot
intents: Intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, application_id=APP_ID)

# ========== DATA HELPERS ==========
move_alias_map = {
    "robo-ky": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6PP": ["Forward Punch 2"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash", "laser", "sweep"],
        "2S Heat": ["Crouching Slash Heat", "laser heat", "sweep heat"],
        "2H": ["Crouching Heavy", "missle", "Knee rocket"],
        "2H Heat": ["Crouching Heavy Heat", "missle heat", "Knee rocket heat"],
        "2d": ["gimmick", "gimmic-ky", "gimmic", "gimmicky", "mat"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust", "Peddle"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "Overheat Explosion": ["OE"],
        "63214k": ["63214k", "skyline", "s-ky-line"],
        "[P + K]": ["P+K", "[P+K]", "P + K", "Delayed Getup", "DG"],
        "236S": ["Don't Get Coc-KY! Level 1", "Don't Get Coc-KY! Lvl 1", "Don't Get Coc-KY! Lvl1", "Don't Get Coc-KY! 1", "Don't Get Coc-KY!", "Don't Get Coc-KY Level 1", "Don't Get Coc-KY", "Don't Get Coc-KY Lvl 1", "Don't Get Coc-KY Lvl1", "Don't Get Coc-KY 1", "Don't Get Cocky", "Don't Get Cocky Level 1", "Don't Get Cocky Lvl 1", "Don't Get Cocky Lvl1", "Don't Get Cocky 1", "DGC", "DGC Level 1", "DGC Lvl 1", "DGC Lvl1", "DGC 1", "236S Level 1", "236S Lvl 1", "236S Lvl1", "236S 1"],
        "236S Level 2": ["Don't Get Coc-KY! Level 2", "Don't Get Coc-KY! Lvl 2", "Don't Get Coc-KY! Lvl2", "Don't Get Coc-KY! 2", "Don't Get Coc-KY Level 2", "Don't Get Coc-KY Lvl 2", "Don't Get Coc-KY Lvl2", "Don't Get Coc-KY 2", "Don't Get Cocky Level 2", "Don't Get Cocky Lvl 2", "Don't Get Cocky Lvl2", "Don't Get Cocky 2", "DGC Level 2", "DGC Lvl 2", "DGC Lvl2", "DGC 2", "236S Level 2", "236S Lvl 2", "236S Lvl2", "236S 2"],
        "236S Level 3": ["Don't Get Coc-KY! Level 3", "Don't Get Coc-KY! Lvl 3", "Don't Get Coc-KY! Lvl3", "Don't Get Coc-KY! 3", "Don't Get Coc-KY Level 3", "Don't Get Coc-KY Lvl 3", "Don't Get Coc-KY Lvl3", "Don't Get Coc-KY 3", "Don't Get Cocky Level 3", "Don't Get Cocky Lvl 3", "Don't Get Cocky Lvl3", "Don't Get Cocky 3", "DGC Level 3", "DGC Lvl 3", "DGC Lvl3", "DGC 3", "236S Level 3", "236S Lvl 3", "236S Lvl3", "236S 3"],
        "214S": ["Fun-KY", "Fun-KY Level 1", "Fun-KY Lvl 1", "Fun-KY! Lvl1", "Fun-KY 1", "Fun-KY Level 1", "Fun-KY Lvl 1", "Fun-KY Lvl1", "Fun-KY 1", "Funky", "Funky Level 1", "Funky Lvl 1", "Funky Lvl1", "Funky 1", "214S", "214S Level 1", "214S Lvl 1", "214S Lvl1", "214S 1"],
        "214S Level 2": ["Fun-KY Level 2", "Fun-KY Lvl 2", "Fun-KY! Lvl2", "Fun-KY 2", "Fun-KY Level 2", "Fun-KY Lvl 2", "Fun-KY Lvl2", "Fun-KY 2", "Funky Level 2", "Funky Lvl 2", "Funky Lvl2", "Funky 2", "214S Level 2", "214S Lvl 2", "214S Lvl2", "214S 2"],
        "214S Level 3": ["Fun-KY Level 2", "Fun-KY Lvl 2", "Fun-KY! Lvl2", "Fun-KY 2", "Fun-KY Level 2", "Fun-KY Lvl 2", "Fun-KY Lvl2", "Fun-KY 2", "Funky Level 2", "Funky Lvl 2", "Funky Lvl2", "Funky 2", "214S Level 2", "214S Lvl 2", "214S Lvl2", "214S 2"],
        "623H": ["623H Level 1", "623H Lvl1", "623H 1", "Hun-KY Homerun", "Hun-KY Homerun Level 1", "Hun-KY Homerun Lvl1", "Hun-KY Homerun 1", "Hunky Homerun", "Hunky Homerun Level 1", "Hunky Homerun Lvl1", "Hunky Homerun 1", "HH", "HH Level 1", "HH Lvl1", "HH 1", "Homerun", "Homerun Level 1", "Homerun Lvl1", "Homerun 1"],
        "623H Level 2": ["623H Level 2", "623H Lvl2", "623H 2", "Hun-KY Homerun Level 2", "Hun-KY Homerun Lvl2", "Hun-KY Homerun 2", "Hunky Homerun Level 2", "Hunky Homerun Lvl2", "Hunky Homerun 2", "HH Level 2", "HH Lvl2", "HH 2", "Homerun Level 2", "Homerun Lvl2", "Homerun 2"],
        "623H Level 3": ["623H Level 3", "623H Lvl3", "623H 3", "Hun-KY Homerun Level 3", "Hun-KY Homerun Lvl3", "Hun-KY Homerun 3", "Hunky Homerun Level 3", "Hunky Homerun Lvl3", "Hunky Homerun 3", "HH Level 3", "HH Lvl3", "HH 3", "Homerun Level 3", "Homerun Lvl3", "Homerun 3"],
        "j.623H": ["j623h", "j623h level 1", "j623h lvl1", "j623h 1" "j.623H level 1", "j.623H lvl1", "j.623H 1", "Air Hun-KY Homerun"," Air Hun-KY Homerun Level 1", "Air Hunky Homerun", "Air Hunky Homerun Level 1", "Air Hunky Homerun Lvl1", "Air Hunky Homerun 1", "Air HH", "Air HH level 1", "Air HH lvl1", "Air HH 1" "Air Homerun", "Air Homerun Lvl1", "Air Homerun Level 1", "Air Homerun 1"],
        "j.623H level 2": ["j623h level 2", "Air Hun-KY Homerun Level 2", "j623h lvl2", "j623h 2" "j.623H level 2", "j.623H lvl2", "j.623H 2", "Air Hun-KY Homerun 2"," Air Hun-KY Homerun Level 2", "Air Hunky Homerun 2", "Air Hunky Homerun Level 2", "Air Hunky Homerun Lvl2", "Air Hunky Homerun 2", "Air HH 2", "Air HH level 2", "Air HH lvl2", "Air HH 2" "Air Homerun 2", "Air Homerun Lvl2", "Air Homerun Level 2", "Air Homerun 2"],
        "j.623H level 3": ["j623h level 3", "Air Hun-KY Homerun Level 3", "j623h lvl3", "j623h 3" "j.623H level 3", "j.623H lvl3", "j.623H 3", "Air Hun-KY Homerun 3"," Air Hun-KY Homerun Level 3", "Air Hunky Homerun 3", "Air Hunky Homerun Level 3", "Air Hunky Homerun Lvl3", "Air Hunky Homerun 3", "Air HH 3", "Air HH level 3", "Air HH lvl3", "Air HH 3" "Air Homerun 3", "Air Homerun Lvl3", "Air Homerun Level 3", "Air Homerun 3"],
        "j.236S": ["j236S", "j236S Level 1", "j236S Lvl1", "j236S 1", "j.236S Level 1", "j.236S Lvl1", "j.236S 1", "Jun-KY Bargain", "Jun-KY Bargain Level 1", "Jun-KY Bargain Lvl1", "Jun-KY Bargain 1", "Junky Bargain", "Junky Bargain Level 1", "Junky Bargain Lvl1", "Junky Bargain 1", "JB", "JB Level 1", "JB Lvl1", "JB 1"],
        "j.236S level 2": ["j236S Level 2", "j236S Lvl2", "j236S 2", "j.236S Lvl2", "j.236S 2", "Jun-KY Bargain Level 2", "Jun-KY Bargain Lvl2", "Jun-KY Bargain 2", "Junky Bargain Level 2", "Junky Bargain Lvl2", "Junky Bargain 2", "JB Level 2", "JB Lvl2", "JB 2"],
        "j.236S level 3": ["j236S level 3", "j236S Lvl3", "j236S 3", "j.236S Lvl3", "j.236S 3", "Jun-KY Bargain Level 3", "Jun-KY Bargain Lvl3", "Jun-KY Bargain 3", "Junky Bargain Level 3", "Junky Bargain Lvl3", "Junky Bargain 23", "JB Level 3", "JB Lvl3", "JB 3"],
        "66P/K/S/H": ["Spi-KY", "SpiKY", "66X", "66P", "66K", "66S", "66H", "66X"],
        "j.214D": ["j214D", "Today's S-KY's Beautiful", "Today's SKY's Beautiful", "Today SKY Beautiful", "TSB", "Roflcopter", "Stormlockable"],
        "236236S > S x N": ["What's Useless Will Always Be So", "What Useless Will Always Be So", "WUWABS", "236236S", "Kenshiro", "JoJo"],
        "Automatic After 623H": ["Whac-KY Blow", "Whacky Blow", "Wacky Blow", "WB"],
        "236236P": ["Ris-KY Lovers", "Risky Lovers", "RL", "Overclock", "Robo Install", "Install", "Genky Lovers"],
        "236236P Explosion": ["Ris-KY Lovers Explosion", "Risky Lovers Explosion", "RL Explosion", "Overclock Explosion", "236236P[e]"],
        "236236H": ["13 Lucky", "13 Luck-KY", "Instant Kill", "IK"]
    },
    "ky kiske": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6H": ["Forward Heavy"],
        "3H": ["Diagonal Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "236S": ["Stun Edge S", "SE S", "Stun Edge", "SE"],
        "236H": ["Stun Edge H", "SE H"],
        "j.236S": ["j236S", "Air Stun Edge S", "Air SE S", "Air Stun Edge", "Air SE"],
        "j.236H": ["j236H", "Air Stun Edge H", "Air SE H"],
        "236D": ["Charged Stun Edge", "CSE"],
        "j.236D": ["j236D", "Air Charged Stun Edge", "Air CSE"],
        "623S": ["DP S", "Vapor Thrust S", "VT S", "Vapor Thrust", "VT", "DP"],
        "623H": ["DP H", "Vapor Thrust H", "VT H"],
        "j.623S/H": ["j623S/H", "j.623S", "j.623H", "j623S", "j623H", "Air DP", "DP", "Air Vapor Thrust", "Air VT"],
        "623S/H > S": ["623S > S", "623H > S", "Lightning Javelin S", "Lightning Javelin", "LJ", "LJ S"],
        "623S/H > H": ["623S > H", "623H > H", "Lightning Javelin H", "LJ H"],
        "236K": ["Stun Dipper", "SD", "Dipper"],
        "214K": ["Greed Sever", "GS", "Sever"],
        "236D > 4D > 46D": ["Charge Drive", "CD"],
        "214D": ["FB Greed Sever", "FB GS", "FB Sever" "Force Break Greed Sever", "Force Break GS", "Force Break Sever"],
        "j.214D": ["j214D", "Stun Raising", "SR"],
        "632146H": ["Ride The Lightning", "RTL"],
        "j.632146H": ["j632146H", "air ride the lightning", "air rtl"],
        "236236H": ["Rising Force", "RF", "Instant Kill", "IK"]
    },
    "potemkin": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "[4]6H": ["46H", "hammerfall", "hammer fall", "hammer"],
        "j.632146D": ["j632146D", "aerial pb", "aerial p.b.", "air p.b.", "air pb", "aerial pot buster", "air potemkin buster", "air pot buster", "Aerial Potemkin Buster"],
    },
    "faust": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "j.2K": ["j2K"],
        "41236K > 4": ["Withdraw"],
        "4 > 236P": ["Holler", "Holler!", "41236K > 4 > 236P"],
        "236P > 236P": ["Can't Hear You!", "Can't Hear You", "41236K > 4 > 236P > 236P"],
        "j.236P": ["j236P", "Love", "Air Bomb"],
        "236P": ["What Could This Be?", "What Could This Be"],
        "4 > 236D > 236D": ["Gettin' to the Good Part > 236D", "This One's on the House", "This One on the House"],
        "j.236D": ["j236D", "FB Rerere no Choutsuki", "Force Break Rerere no Choutsuki", "FB Pogo", "Force Break Pogo"],
        "214S": ["From The Above", "From Above"],
        "236236P": ["W-W-What Could This Be?", "W-W-What Could This Be"],
    },
    "order-sol": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "214[D]": ["Charge", "214[D]"],
        "Special > D": ["Action Charge", "ac"],
        "Special > j.D": ["Air Action Charge", "Air AC", "Special > jD"],
        "236P": ["236P Level 1", "236P Lvl 1", "236P 1", "Blockhead Buster", "Blockhead Buster Level 1", "Blockhead Buster Lvl 1", "BHB1", "Blockhead Buster 1"],
        "236P Level 2": ["236P Level 2", "236P Lvl 2", "236P 2", "Blockhead Buster Level 2", "Blockhead Buster Lvl 2", "BHB2", "Blockhead Buster 2"],
        "236P Level 3": ["236P Level 3", "236P Lvl 3", "236P 3", "Blockhead Buster Level 3", "Blockhead Buster Lvl 3", "BHB3", "Blockhead Buster 3"],
        "j.623H": ["j623H Lvl 1", "j.623H Lvl 1", "j623H Level 1", "j.623H Level 1", "j.623H"],
        "j.623H level 2": ["j623H Lvl 2", "j.623H Lvl 2", "j623H Level 2", "j.623H Level 2"],
        "j.623H level 3": ["j623H Lvl 3", "j.623H Lvl 3", "j623H Level 3", "j.623H Level 3"],
        "j.236K": ["j236K Lvl 1", "j.236K Lvl 1", "j236K Level 1", "j.236K Level 1", "j.236K"],
        "j.236K level 2": ["j236K Lvl 2", "j.236K Lvl 2", "j236K Level 2", "j.236K Level 2"],
        "j.236K level 3": ["j236K Lvl 3", "j.236K Lvl 3", "j236K Level 3", "j.236K Level 3"]
    },
    "justice": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "D + X": ["Blue Burst", "D + P", "D + K", "D + S", "D + H"],
        "236P": ["Valkyrie Arc", "VA"],
        "41236S": ["Michael Sword S", "MSS", "Michael Sword", "MS"],
        "41236H": ["Michael Sword H", "MSH"],
        "j.41236S": ["j41236S", "j.41236S", "Air Michael Sword S", "AMSS", "Air Michael Sword", "AMS"],
        "j.41236H": ["j41236H", "j.41236H", "Air Michael Sword H", "AMSH"],
        "623K": ["Strike Back Tail", "S.B.T.", "SBT"],
        "22[X] > ]X[": ["Nuclear Blast", "N.B.", "NB", "22[P] > ]P[", "22[S] > ]S[", "22[K] > ]K[", "22[D] > ]D[", "22[H] > ]H[", "22[P]", "22[K]", "22[S]", "22[H]", "22[D]", "22[X]", "22P", "22K", "22S", "22H", "22D", "22X"],
        "236D": ["Saperia Trance", "ST"], 
        "j.236D": ["Air Saperia Trance", "Air ST", "j236D"], 
        "632146H": ["Michael Blade", "MB"],
        "632146S": ["Imperial Ray", "IR"],
        "46463214H": ["Gamma Ray", "GR"],
        "46463214S": ["Omega Shift", "Install"],
        "236236H": ["X Laser", "Laser", "Instant Kill", "IK"]
    },
    "baiken": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "j.H": ["jH", "j.H"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "236K": ["Tatami Gaeshi", "TTG"],
        "j.236K": ["Air Tatami Gaeshi", "Air TG", "j236K"],
        "j.623S": ["j623S", "Youzansen"],
        "63214K": ["Suzuran"],
        "412K": ["Mawarikomi"],
        "412H": ["Ouren"],
        "412D > P/K/S": ["Baku: XXX", "Baku XXX", "XXX", "412D > P", "412D > K", "412D > S", "412D > X"],
        "412D > P/K/S > P": ["Baku Followup P", "BF P", "Baku Followups P", "Baku Followup", "Baku Followups", "BF", "412D > P > P", "412D > K > P", "412D > S > P", "421D > X > P"],
        "412D > P/K/S > K": ["Baku Followup K", "BF K", "Baku Followups K", "412D > P > K", "412D > K > K", "412D > S > K", "421D > X > K"],
        "412D > P/K/S > S": ["Baku Followup S", "BF S", "Baku Followups S", "412D > P > S", "412D > K > S", "412D > S > S", "421D > X > S"],
        "412D > P/K/S > H": ["Baku Followup H", "BF H", "Baku Followups H", "412D > P > H", "412D > K > H", "412D > S > H", "421D > X > H"],
        "412D > P/K/S > D": ["Baku Followup D", "BF D", "Baku Followups D", "412D > P > D", "412D > K > D", "412D > S > D", "421D > X > D"],
        "236D": ["Triple Tatami Gaeshi", "TTG"],
        "236236S": ["Tsurane Sanzu Watashi", "TSW", "Strong Reversal"],
        "236236H": ["Garyou Tensei", "GT", "Instant Kill", "IK"]
    },
    "jam kuradoberi": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "22K/S/H": ["22K", "22S", "22H", "Breath of Asanagi", "BOA"],
        "236K":  ["Ryuujin K", "Ryuujin"],
        "j.236K":  ["Air Ryuujin", "Air Ryuujin K", "j236K"],
        "236D":  ["Ryuujin D"],
        "214K":  ["Gekirin", "Gekirin K"],
        "j.214K":  ["Air Gekirin", "Air Gekirin K", "j214K"],
        "214D":  ["Gekirin D"],
        "623K":  ["Kenroukaku", "Kenroukaku K"],
        "j.623K":  ["Air Kenroukaku", "Air Kenroukaku K", "j623K"],
        "623D":  ["Kenroukaku D"],
        "236S":  ["Bakushuu"],
        "236S > P":  ["Mawarikomi"],
        "236S > H Crossup":  ["Senri Shinshou Crossup"],
        "236P or 236S > 236P":  ["Choujin", "236S > 236P", "236P"],
        "j.236P":  ["j236P", "Air Choujin"],
        "j.2 + K":  ["j2+K", "j2+K", "j2 + K", "Houeikyaku"],
        "22D": ["FB Breath of Asanagi", "Force Break Breath of Asanagi", "FB BOA"],
        "236236H": ["Geki: Saishinshou", "Geki Saishinshou", "GS"],
        "236236H[ik]": ["Gasenkotsu", "IK", "Instant Kill"]
    },
    "kliff undersn": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["6P Level 1", "6P Lvl1", "6P 1", "Forward Punch", "Forward Punch Level 1", "Forward Punch Lvl1", "Forward Punch 1"],
        "6P Level 2": ["6P Level 2", "6P Lvl2", "6P 2", "Forward Punch Level 2", "Forward Punch Lvl2", "Forward Punch 2"],
        "6P Level 3": ["6P Level 3", "6P Lvl2", "6P 3", "Forward Punch Level 3", "Forward Punch Lvl3", "Forward Punch 3"],
        "6H": ["6H Level 1", "6H Lvl1", "6H 1", "Forward Heavy", "Forward Heavy Level 1", "Forward Heavy Lvl1", "Forward Heavy 1"],
        "6H Level 2": ["6H Level 2", "6H Lvl2", "6H 2", "Forward Heavy Level 2", "Forward Heavy Lvl2", "Forward Heavy 2"],
        "6H Level 3": ["6H Level 3", "6H Lvl2", "6H 3", "Forward Heavy Level 3", "Forward Heavy Lvl3", "Forward Heavy 3"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["6H Level 1", "6H Lvl1", "6H 1", "Crouching Heavy", "Crouching Heavy Level 1", "Crouching Heavy Lvl1", "Crouching Heavy 1"],
        "2H Level 2": ["2H Level 2", "2H Lvl2", "2H 2", "Crouching Heavy Level 2", "Crouching Heavy Lvl2", "Crouching Heavy 2"],
        "2H Level 3": ["2H Level 3", "2H Lvl2", "2H 3", "Crouching Heavy Level 3", "Crouching Heavy Lvl3", "Crouching Heavy 3"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "66": ["Step Dash", "Dash", "SD"],
        "T": ["Taunt"],
        "236P": ["Bellowing Roar", "BR", "Bellowing Roar P", "BR P"],
        "236S": ["Bellowing Roar S", "BR S"],
        "214S": ["Skull Crusher", "SC"],
        "j.214S": ["j214S", "Air Skull Crusher", "Air SC"],
        "214K": ["Nape Saddle", "NS"],
        "623H > H x N": ["Scale Ripper", "SR", "623H>HxN"],
        "214P": ["2-Steps Forward", "2 Steps Forward", "2 Steps FWD", "2SF"],
        "214P > P": ["Hellish Charge", "Charge", "214P>P"],
        "j.41236S": ["j41236S", "Limb Severer", "LS"],
        "j.236D": ["j236D", "Air Bellowing Roar", "Air BR"],
        "214P > D": ["FB Hellish Charge", "FB Charge", "Force Break Hellish Charge", "Force Break Charge", "214P>D"],
        "236236H": ["Reflex Roar", "RR"],
        "632146H/[H]": ["632146H", "632146[H]", "Sole Survivor", "SS"],
        "236236H": ["Pulverizing Dragon Roar", "Pulverizing Dragon's Roar", "PDR", "IK", "Instant Kill"],
    },
    "a.b.a": {
        "j.H": ["jH"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "6P[m]": ["6p m", "6p moroha"],
        "6P[gm]": ["6p gm", "6p goku moroha"],
        "6H[m]": ["6h m", "6h moroha"],
        "6H[gm]": ["6h gm", "6h goku moroha"],
        "2H[m]": ["2H m", "2H moroha"],
        "2H[gm]": ["2H gm", "2H goku moroha"],
        "j.D[m]": ["jd[m]", "j.d m", "j.D moroha", "jd m", "jD moroha"],
        "j.D[gm]": ["jd[gm]", "j.d gm", "j.D goku moroha", "jd gm", "jD goku moroha"],
        "D + X": ["Blue Burst", "D + P", "D + S", "D + K", "D + H"],
        "63214H": ["Bonding", "Keygrab"],
        "j.63214H": ["j63214H", "Air Bonding", "Air Keygrab"],
        "236P": ["Dragging", "Drag"],
        "236H": ["Avoidance"],
        "63214P": ["Injecting"],
        "63214H[m]": ["Bonding Moroha", "Keygrab Moroha", "63214H m", "63214H moroha"],
        "j.63214H[m]": ["Air Bonding Moroha", "Air Keygrab Moroha", "j.63214H gm", "j.63214H Goku moroha", "j63214H gm", "j63214H Goku moroha"],
        "j.41236S": ["Eradication", "j41236S"],
        "j.41236S[gm]": ["j.41236S[gm]", "Eradication Goku Moroha", "j41236S gm", "j.41236S gm", "j41236S goku moroha", "j.41236S goku moroha"],
        "63214P[m]": ["Displacement"],
        "Moroha Gauge Reaches 0": ["Suka Motion", "SM"],
        "236D": ["FB Dragging", "FB Drag", "Force Break Dragging", "Force Break Drag"],
        "236D[m]/[gm]": ["FB Avoidance", "Force Break Avoidance", "236D[m]", "236D[gm]"],
        "j.632146P": ["j632146P", "Evidence: Destruction", "Evidence Destruction", "ED"],
        "j.632146P[m]": ["j632146P m", "Evidence: Destruction Moroha", "Evidence Destruction Moroha", "ED Moroha", "j632146P moroha", "j.632146P moroha", "j.632146P m"],
        "j.632146P > 214K": ["j632146P > 214K", "Evidence: Destruction Followup", "Evidence Destruction Followup", "ED Followup"],
    },
    "slayer": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6[K]": ["6[K]", "Forward Kick Hold"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.2K": ["j2K", "Jumping Down Kick"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "236P": ["Mappa Hunch P", "MH P", "Mappa Hunch", "MH"],
        "236K": ["Mappa Hunch K", "MH K"],
        "236[P]": ["Mappa Hunch P Feint", "MH P Feint", "Mappa Hunch Feint", "MH Feint"],
        "236[K]": ["Mappa Hunch K Feint", "MH K Feint"],
        "214P": ["Dandy Step P", "DS P", "Dandy Step", "DS"],
        "214K": ["Dandy Step K", "DS K"],
        "214S": ["Dandy Step S", "DS S"],
        "214H": ["Dandy Step H", "DS H"],
        "214D": ["Dandy Step D", "DS D", "FB Dandy Step", "FB DS", "Force Break Dandy Step", "FB Dandy Step"],
        "214P/K/S/D/H > P": ["Pilebunker", "PB", "214P > P", "214K > P", "214S > P", "214D > P", "214H > P"],
        "214P/K/S/D/H > K": ["Crosswise Heel", "CH", "214P > K", "214K > K", "214S > K", "214D > K", "214H > K"],
        "214P/K/S/D/H > S": ["Under Pressure", "UP", "214P > S", "214K > S", "214S > S", "214D > S", "214H > S"],
        "214P/K/S/D/H > H": ["It's Late", "It Late", "IL", "214P > H", "214K > H", "214S > H", "214D > H", "214H > H"],
        "214P/K/S/D/H > S > H": ["It's Late Under Pressure", "It Late Under Pressure", "ILUP", "214P > S > H", "214K > S > H", "214S > S > H", "214D > S > H", "214H > S > H"],
        "236H": ["Bloodsucking Universe", "Bloodsuck", "BU", "Universe"],
        "j.214K": ["j214K", "Footloose Journey", "FJ"],
        "236D": ["Big Bang Upper", "BBU", "Big Bang", "YOLO"],
        "214P/K/S/D/H > D": ["FB Pilebunker", "FB PB", "Force Break Pilebunker", "Force Break PB", "214P > D", "214K > D", "214S > D", "214H > D", "214D > D"],
        "632146S": ["Dead on Time", "DOT"],
        "236236H": ["Eternal Wings", "EW"],
        "j.214214S": ["j214214S", "Up and Close Dandy", "UACD"],
        "236236H": ["All Dead", "AD", "Instant Kill", "IK"]
    },
    "testament": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6H": ["Forward Kick"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "236P": ["Phantom Soul P", "PS P", "Phantom Soul", "PS"],
        "236K": ["Phantom Soul K", "PS K"],
        "236D": ["FB Phantom Soul", "FB PS", "Force Break Phantom Soul"],
        "Automatic After Curse Feathers": ["Feathers"],
        "Automatic After Curse Overhead": ["Overhead"],
        "214P": ["Badlands", "BL"],
        "j.214P": ["j214P", "Air Badlands", "Air BL"],
        "41236S": ["EXE Beast S", "EB S", "EXE Beast", "EB"],
        "41236H": ["EXE Beast H", "EB H"],
        "214K": ["Warrant"],
        "22P/K": ["Lucht Warrant", "LW", "22P", "22K"],
        "214S": ["HITOMI"], 
        "214S Powered Up": ["HITOMI Powered Up"],
        "214H": ["Zeinest"],
        "j.214H": ["Air Zeinest", "j214H"],
        "214H Powered Up": ["Zeinest Powered Up"],
        "j.214H Powered Up": ["Air Zeinest Powered Up", "j214H Powered Up"],
        "214D": ["Grave Digger", "GD"],
        "j.214D": ["Air Grave Digger", "j214D", "Air GD"],
        "632146S": ["Nightmare Circular S", "NC S"],
        "236236H": ["Master of Puppets", "Master of puppet", "Puppets", "Puppet", "MOP"],
        "236236H[ik]": ["Seventh Sign", "SS", "IK", "Instant Kill"]
    },
    "bridget": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6H": ["Forward Heavy"],
        "3H": ["Diagonal Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "8/9/7/6/5/4H": ["8H", "9H", "7H", "6H", "5H", "4H", "Yo-Yo Placement", "Yo Yo Placement", "YYP"],
        "j.8/9/7/6/5/4/3/2/1H": ["j.8H", "j.9H", "j.7H", "j.6H", "j.5H", "j.4H", "j.3H", "j.2H", "j.1H", "j8H", "j9H", "j7H", "j6H", "j5H", "j4H", "j3H", "j2H", "j1H", "Air Yo-Yo Placement", "Air Yo Yo Placement", "Air YYP"],
        "Yo-Yo Set > H/[H]": ["Yo-Yo Set > H", "Yo Yo Set > H", "YYS > H", "8/9/7/6/5/4H > H", "8H > H", "9H > H", "7H > H", "6H > H", "5H > H", "4H > H", "Yo-Yo Set > [H]", "Yo Yo Set > [H]", "YYS > [H]", "8/9/7/6/5/4H > [H]", "8H > [H]", "9H > [H]", "7H > [H]", "6H > [H]", "5H > [H]", "4H > [H]"],
        "Air Yo-Yo Set > H/[H]": ["Air Yo-Yo Set > H", "Air Yo Yo Set > H"],
        "236K > K": ["Shoot"],
        "623P": ["Starship"],
        "j.623P": ["j623P", "Air Starship"],
        "Yo-Yo Set > 236H": ["Roger Rush"],
        "Yo-Yo Set > j.236H": ["Air Roger Rush"],
        "Yo-Yo Set > 214H": ["Jagged Roger"],
        "Yo-Yo Set > j.214H": ["Air Jagged Roger"],
        "Yo-Yo Set > 623H": ["Roger Hug"],
        "Yo-Yo Set > 421H": ["Roger Get"],
        "Yo-Yo Set > j.421H": ["Air Roger Get"],
        "Yo-Yo Set > 421H High": ["Roger Get High"],
        "Yo-Yo Set > j.421H High": ["Air Roger Get High"],
        "Yo-Yo Set > 236D": ["FB Roger Rush", "Force Break Roger Rush"],
        "Yo-Yo Set > j.236D": ["FB Air Roger Rush", "Force Break Air Roger Rush"],
        "Yo-Yo Set > 214D": ["FB Jagged Roger", "Force Break Jagged Roger"],
        "Yo-Yo Set > j.214D": ["FB Air Jagged Roger", "Force Break Air Jagged Roger"],
        "4123641236S": ["Maintenance Disaster", "MD"],
        "Yo-Yo Set > 632146H": ["Me and My Killing Machine", "MAMKM"],
        "Yo-Yo Set > 412364H": ["Me and My Killing Machine Delay", "MAMKM Delay"],
    },
    "zappa": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "f.S Puddle": ["fs puddle", "far slash puddle"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"], 
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "236P": ["Hello, Three Centipedes", "Hello Three Centipedes", "Hello 3 Centipedes", "Summon", "Centipedes"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "D[d]": ["Awaken Dog"],
        "5D[d]": ["5Dd", "5D Dog"],
        "6D": ["6D[d]", "6DD", "6D Dog"],
        "8D": ["8D[d]", "8DD", "8D Dog"],
        "2D[d]": ["2D[d]", "2DD", "2D Dog"],
        "4D": ["4D[d]", "4D Dog"],
        "4DD": ["4DD[d]", "4DD Dog"],
        "c.S[t]": ["cst", "Close Slash Triplets", "c.st", 'cS[t]'],
        "f.S[t]": ["fst", "Far Slash Triplets", "f.st", "Far Slash Triplets 1", "fS[t]"],
        "f.SS[t]": ["fsst", "Far Slash Triplets", "f.sst", "Far Slash Triplets 2", "fSS[t]"],
        "f.SSS[t]": ["fssst", "Far Slash Triplets", "f.sss t", "Far Slash Triplets 3", "fSSS[t]"],
        "5H[t]": ["Standing Heavy Triplets", "5Ht", "Standing Heavy Triplets 1"],
        "5HH[t]": ["5HHt", "Standing Heavy Triplets 2"],
        "5HHH[t]": ["5HHt", "Standing Heavy Triplets 3"],
        "6S[t]": ["Forward Slash Triplets", "Forward Slash", "6st", "Forward Slash Triplets 1", "Forward Slash 1"],
        "6SS[t]": ["Forward Slash Triplets 2", "Forward Slash 2", "6sst"],
        "6SSS[t]": ["Forward Slash Triplets 3", "Forward Slash 3", "6ssst"],
        "6H[t]": ["Forward Heavy Triplets"],
        "2S[t]": ["Crouching Slash Triplets", "2St", "Crouching Slash Triplets 1"],
        "2SS[t]": ["2SSt", "Crouching Slash Triplets 2"],
        "2SSS[t]": ["2SSSt", "Crouching Slash Triplets 3"],
        "2H[t]": ["Crouching Heavy Triplets", "2Ht", "Crouching Heavy Triplets 1"],
        "2HH[t]": ["2HHt", "Crouching Heavy Triplets 2"],
        "2HHH[t]": ["2HHHt", "Crouching Heavy Triplets 3"],
        "j.S[t]": ["j.St", "js[t]", "jst", "Jumping Slash Triplets"],
        "j.2S[t]": ["j.2St", "j2s[t]", "j2st", "Jumping Down Slash Triplets"],
        "j.H[t]": ["j.Ht", "jh[t]", "jht", "Jumping Heavy Triplets"],
        "236P[t]": ["Please Don't Come Back P", "PDCB P", "236P triplets", "236Pt", "Please Don't Come Back", "PDCB"],
        "236K/S/H[t]": ["Please Don't Come Back K", "PDCB K", "Please Don't Come Back S", "PDCB S", "Please Don't Come Back H", "PDCB H", "236K/S/H triplets", "236K/S/Ht", "236K triplets", "236Kt", "236K[t]", "236S triplets", "236S[t]", "236St", "236H triplets", "236H[t]", "236Ht"],
        "236D[t]": ["Please Don't Come Back D", "PDCB D", "236D triplets", "236Dt"],
        "Automatic While Haunting Banana": ["Curse Items Banana", "Curse Item Banana", "Banana"],
        "Automatic While Haunting Golf Ball": ["Curse Items Golf Ball", "Curse Item Golf Ball", "Golf Ball"],
        "Automatic While Haunting Potted Plant": ["Curse Items Potted Plant", "Curse Item Potted Plant", "Potted Plant"],
        "214P[t]": ["I Was Lonely After All...", "I Was Lonely After All", "214Pt", "214P triplets", "IWLAA"],
        "c.S[s]": ["css", "c.ss", "Close Slash Sword", "cS[s]"],
        "f.S[s]": ["fss", "Far Slash Sword", "fS[s]"],
        "5H[s]": ["Standing Heavy Sword", "5Hs"],
        "6H[s]": ["6Hs", "6H Sword", "Forward Heavy Sword"],
        "2H[s]": ["2Hs", "2H Sword", "Crouching Heavy Sword"],
        "j.S[s]": ["j.ss", "jss", "js[s]", "Jumping Slash Sword"],
        "j.H[s]": ["j.Hs", "jhs", "jh[s]", "Jumping Heavy Sword"],
        "236S[s]": ["This Has Gotta Hurt", "236Ss", "236S sword", "THGH"],
        "623H[s]": ["Please Fall", "PF", "623Hs", "623H Sword"],
        "63214H[s]": ["Come Close, and I'll Kill You", "Come Close and I'll Kill You", "I'LL KILL YOU", "Come Close and I Kill You", "CCAIKY", "63214Hs", "63214H Sword"],
        "236S > H[s]": ["This Has Gotta Hurt Followup", "236S > Hs", "236S > H sword", "THGH Followup"],
        "j.236H[s]": ["j236H[s]", "j236Hs", "j236H sword", "j.236Hs", "j.236H sword", "Coming Through", "CT"],
        "c.S[r]": ["c.Sr", "cs[r]", "csr", "close slash raou"],
        "f.S[r]": ["f.Sr", "fs[r]", "fsr", "far slash raou"],
        "5H[r]": ["Standing Heavy Raou", "5Hr"],
        "5D[r]": ["Standing Dust Raou", "5Dr"],
        "6H[r]": ["Forward Heavy Raou", "5Dr"],
        "2S[r]": ["Crouching Slash Raou", "2Sr"],
        "2H[r]": ["Crouching Heavy Raou", "2Hr"],
        "2S[r]": ["Crouching Slash Raou", "2Sr"],
        "j.S[r]": ["j.sr", "jsr", "js[r]", "Jumping Slash Raou"],
        "j.H[r]": ["j.hr", "jhr", "jh[r]", "Jumping Heavy Raou"],
        "236S[r]": ["236Sr", "236S raou", "Darkness Anthem", "DA"],
        "j.236S[r]": ["j.236Sr", "j.236S raou", "j236Sr", "j236S[r]", "j236S raou", "Air Darkness Anthem", "Air DA"],
        "236S[r] > P/K/S/H or j.236S[r] > P/K/S/H": ["236S[r] > P/K/S/H", "236S[r] > P", "236S[r] > K", "236S[r] > S", "236S[r] > H", "j.236S[r] > P/K/S/H", "j.236S[r] > P", "j.236S[r] > K", "j.236S[r] > S", "j.236S[r] > H", "j236S[r] > P/K/S/H", "j236S[r] > P", "j236S[r] > K", "j236S[r] > S", "j236S[r] > H", "Darkness Anthem Followup", "DAF"],
        "214S[r]": ["214Sr", "Last Edguy", "DP", "LE"],
        "j.214S[r]": ["j214S[r]", "j214Sr", "j214S raou", "j.214Sr", "j.214S raou", "Air Last Edguy", "Air LE", "Air DP"], 
        "214D": ["Etiquette Starts Here", "ESH", "Etiquette"],
        "632146H": ["Birth!!", "Birth"],
        "632146S[r]": ["632146Sr", "632146S raou", "Bellows Malice", "BM"],
        "236236H": ["I'm Scared...", "I'm Scared", "Im scared", "Im Scared...", "IS", "IK", "Instant Kill"]
    },
    "i-no": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"], 
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "66": ["Dash"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "41236S": ["Stroke the Big Tree", "STBT", "Stroke the Big Tree S", "STBT S"],
        "41236H": ["Stroke the Big Tree H", "STBT H"],
        "214P/H": ["214P", "214H", "Antidepressant Scale", "AS"],
        "j.214P/H": ["j.214P", "j.214H", "j214P", "j214H", "j214P/H", "Air Antidepressant Scale", "Air AS"],
        "j.236P/[P]": ["j.236P", "j236P", "j.236[P]", "j236[P]", "Sultry Performance P", "SP P", "Sultry Performance", "SP"],
        "j.236K/[K]": ["j.236K", "j236K", "j.236[K]", "j236[K]", "Sultry Performance K", "SP K"],
        "j.236S/[S]": ["j.236S", "j236S", "j.236[S]", "j236[S]", "Sultry Performance S", "SP S"],
        "j.236H/[H]": ["j.236H", "j236H", "j.236[H]", "j236[H]", "Sultry Performance H", "SP H"],
        "632146K": ["Chemical Love (Horizontal)", "Chemical Love Horizontal", "CL Horizontal"],
        "j.632146K": ["Air Chemical Love (Horizontal)", "Air Chemical Love Horizontal", "Air CL Horizontal", "j632146K"],
        "632146S": ["Chemical Love (Vertical)", "Chemical Love Vertical", "CL Vertical"],
        "j.632146S": ["Air Chemical Love (Vertical)", "Air Chemical Love Vertical", "Air CL Vertical", "j632146S"],
        "214D": ["FB Antidepressant Scale", "FB AS", "Force Break Antidepressant Scale", "Force Break AS"],
        "j.214D": ["FB Air Antidepressant Scale", "FB Air AS", "Force Break Air Antidepressant Scale", "Force Break Air AS", "j214D"],
        "j.236D": ["j236D", "FB Sultry Performance", "FB SP", "Force Break Sultry Performance", "Force Break SP"],
        "j.236D > X": ["j236D > X", "j236D > P", "j236D > K", "j236D > S", "j236D > H", "j236D > D", "j.236D > P", "j.236D > K", "j.236D > S", "j.236D > H", "j.236D > D", "FB Sultry Performance Followup", "FB SP Followup", "Force Break Sultry Performance Followup", "Force Break SP Followup"],
        "632146H": ["Longing Desperation", "Desperation", "LD"],
        "j.2363214S": ["Ultimate Fortissimo", "UF", "j2363214S"],
        "236236H": ["Last Will and Testament", "LWAT", "Testament", "Instant Kill", "IK"]
    },
    "anji mito": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "5S": ["slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"], 
        "3P": ["Diagonal Punch"],
        "6K": ["Forward Kick"],
        "3K": ["Diagonal Kick"],
        "6S": ["Forward Slash"],
        "3S": ["Diagonal Slash"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "236P": ["Shitsu", "Shih Tzu"],
        "236S": ["Fuujin S", "Fuujin"],
        "236S/H > P": ["236S > P", "236H > P", "Shin: Ichishiki", "Shin Ichishiki", "Ichishiki", "SH"],
        "236S/H > K": ["236S > K", "236H > K", "Issokutobi"],
        "236S/H > S": ["236S > S", "236H > S", "Nagiha"],
        "236S/H > H": ["236S > H", "236H > H", "Rin"],
        "P During Autoguard": ["Kou"],
        "K During Autoguard": ["Sou"],
        "623H": ["On"],
        "214P": ["Kai P", "Kai"],
        "214K": ["Kai K"],
        "j.214P": ["j214P", "Shin: Nishiki", "Shin Nishiki", "Nishiki", "SN"],
        "236D": ["FB Shitsu", "FB Shih Tzu", "Force Break Shitsu", "Force Break Shih Tzu"],
        "236S/H > D": ["236S > D", "236H > D", "FB Rin", "Force Break Rin"],
        "D During Autoguard": ["FB Kou", "Force Break Kou"],
        "623D": ["FB On", "Force Break On"],
        "632146H": ["Issei Ougi: Sai", "Issei Ougi Sai", "Sai", "IOS"],
        "[2]8K": ["Tenjinkyaku"],
        "63214S During Autoguard": ["Kachoufuugetsu", "63214S"],
        "236236H": ["IK", "Zetsu", "Instant Kill"],
    },
    "sol badguy": {
        "5K DI": ["5K Dragon Install"],
        "6H DI": ["6H Dragon Install"],
        "j.H": ["jh"],
        "j.H DI": ["jh di", "j.h dragon install", "jh dragon install"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "236P": ["Gun Flame", "GF"],
        "623S": ["Volcanic Viper S", "VV S"],
        "623H": ["Volcanic Viper H", "VV H"],
        "623S DI": ["Volcanic Viper S Dragon Install", "VV S Dragon Install", "Volcanic Viper S DI", "VV S DI"],
        "623H DI": ["Volcanic Viper H Dragon Install", "VV H Dragon Install", "Volcanic Viper H DI", "VV H DI"],
        "j.623S": ["Air Volcanic Viper S", "Air VV S", "j623S"],
        "j.623H": ["Air Volcanic Viper H", "Air VV H", "j623H"],
        "j.623S/H DI": ["Air Volcanic Viper DI", "Air VV DI", "Air Volcanic Viper Dragon Install", "Air VV Dragon Install", "j623S/H", "j623S DI", "j623H DI", "j.623S DI", "j.623H DI", "j623S Dragon Install", "j623H Dragon Install", "j.623S Dragon Install", "j.623H Dragon Install"],
        "j.236H": ["j236H", "Sidewinder"],
        "623S/H > 214K": ["Knockdown", "623S > 214K", "623H > 214K"],
        "236K": ["Bandit Revolver", "BR"],
        "j.236K": ["j236K", "Air Bandit Revolver", "Air BR"],
        "236K DI": ["Bandit Revolver DI", "BR DI", "Bandit Revolver Dragon Install", "BR Dragon Install", "236K Dragon Install"],
        "j.236K DI": ["j236K DI", "j.236K Dragon Install", "Air Bandit Revolver DI", "Air BR DI", "j236K Dragon Install", "j.236K Dragon Install" "Air Bandit Revolver Dragon Install", "Air BR Dragon Install"],
        "236[K]": ["Bandit Bringer", "BB"],
        "214K": ["Riot Stamp", "RS"],
        "j.214K": ["Slam", "j214K"],
        "214S": ["Ground Viper", "GV"],
        "41236H/41236D > 64D": ["Tyrant Rave", "Rave", "TR", "41236H > 64D", "41236D > 64D"],
        "j.236D": ["j236D", "FB Sidewinder", "Force Break Sidewinder"],
        "214214S": ["Dragon Install", "DI"],
        "214214214214P + H": ["Dragon Install 2nd", "DI 2nd", "Dragon Install Second", "DI Second", "Dragon Install 2", "DI 2"],
    },
    "dizzy": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"], 
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.2S": ["Jumping Down Slash", "j2s"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "66": ["Dash"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "236H": ["I Use This to Fish H", "Fish H", "IUTTF H", "I Use This to Fish", "Fish", "IUTTF"],
        "236D": ["I Use This to Fish D", "Fish D", "IUTTF D"],
        "214P": ["My Talking Buddies P", "MTB P", "My Talking Buddies", "MTB"],
        "214K": ["My Talking Buddies K", "MTB K"],
        "214S": ["My Talking Buddies S", "MTB S"],
        "214H": ["My Talking Buddies H", "MTB H"],
        "214D": ["My Talking Buddies D", "MTB D"],
        "421S/[S]": ["I Use This to Get Fruit", "IUTTGF", "421S", "421[S]"],
        "236K": ["It Started Out as Just Light K", "ISOAJL K", "It Started Out as Just Light", "ISOAJL"],
        "236S": ["It Started Out as Just Light S", "ISOAJL S"],
        "j.214P/K/S": ["j214P/K/S", "j214P", "j214K", "j214S", "j.214P", "j.214K", "j.214S", "Please Leave Me Alone", "PLMA"],
        "j.214P/K/S Pop": ["j214P/K/S Pop", "j214P Pop", "j214K Pop", "j214S Pop", "j.214P Pop", "j.214K Pop", "j.214S Pop", "Please Leave Me Alone Pop", "PLMA Pop", "Pop"],
        "j.214D": ["j214D", "FB Please Leave Me Alone", "FB PLMA", "Force Break Please Leave Me Alone", "Force Break PLMA"],
        "j.214D Pop": ["j214D Pop", "FB Please Leave Me Alone Pop", "FB PLMA Pop", "Force Break Please Leave Me Alone Pop", "Force Break PLMA Pop", "FB Pop", "Force Break Pop"],
        "421D": ["FB I Use This to Get Fruit", "FB IUTTGF", "Force Break I Use This to Get Fruit", "Force Break IUTTGF"],
        "632146S": ["IR", "Imperial Ray"],
        "632146P": ["Necro Unleashed", "NU", "Necro"],
        "64641236H": ["GR", "Gamma Ray"],
        "[2]8462P + H": ["I Can't... Contain My Strength", "I Can't Contain My Strength", "ICCMYS", "IK", "Instant Kill"]
    },
    "axl low": {
        "5P": ["Standing Punch"],
        "5[P]": ["Standing Punch Hold"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "3P": ["Diagonal Punch"],
        "6K": ["Forward Kick"],
        "6[K]": ["Forward Kick Hold"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2[P]": ["Crouching Punch Hold"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2[S]": ["Crouching Slash Hold"],
        "2H": ["Crouching Heavy"],
        "2[H]": ["Crouching Heavy Hold"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.6P": ["j6P", "Jumping Forward Punch"],
        "j.6[P]": ["j6[P]", "Jumping Forward Punch Hold"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["jS", "Jumping Slash"],
        "j.[S]": ["j[S]", "Jumping Slash Hold"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "j.H": ["Jumping Heavy", "jh"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "623S": ["Benten Gari", "BG", "Benten Gari S", "BG S"],
        "623H": ["Benten Gari H", "BG H"],
        "623H > 623H": ["Followup Axl Bomber", "Axl Bomber Followup", "FAB"],
        "j.63214S Or 623H-623H > 63214S": ["j.63214S", "j63214S", "j63214S Or 623H-623H > 63214S", "623H-623H > 63214S", "Kokuu Geki", "KG"],
        "[4]6S": ["Rensen Geki", "RG"],
        "[4]6S > 8/9": ["Kyokusa Geki", "KG", "[4]6S > 8", "[4]6S > 9"],
        "[4]6S > 2/3": ["Sensa Geki", "SG", "[4]6S > 2", "[4]6S > 3"],
        "[4]6H": ["Rashou Sen", "RS"],
        "[4]6H > P": ["Rashou Sen Feint", "RS Feint"],
        "214P": ["Tenhou Seki P", "TS P", "Tenhou Seki", "TS"],
        "214K": ["Tenhou Seki K", "TS K"],
        "63214S": ["Raiei Sageki S", "RS S", "Raiei Sageki", "RS"],
        "63214H/[H]": ["Raiei Sageki H", "RS H", "63214H", "63214[H]"],
        "j.623H": ["Axl Bomber", "AB", "j623H"],
        "623P > 421D": ["Shiranami No Homura", "SNH"],
        "j.623D": ["j623D", "FB Axl Bomber", "FB AB", "Force Break Axl Bomber", "Force Break AB"],
        "[4]6D": ["FB Kyokusa Geki", "Force Break Kyokusa Geki", "FB KG", "Force break kg"],
        "2363214H": ["Byakue Renshou", "BR"],
        "236236H": ["Rensen Ougi: Midare Gami", "Rensen Ougi Midare Gami", "ROMG", "IK", "Instant Kill"]
    },
    "millia rage": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "j.2H": ["Jumping Down Heavy", "j2h"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "214S > SxN": ["Lust Shaker", "LS"],
        "236S": ["Tandem Top S", "TT S", "Tandem Top", "TT"],
        "236H": ["Tandem Top H", "TT H"],
        "j.236P": ["j236P", "Bad Moon", "bm", "moon"],
        "j.236K": ["j236K", "Turbo Fall", "TF", "Fall"],
        "214K": ["Roll", "Forward Roll", "FR"],
        "214P": ["Iron Savior", "IS", "Slide", "Haircar"],
        "j.214K/S": ["j214K/S", "j214K", "j214S", "j.214K", "j.214S", "Silent Force K/S", "SF K/S", "Silent Force K", "Silent Force S", "SF K", "SF S"],
        "j.214H": ["j214H","j.214H", "Silent Force H", "SF H"],
        "214H > Direction + H": ["Secret Garden", "SG", "214H", "214H > 1 + H", "214H > 1 + H", "214H > 2 + H", "214H > 3 + H", "214H > 4 + H", "214H > 5 + H", "214H > 6 + H", "214H > 7 + H", "214H > 8 + H", "214H > 9 + H"],
        "236D": ["Pretty Maze", "Maze"],
        "214D > Direction + H/D": ["FB Secret Garden", "FB SG", "Force Break Secret Garden", "Force Break SG", "214D", "214D > 1 + H", "214D > 2 + H", "214D > 3 + H", "214D > 4 + H", "214D > 5 + H", "214D > 6 + H", "214D > 7 + H", "214D > 8 + H", "214D > 9 + H", "214D > 1 + D", "214D > 2 + D", "214D > 3 + D", "214D > 4 + D", "214D > 5 + D", "214D > 6 + D", "214D > 7 + D", "214D > 8 + D", "214D > 9 + D"],
        "j.236D": ["Air Pretty Maze", "Air Maze", "j236d"],
        "214D > Direction + H/D": ["FB Secret Garden", "FB SG", "214D", "Force Break Secret Garden", "Force Break SG", "214D > Direction + H", "214D > Direction + D"],
        "2141236H": ["Winger"],
        "j.2141236H": ["Air Winger"],
        "236236S": ["Emerald Rain", "ER", "Emerald Splash"],
        "236236H": ["Iron Maiden", "IM", "Instant Kill", "IK"]
    },
    "chipp zanuff": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6H": ["Forward Heavy"],
        "3H": ["Diagonal Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "j.2K": ["Jumping Down Kick"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "j.46/64": ["j.46", "j.64", "j46", "j64", "Sankaku Tobi", "ST", "Tobi", "Wall Cling"],
        "236P": ["Alpha Blade", "AB"],
        "j.236P": ["Air Alpha Blade", "Air AB", "j236P"],
        "236P > H": ["Alpha Plus", "AP"],
        "623S": ["Beta Blade", "BB", "DP"],
        "j.623S": ["Air Beta Blade", "Air BB", "j623S", "Air BnB", "Air DP"],
        "41236H": ["Gamma Blade", "GB"],
        "22P": ["Tsuyoshi-shiki Ten'i P", "Tsuyoshi shiki Ten'i P", "TSTI P", "Ten'i P"],
        "22K": ["Tsuyoshi-shiki Ten'i K", "Tsuyoshi shiki Ten'i K", "TSTI K", "Ten'i K"],
        "22S": ["Tsuyoshi-shiki Ten'i S", "Tsuyoshi shiki Ten'i S", "TSTI S", "Ten'i S"],
        "22H/D": ["Tsuyoshi-shiki Ten'i H", "Tsuyoshi shiki Ten'i H", "TSTI H", "22H", "22D", "Ten'i H", "Ten'i D", "Tsuyoshi-shiki Ten'i D", "Tsuyoshi shiki Ten'i D", "TSTI D", "Tsuyoshi-shiki Ten'i H/D", "Tsuyoshi shiki Ten'i H/D", "TSTI H/D", "Ten'i H/D"],
        "214K": ["Tsuyoshi-shiki Meisei", "Meisei", "TSM", "Hide And Seek"],
        "41236K": ["Genrou Zan", "GZ"],
        "236S > 236S > 236K or 236S > 236K": ["Senshuu", "GZ", "236S > 236S > 236K", "236S > 236K"],
        "j.214P Slow": ["Shuriken Slow", "j214P Slow", "j.214P", "j214P"],
        "j.214P Fast": ["Shuriken Fast", "j214P Fast"],
        "41236K > D": ["Genrou Zan You", "GZY", "You"],
        "623D": ["FB Beta Blade", "Force Break Beta Blade", "FB BB", "Force Break BB"],
        "j.623D": ["FB Air Beta Blade", "Force Break Air Beta Blade", "FB Air BB", "Force Break Air BB", "j623D"],
        "41236D": ["FB Gamma Blade", "FB GB", "Force Break Gamma Blade", "Force Break GB"],
        "632146H": ["Zansei Rouga", "Rouga", "ZR"],
        "236236K": ["Banki Messai", "BM", "Bankai"],
        "236236H": ["Delta End", "DE", "Instant Kill", "IK"]
    },
    "johnny": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "66": ["Dash"],
        "236[P/K/S]": ["236[P]", "236[K]", "236[S]", "Mist Finer Stance", "MFS", "Misfire"],
        "236[P/K/S] > 66": ["236[P] > 66", "236[K] > 66", "236[S] > 66", "Mist Finer Stance Forwards Dash", "MFSFD"],
        "236[P/K/S] > 44": ["236[P] > 44", "236[K] > 44", "236[S] > 44", "Mist Finer Stance Backwards Dash", "MFSBD"],
        "236[P/K/S] > H": ["236[P] > H", "236[K] > H", "236[S] > H", "Mist Finer Stance Cancel", "MFSC"],
        "236]P[": ["236P", "236P Level 1", "236P Lvl 1", "236P Lvl1", "236P 1" "236]P[ Level 1", "236]P[ Lvl1", "236]P[ 1", "Mist Finer Upper Level 1", "Mist Finer Upper Lvl1", "Mist Finer Upper 1", "Mist Finer: Upper Level 1", "Mist Finer: Upper Lvl1", "Mist Finer: Upper 1", "MFU Level 1", "MFU Lvl1", "MFU 1"],
        "236]P[ Level 2": ["236P Level 2", "236P Lvl 2", "236P Lvl2", "236P 2" "236]P[ Level 2", "236]P[ Lvl2", "236]P[ 2", "Mist Finer Upper Level 2", "Mist Finer Upper Lvl2", "Mist Finer Upper 2", "Mist Finer: Upper Level 2", "Mist Finer: Upper Lvl2", "Mist Finer: Upper 2", "MFU Level 2", "MFU Lvl2", "MFU 2"],
        "236]P[ Level 3": ["236P Level 3", "236P Lvl 3", "236P Lvl3", "236P 3" "236]P[ Level 3", "236]P[ Lvl3", "236]P[ 3", "Mist Finer Upper Level 3", "Mist Finer Upper Lvl3", "Mist Finer Upper 3", "Mist Finer: Upper Level 2", "Mist Finer: Upper Lvl3", "Mist Finer: Upper 3", "MFU Level 3", "MFU Lvl3", "MFU 3"],
        "236]K[": ["236K", "236K Level 1", "236K Lvl 1", "236K Lvl2", "236K 1" "236]K[ Level 1", "236]K[ Lvl1", "236]K[ 1", "Mist Finer Middle Level 1", "Mist Finer Middle Lvl1", "Mist Finer Middle 1", "Mist Finer: Middle Level 1", "Mist Finer: Middle Lvl1", "Mist Finer: Middle 1", "MFM Level 1", "MFM Lvl1", "MFM 1"],
        "236]K[ Level 2": ["236K Level 2", "236K Lvl 2", "236K Lvl2", "236K 2" "236]K[ Level 2", "236]K[ Lvl2", "236]K[ 2", "Mist Finer Middle Level 2", "Mist Finer Middle Lvl2", "Mist Finer Middle 2", "Mist Finer: Middle Level 2", "Mist Finer: Middle Lvl2", "Mist Finer: Middle 2", "MFM Level 2", "MFM Lvl2", "MFM 2"],
        "236]K[ Level 3": ["236K Level 3", "236K Lvl 3", "236K Lvl3", "236K 3" "236]K[ Level 3", "236]K[ Lvl3", "236]K[ 3", "Mist Finer Middle Level 3", "Mist Finer Middle Lvl3", "Mist Finer Middle 3", "Mist Finer: Middle Level 2", "Mist Finer: Middle Lvl3", "Mist Finer: Middle 3", "MFM Level 3", "MFM Lvl3", "MFM 3"],
        "236]S[": ["236S", "236S Level 1", "236S Lvl 1", "236S Lvl2", "236S 1" "236]K[ Level 1", "236]S[ Lvl1 ", "236]S[ 1", "Mist Finer Lower Level 1", "Mist Finer Lower Lvl1", "Mist Finer Lower 1", "Mist Finer: Lower Level 1", "Mist Finer: Lower Lvl1", "Mist Finer: Lower 1", "MFM Lower 1", "MFL Lvl1", "MFL 1"],
        "236]S[ Level 2": ["236S Level 2", "236S Lvl 2", "236S Lvl2", "236S 2" "236]K[ Level 2", "236]S[ Lvl2", "236]S[ 2", "Mist Finer Lower Level 2", "Mist Finer Lower Lvl2", "Mist Finer Lower 2", "Mist Finer: Lower Level 2", "Mist Finer: Lower Lvl2", "Mist Finer: Lower 2", "MFM Lower 2", "MFL Lvl2", "MFL 2"],
        "236]S[ Level 3": ["236S Level 3", "236S Lvl 3", "236S Lvl3", "236S 3" "236]K[ Level 3", "236]S[ Lvl3", "236]S[ 3", "Mist Finer Lower Level 3", "Mist Finer Lower Lvl3", "Mist Finer Lower 3", "Mist Finer: Lower Level 2", "Mist Finer: Lower Lvl3", "Mist Finer: Lower 3", "MFM Lower 3", "MFL Lvl3", "MFL 3"],
        "236H": ["Glitter Is Gold Towards", "GIGT"],
        "214H": ["Glitter Is Gold Up", "GIGU", "Glitter Is Gold", "GIG"],
        "214P": ["Bacchus Sigh", "BS"],
        "623S": ["Divine Blade", "DB"],
        "623S > S": ["Divine Blade Followup", "DB Followup"],
        "j.236S": ["j236S", "Air Divine Blade", "Air DB"],
        "j.41236H": ["Ensenga", "j41236H"],
        "421S": ["Killer Joker", "Joker", "KJ"],
        "421S > S": ["Killer Joker Followup", "Joker Followup", "KJ Followup"],
        "j.214S": ["Air Killer Joker", "Air Joker", "Air KJ", "j214s"],
        "236[P/K/S] > 214D": ["236[P] > 214D", "236[K] > 214D", "236[S] > 214D", "Stance Jackhound", "StaJ"],
        "236[P/K/S] > 66 > 214D": ["236[P] > 66 > 214D", "236[K] > 66 > 214D", "236[S] > 66 > 214D", "Step Jackhound", "SteJ"],
        "214D > 236D": ["Return Jack", "RJ"],
        "632146H": ["That's My Name", "That my name", "TMN"],
        "j.236236H": ["j236236H", "Uncho's Iai", "Uncho Iai", "UI", "Iai"],
        "236236H": ["Joker Trick", "JT", "Instant Kill", "IK"]
    },
    "may": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "5[D]": ["Dust Hold", "Just Kidding~", "Just Kidding", "JK"],
        "6P": ["Forward Punch"],
        "6[P]": ["Forward Punch Hold"],
        "6H": ["Forward Heavy", "Forward Heavy Level 1", "Forward Heavy Lvl1", "Forward Heavy 1", "6H Level 1", "6H Lvl1", "6H 1"],
        "6H Level 2": ["Forward Heavy Level 2", "Forward Heavy Lvl2", "Forward Heavy 2", "6H Level 2", "6H Lvl2", "6H 2"],
        "6H Level 3": ["Forward Heavy Level 3", "Forward Heavy Lvl3", "Forward Heavy 3", "6H Level 3", "6H Lvl3", "6H 3"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "j.2H": ["j2H", "Jumping Down Heavy"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "[4]6S": ["Mr. Dolphin Horizontal S", "Mr Dolphin Horizontal S", "Dolphin Horizontal S", "MDH S", "Mr. Dolphin Horizontal", "Mr Dolphin Horizontal", "Dolphin Horizontal", "MDH"], 
        "[4]6H": ["Mr. Dolphin Horizontal H", "Mr Dolphin Horizontal H", "Dolphin Horizontal H", "MDH H"], 
        "[2]8S": ["Mr. Dolphin Vertical S", "Mr Dolphin Vertical S", "Dolphin Vertical S", "MDV S", "Mr. Dolphin Vertical", "Mr Dolphin Vertical", "Dolphin Vertical", "MDV"], 
        "[2]8H": ["Mr. Dolphin Vertical H", "Mr Dolphin Vertical H", "Dolphin Vertical H", "MDV H"], 
        "623S": ["Restive Rolling S", "RR S", "Rolling S", "Restive Rolling", "RR", "Rolling"],
        "623H": ["Restive Rolling H", "RR H", "Rolling H"],
        "j.623S": ["Air Restive Rolling S", "Air RR S", "Air Rolling S", "j623S", "Air Restive Rolling", "Air RR", "Air Rolling"],
        "j.623H": ["Air Restive Rolling H", "Air RR H", "Air Rolling H", "j623H"],
        "623H > H": ["Restive Rolling H Extension", "RR H Extension", "Rolling H Extension", "Restive Rolling Extension", "Rolling Extension"],
        "41236[X]": ["Applause For The Victim", "AFTV", "Hoops", "41236[P]", "41236[K]", "41236[S]", "41236[H]", "41236[D]"],
        "41236]X[": ["Applause for the Victim Release", "AFTV Release", "Victim Release", "Hoops Release", "41236]P[", "41236]K[", "41236]S[", "41236]H[", "41236]D[", "41236P", "41236K", "41236S", "41236H", "41236D", "41236X"],
        "63214K": ["Overhead Kiss", "OK"],
        "[4]6S > 56D": ["Go, Mr. Dolphin! Horizontal S", "Go, Mr. Dolphin Horizontal S", "Go Mr Dolphin Horizontal S", "Go, Mr. Dolphin Horizontal S", "GMDHS"],
        "[4]6H > 56D": ["Go, Mr. Dolphin! Horizontal H", "Go, Mr. Dolphin Horizontal H", "Go Mr Dolphin Horizontal H", "Go, Mr. Dolphin Horizontal H", "GMDHH"],
        "[2]8S/H > 58D": ["Go, Mr. Dolphin! Vertical", "Go, Mr. Dolphin Vertical", "Go Mr Dolphin Vertical", "Go, Mr. Dolphin Vertical", "GMDV", "[2]8S > 58D", "[2]8H > 58D"],
        "236236S": ["Great Yamada Attack", "Yamada", "Big Whale"],
        "63214S": ["Super Screaming Ultimate Spinning Whirlwind", "Whirlwind", "SSUSW"],
        "63214S > P": ["Deluxe Goshogawara Bomber", "Bomber", "DGB"],
        "4123641236H": ["May and the Jolly Crew", "MATJC", "Instant Kill", "IK"]
    },
    "venom": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "6K": ["Forward Kick"],
        "6H": ["Forward Heavy"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "4/6[t]H": ["Ground Throw", "4H", "6[t]H", "GT", "4/6H"],
        "j.4/6H": ["Air Throw", "j.4H", "j.6H", "j4H", "j6H", "j4/6H", "AT"],
        "6X + X While Blocking": ["Dead Angle Attack", "DAA"],
        "214X": ["Summoning Ball", "Summon Ball", "SB", "214P", "214K", "214S", "214H", "214D"],
        "j.214X": ["Air Summoning Ball", "Air Summon Ball", "Air SB", "j.214P", "j.214K", "j.214S", "j.214H", "j.214D", "j214P", "j214K", "j214S", "j214H", "j214D", "j214X"],
        "[4]6S": ["Stinger Aim S", "Stinger S", "SA S", "Stinger Aim", "Stinger", "SA"],
        "[4]6H": ["Stinger Aim H", "Stinger H", "SA H"],
        "[4]6[S]": ["Enhanced Stinger Aim S", "Enhanced Stinger S", "ESA S", "Enhanced Stinger Aim", "Enhanced Stinger", "ESA"],
        "[4]6[H]": ["Enhanced Stinger Aim H", "Enhanced Stinger H", "ESA H"],
        "[2]8S": ["Carcass Raid S", "Carcass S", "CR S", "Carcass Raid", "Carcass", "CR"],
        "[2]8H": ["Carcass Raid H", "Carcass H", "CR H"],
        "[2]8[S]": ["Enhanced Carcass Raid S", "Enhanced Carcass S", "ECR S", "Enhanced Carcass Raid", "Enhanced Carcass", "ECR"],
        "[2]8[H]": ["Enhanced Carcass Raid H", "Enhanced Carcass H", "ECR H"],
        "[2]8S/H > P or [4]6S/H > P": ["[2]8S/H > P", "[4]6S/H > P", "[2]8S > P", "[2]8H > P", "[4]6S > P", "[4]6H > P", "Feint"],
        "421X": ["Dubious Curve", "DC", "Curve", "421P", "421K", "421S", "421H", "421D"],
        "623H": ["Double Head Morbid H", "DHM H"],
        "j.236S": ["j236S", "Mad Struggle S", "MS S", "Struggle S", "Mad Struggle", "MS", "Struggle"],
        "j.236H": ["j236H", "Mad Struggle H", "MS H", "Struggle H"],
        "623K": ["Teleport"],
        "214X Hit Ball": ["Active Balls Hit", "Hit Ball", "HB"],
        "214X Lightning Ball": ["Lightning Ball", "LB"],
        "[4]6D": ["FB Stinger Aim", "FB Stinger", "FB SA", "Force Break Stinger Aim", "Force Break Stinger", "Force Break SA"],
        "[4]6[D]": ["FB Enhanced Stinger Aim", "FB Enhanced Stinger", "FB ESA", "Force Break Enhanced Stinger Aim", "Force Break Enhanced Stinger", "Force Break ESA"],
        "[2]8D": ["FB Carcass Raid", "FB Carcass", "FB CR", "Force Break Carcass Raid", "Force Break Carcass", "Force Break CR"],
        "[2]8[D]": ["FB Enhanced Carcass Raid", "FB Enhanced Carcass", "FB ECR", "Force Break Enhanced Carcass Raid", "Force Break Enhanced Carcass", "Force Break ECR"],
        "623D": ["FB Double Head Morbid", "Force Break Double Head Morbid", "FB DHM", "Force Break DHM"],
        "j.236D": ["FB Mad Struggle", "FB MS", "j236D", "Force Break Mad Struggle", "Force Break MS"],
        "2141236S": ["Dark Angel", "DA"],
        "j.236236H": ["Red Hail", "Hail", "RH", "j236236H"],
        "632146X": ["Tactical Arch", "TA", "Arch", "632146P", "632146K", "632146S", "632146H", "632146D"],
        "236236H": ["Dimmu Borgir", "DB", "Instant Kill", "IK"]
    },
    "eddie": {
        "5P": ["Standing Punch"],
        "5K": ["Standing Kick"],
        "c.S": ["cs", "Close Slash"],
        "f.S": ["fs", "Far Slash"],
        "5H": ["Standing Heavy"],
        "5D": ["Dust"],
        "6P": ["Forward Punch"],
        "2P": ["Crouching Punch"],
        "2K": ["Crouching Kick"],
        "2S": ["Crouching Slash"],
        "2H": ["Crouching Heavy"],
        "2d": ["sweep", "crouching dust"],
        "j.P": ["Jumping Punch", "jp"],
        "j.K": ["Jumping Kick", "jk"],
        "j.S": ["Jumping Slash", "js"],
        "j.H": ["Jumping Heavy", "jh"],
        "jd": ["jd", "j.d", "j.D", "Jumping Dust"],
        "7/8/9 Airborne": ["7 Airborne", "8 Airborne", "9 Airborne", "Flight"],
        "22S": ["Invite Hell S", "IH S"],
        "22H": ["Invite Hell H", "IH H"],
        "214[K]": ["Break the Law", "BTL"],
        "214[K] > 41236S": ["Break the Law Followup", "BTL Followup"],
        "j.41236S": ["Shadow Gallery", "SG"],
        "236P/K/S/H[s] or 214H[s]": ["236P[s]", "236K[s]", "236S[s]", "236H[s]", "236D[s]", "214H[s]", "Summon Eddie", "Summon"],
        "236P/K/S/H[us] or 214H[us]": ["236P[us]", "236K[us]", "236S[us]", "236H[us]", "236D[us]", "214H[us]", "Unsummon Eddie", "Unsummon"],
        "236P or ]P[ Normal Shadow": ["236P", "]P[ Normal Shadow", "Small Attack", "SA"],
        "]D[ Normal Shadow": ["Overhead Attack", "OA", "Overhead"],
        "214P": ["Traversing"],
        "]H[ Vice Shadow": ["Drill Special Vice", "DSV"],
        "22D": ["Drill Special", "DS"],
        "236D": ["Exhaustion", "Exhaust"],
        "632146H": ["Amorphous"],
        "j.236236S/[S]": ["Executor-X" "Executor", "Executor X", "j.236236S", "j.236236[S]", "j236236S", "j236236[S]"],
        "236236H": ["Black In Mind", "BIM", "Instant Kill", "IK"]
    }
}

frame_override_table = {
    "robo-ky": {
        "63214k": {"startup": "7", "active": "1", "recovery": "37"},
        "2d": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "jd": {"startup": "8", "active": "24", "recovery": "12", "land": "8"},
        "[P + K]": [
            {
                "label": "Face Up",
                "startup": "-1",
                "active": "-1",
                "recovery": "82"
            },
            {
                "label": "Face Down",
                "startup": "-1",
                "active": "-1",
                "recovery": "80"
            }
        ],
        "Overheat Explosion": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236S": {"startup": "24", "active": "N/A", "recovery": "58"},
        "236S level 2": {"startup": "24", "active": "N/A", "recovery": "58"},
        "236S level 3": {"startup": "24", "active": "N/A", "recovery": "58"},
        "214s": {"startup": "21", "active": "12", "recovery": "7", "land": "4"},
        "214S level 2": {"startup": "13", "active": "19", "recovery": "7", "land": "6"},
        "214S level 3": {"startup": "11", "active": "24", "recovery": "7", "land": "3"},
        "623H": {"startup": "9", "active": "3", "recovery": "38", "land": "8"},
        "623H level 2": {"startup": "3", "active": "2(4)3", "recovery": "35", "land": "8"},
        "623H level 3": {"startup": "3", "active": "4(6)4", "recovery": "29", "land": "8"},
        "j.623H": {"startup": "9", "active": "3", "recovery": "0", "land": "8"},
        "j.623H level 2": {"startup": "3", "active": "2(4)3", "recovery": "0", "land": "8"},
        "j.623H level 3": {"startup": "3", "active": "4(6)4", "recovery": "0", "land": "8"},
        "j.236S": {"startup": "11", "active": "N/A", "recovery": "48", "land": "14"},
        "j.236S level 2": {"startup": "7", "active": "N/A", "recovery": "32", "land": "14"},
        "j.236S level 3": {"startup": "9", "active": "N/A", "recovery": "40", "land": "14"},
        "j.214D": {"startup": "0", "active": "-1", "recovery": "68", "land": "0"},
        "236236S > S x N": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236236S > 236S": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Automatic After 623H": {"startup": "13", "active": "12(15)20", "recovery": "26", "land": "10"},
        "236236P": {"startup": "10 + 12", "active": "-1", "recovery": "0"},
        "236236P Explosion": {"startup": "1", "active": "81", "recovery": "53"},
    },
    "ky kiske": {
        "jd": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236S": {"startup": "10", "active": "N/A", "recovery": "42"},
        "236H": {"startup": "10", "active": "N/A", "recovery": "53"},
        "j.236S": {"startup": "15", "active": "N/A", "recovery": "60", "land": "14"},
        "j.236H": {"startup": "13", "active": "N/A", "recovery": "57", "land": "14"},
        "236D": {"startup": "43", "active": "N/A", "recovery": "69"},
        "214K": {"startup": "18", "active": "15", "recovery": "5", "land": "11"},
        "j.236D": {"startup": "31", "active": "N/A", "recovery": "64", "land": "14"},
        "623S": {"startup": "9", "active": "3", "recovery": "32", "land": "13"},
        "623H": {"startup": "11", "active": "4", "recovery": "30", "land": "13"},
        "j.623S/H": {"startup": "11", "active": "3", "recovery": "0", "land": "13"},
        "j.214D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.632146H": {"startup": "8", "active": "42", "recovery": "0", "land": "8"},
    },
    "faust": {
        "j.2K": {"startup": "10", "active": "1", "recovery": "0", "land": "6"},
        "jd": {"startup": "12", "active": "11", "recovery": "21", "land": "4"},
        "41236K > 4": {"startup": "0", "active": "-1", "recovery": "56"},
        "236P > 236P": {"startup": "0", "active": "-1", "recovery": "39"},
        "j.236P": {"startup": "21", "active": "N/A", "recovery": "50", "land": "5"},
        "236P": {"startup": "13", "active": "N/A", "recovery": "24"},
        "Pogo 9": {"startup": "0", "active": "-1", "recovery": "19"},
        "Pogo H": {"startup": "9", "active": "32", "recovery": "23", "land": "3"},
        "Pogo D": {"startup": "9", "active": "N/A", "recovery": "18"},
        "214S": {"startup": "47", "active": "20", "recovery": "26", "land": "6"},
        "4 > 236D > 236D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "214S": {"startup": "47", "active": "20", "recovery": "26", "land": "6"},
        "j.236D": {"startup": "14", "active": "1", "recovery": "1"},
        "236P Donut": [
            {
                "label": "Regular",
                "startup": "53",
                "active": "216",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "53",
                "active": "216",
                "recovery": "0"
            }
        ],
        "236P Chocolate": [
            {
                "label": "Regular",
                "startup": "53",
                "active": "216",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "53",
                "active": "216",
                "recovery": "0"
            }
        ],
        "236P Chikuwa": [
            {
                "label": "Regular",
                "startup": "53",
                "active": "216",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "53",
                "active": "216",
                "recovery": "0"
            }
        ],
        "236P Hammer": [
            {
                "label": "Regular",
                "startup": "13",
                "active": "43",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "9",
                "active": "45",
                "recovery": "0"
            }
        ],
        "236P Dumbbell": {"startup": "13", "active": "40", "recovery": "0"},
        "236P Washpan": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236P Coin": [
            {
                "label": "Regular",
                "startup": "13",
                "active": "169",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "9",
                "active": "171",
                "recovery": "0"
            }
        ],
        "236P Bomb": [
            {
                "label": "Regular",
                "startup": "134",
                "active": "12",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "132",
                "active": "12",
                "recovery": "0"
            }
        ],
        "236P Meteors": [
            {
                "label": "Regular",
                "startup": "196",
                "active": "-1",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "192",
                "active": "-1",
                "recovery": "0"
            }
        ],
        "236P Poison": [
            {
                "label": "Regular",
                "startup": "89",
                "active": "50",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "86",
                "active": "50",
                "recovery": "0"
            }
        ],
        "236P Chibi Faust": [
            {
                "label": "Regular",
                "startup": "39",
                "active": "-1",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "35",
                "active": "-1",
                "recovery": "0"
            }
        ],
        "236P Chibi Faust": [
            {
                "label": "Regular",
                "startup": "39",
                "active": "-1",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "35",
                "active": "-1",
                "recovery": "0"
            }
        ],
        "236P Chibi Robo-Ky": [
            {
                "label": "Regular",
                "startup": "39",
                "active": "-1",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "35",
                "active": "-1",
                "recovery": "0"
            }
        ],
        "236P Chibi Potemkin": [
            {
                "label": "Regular",
                "startup": "13",
                "active": "-1",
                "recovery": "0"
            },
            {
                "label": "Pogo",
                "startup": "9",
                "active": "-1",
                "recovery": "0"
            }
        ],
        "236236P": {"startup": "7", "active": "N/A", "recovery": "41"},
    },
    "potemkin": {
        "jd": {"startup": "11", "active": "1", "recovery": "0", "land": "8"},
        "[4]6H": [
            {
                "label": "Earliest Hammerfall",
                "startup": "19",
                "active": "2",
                "recovery": "27"
            },
            {
                "label": "Latest Hammerfall",
                "startup": "27",
                "active": "2",
                "recovery": "35"
            }
        ],
        "j.632146D": {"startup": "5", "active": "1", "recovery": "0", "land": "12"},
        "63214S Reflect": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236P": {"startup": "25", "active": "8", "recovery": "0", "land": "13"},
        "214P": {"startup": "25", "active": "9", "recovery": "0", "land": "6"},
        "[4]6H > P": {"startup": "0", "active": "-1", "recovery": "16"},
        "63214D": {"startup": "28", "active": "6", "recovery": "28"},
        "632146H": {"startup": "17", "active": "N/A", "recovery": "42"},
    }, 
    "order-sol": {
        "jd": {"startup": "13", "active": "4", "recovery": "7", "land": "5"},
        "214[D]": {"startup": "14", "active": "-1", "recovery": "0"},
        "Special > D": {"startup": "0", "active": "-1", "recovery": "31"},
        "Special > j.D": {"startup": "0", "active": "-1", "recovery": "31", "land": "8"},
        "236P": [
            {
                "label": "BHB1",
                "startup": "12",
                "active": "2",
                "recovery": "29"
            },
            {
                "label": "Projectile",
                "startup": "14",
                "active": "8",
                "recovery": "0"
            }
        ],
        "236P Level 2": [
            {
                "label": "BHB2",
                "startup": "12",
                "active": "2",
                "recovery": "29"
            },
            {
                "label": "Projectile",
                "startup": "14",
                "active": "12",
                "recovery": "0"
            }
        ],
        "236P Level 3": [
            {
                "label": "BHB3",
                "startup": "12",
                "active": "2",
                "recovery": "29"
            },
            {
                "label": "Projectile",
                "startup": "14",
                "active": "12(8)12(8)12",
                "recovery": "0"
            }
        ],
        "214S": {"startup": "23", "active": "1", "recovery": "21"},
        "214S Level 2": {"startup": "23", "active": "1(15)1", "recovery": "11"},
        "214S Level 3": {"startup": "17", "active": "1(15)1(17)1", "recovery": "2"},
        "623H": {"startup": "12", "active": "11", "recovery": "22", "land": "8"},
        "j.623H": {"startup": "8", "active": "11", "recovery": "0", "land": "8"},
        "623H level 2": {"startup": "10", "active": "11(3)3", "recovery": "22", "land": "8"},
        "j.623H level 2": {"startup": "8", "active": "11(3)3", "recovery": "0", "land": "8"},
        "623H level 3": {"startup": "8", "active": "11(3)3(22)7", "recovery": "4", "land": "8"},
        "j.623H level 3": {"startup": "8", "active": "11(3)3(22)7", "recovery": "0", "land": "8"},
        "236K": {"startup": "22", "active": "3", "recovery": "6", "land": "6"},
        "j.236K": {"startup": "19", "active": "3", "recovery": "0", "land": "8"},
        "236K level 2": {"startup": "20", "active": "3(9)3", "recovery": "9", "land": "4"},
        "j.236K level 2": {"startup": "19", "active": "3(9)3", "recovery": "0", "land": "8"},
        "236K level 3": {"startup": "18", "active": "3(8)4", "recovery": "8", "land": "2"},
        "j.236K level 3": {"startup": "19", "active": "3(8)4", "recovery": "0", "land": "8"},
        "632146H Level 2": {"startup": "13", "active": "13(16)16", "recovery": "16"},
        "632146H Level 3": {"startup": "13", "active": "13(16)16(10)22", "recovery": "26"},
        "632146P": [
            {
                "label": "SF1",
                "startup": "5",
                "active": "-1",
                "recovery": "34"
            },
            {
                "label": "Projectile",
                "startup": "5",
                "active": "6",
                "recovery": "0"
            }
        ],
        "632146P Level 2": [
            {
                "label": "SF2",
                "startup": "3",
                "active": "-1",
                "recovery": "32"
            },
            {
                "label": "Projectile",
                "startup": "3",
                "active": "2(4)6(4)6",
                "recovery": "0"
            }
        ],
        "632146P Level 3": [
            {
                "label": "SF3",
                "startup": "4",
                "active": "-1",
                "recovery": "38"
            },
            {
                "label": "Projectile",
                "startup": "4",
                "active": "11",
                "recovery": "0"
            }
        ],
    }, 
    "justice": {
        "jd": {"startup": "11", "active": "2", "recovery": "18", "land": "3"},
        "j.41236S": {"startup": "10", "active": "9", "recovery": "26"},
        "j.41236H": {"startup": "21", "active": "9", "recovery": "25"},
        "623K": {"startup": "7", "active": "12", "recovery": "36"},
        "22[X] > ]X[": {"startup": "7", "active": "N/A", "recovery": "52"},
        "46463214H": {"startup": "11", "active": "3(71)104", "recovery": "36"},
        "46463214S": {"startup": "0", "active": "-1", "recovery": "6"},
    },
    "baiken": {
        "j.H": {"startup": "15", "active": "1", "recovery": "0"},
        "jd": {"startup": "9", "active": "3", "recovery": "21", "land": "6"},
        "j.623S": {"startup": "6", "active": "12", "recovery": "15", "land": "11"},
        "63214K": {"startup": "0", "active": "-1", "recovery": "31"},
        "412K": {"startup": "0", "active": "-1", "recovery": "35"},
        "412H": {"startup": "19", "active": "2", "recovery": "14", "land": "10"},
        "236D": {"startup": "14", "active": "16", "recovery": "18"},
        "j.236K": {"startup": "18", "active": "N/A", "recovery": "0", "land": "16"},
    },
    "jam kuradoberi": {
        "3H": {"startup": "5", "active": "2(2)4", "recovery": "15", "land": "8"},
        "jd": {"startup": "7", "active": "3(4)6", "recovery": "16"},
        "22K/S/H":  {"startup": "54", "active": "-1", "recovery": "1"},
        "236K":  {"startup": "17", "active": "6", "recovery": "25", "land": "11"},
        "j.236K":  {"startup": "9", "active": "6", "recovery": "0", "land": "11"},
        "236D":  {"startup": "11", "active": "16", "recovery": "0", "land": "15"},
        "214K":  {"startup": "19", "active": "13", "recovery": "3", "land": "10"},
        "j.214K":  {"startup": "9", "active": "13", "recovery": "0", "land": "10"},
        "214D":  {"startup": "12", "active": "26", "recovery": "0", "land": "12"},
        "623K":  {"startup": "7", "active": "23", "recovery": "0", "land": "6"},
        "j.623K":  {"startup": "4", "active": "21", "recovery": "0", "land": "6"},
        "623D":  {"startup": "3", "active": "26", "recovery": "0", "land": "5"},
        "236S":  {"startup": "6", "active": "19", "recovery": "22"},
        "236S > P":  {"startup": "0", "active": "-1", "recovery": "27"},
        "236S > H Crossup":  {"startup": "29", "active": "3", "recovery": "15"},
        "236P or 236S > 236P":  {"startup": "0", "active": "-1", "recovery": "42", "land": "2"},
        "j.236P":  {"startup": "0", "active": "-1", "recovery": "0", "land": "2"},
        "j.2 + K":  {"startup": "10", "active": "1", "recovery": "0", "land": "6"},
        "22D": {"startup": "20", "active": "-1", "recovery": "32"},
        "236236H": {"startup": "3", "active": "3(2)3", "recovery": "36"},
    },
    "kliff undersn": {
        "6P Level 2": {"startup": "22", "active": "7", "recovery": "28"},
        "6H Level 2": {"startup": "40", "active": "9", "recovery": "63"},
        "2H Level 2": {"startup": "36", "active": "4", "recovery": "18"},
        "jd":  {"startup": "25", "active": "1", "recovery": "0", "land": "14"},
        "66":  {"startup": "0", "active": "-1", "recovery": "35"},
        "T":  {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "214S":  {"startup": "10", "active": "24", "recovery": "25"},
        "j.214S":  {"startup": "9", "active": "24", "recovery": "0", "land": "6"},
        "214K":  {"startup": "28", "active": "8", "recovery": "4", "land": "8"},
        "623H > H x N":  {"startup": "7", "active": "291", "recovery": "22"},
        "214P": {"startup": "0", "active": "-1", "recovery": "49"},
        "j.41236S": {"startup": "14", "active": "12", "recovery": "26"},
        "j.236D": {"startup": "8", "active": "N/A", "recovery": "26"},
        "632146H/[H]": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
    },
    "a.b.a": {
        "j.H": {"startup": "15", "active": "1", "recovery": "0"},
        "jd": {"startup": "16", "active": "4", "recovery": "13", "land": "5"},
        "6P[m]": {"startup": "10", "active": "6", "recovery": "17"},
        "6P[gm]": {"startup": "7", "active": "5", "recovery": "12"},
        "6H[m]": {"startup": "15", "active": "14", "recovery": "30"},
        "6H[gm]": {"startup": "11", "active": "14", "recovery": "24"},
        "2H[m]": {"startup": "17", "active": "14", "recovery": "6"},
        "2H[gm]": {"startup": "17", "active": "14", "recovery": "6"},
        "j.D[m]": {"startup": "13", "active": "4", "recovery": "13", "land": "5"},
        "j.D[gm]": {"startup": "7", "active": "4", "recovery": "10", "land": "5"},
        "D + X": {"startup": "17", "active": "6", "recovery": "24", "land": "3"},
        "63214H": {"startup": "13", "active": "12", "recovery": "30"},
        "j.63214H": {"startup": "10", "active": "3", "recovery": "0"},
        "236P": {"startup": "0", "active": "-1", "recovery": "29"},
        "236H": {"startup": "35", "active": "N/A", "recovery": "41"},
        "63214P": {"startup": "0", "active": "-1", "recovery": "39"},
        "63214H[m]": {"startup": "13", "active": "12", "recovery": "30"},
        "j.63214H[m]": {"startup": "10", "active": "3", "recovery": "0"},
        "j.41236S": {"startup": "16", "active": "6(5)", "recovery": "0", "land": "12"},
        "j.41236S[gm]": {"startup": "12", "active": "6(5)", "recovery": "0", "land": "12"},
        "63214P[m]": {"startup": "0", "active": "-1", "recovery": "41"},
        "Moroha Gauge Reaches 0": {"startup": "0", "active": "-1", "recovery": "53"},
        "236D": {"startup": "0", "active": "-1", "recovery": "27"},
        "236D[m]/[gm]": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.632146P": {"startup": "12", "active": "24", "recovery": "0", "land": "11"},
        "j.632146P[m]": {"startup": "12", "active": "24", "recovery": "0", "land": "11"},
        "j.632146P > 214K": {"startup": "7", "active": "38", "recovery": "0", "land": "11"},
    },
    "slayer": {
        "6[K]": {"startup": "0", "active": "-1", "recovery": "25", "land": "3"},
        "jd": {"startup": "7", "active": "5", "recovery": "19", "land": "5"},
        "236[P]": {"startup": "0", "active": "-1", "recovery": "24"},
        "236[K]": {"startup": "0", "active": "-1", "recovery": "28"},
        "214P": {"startup": "0", "active": "-1", "recovery": "31"},
        "214K": {"startup": "0", "active": "-1", "recovery": "39"},
        "214S": {"startup": "0", "active": "-1", "recovery": "31"},
        "214H": {"startup": "0", "active": "-1", "recovery": "41"},
        "214D": {"startup": "0", "active": "-1", "recovery": "31"},
        "214P/K/S/D/H > K": {"startup": "6", "active": "4(9)7", "recovery": "16", "land": "5"},
        "j.214K": {"startup": "5", "active": "2(12)", "recovery": "0", "land": "11"},
        "632146S": {"startup": "8", "active": "10", "recovery": "31", "land": "21"},
        "236236H": {"startup": "7", "active": "18", "recovery": "36", "land": "7"},
        "j.214214S": {"startup": "9", "active": "6", "recovery": "0", "land": "20"},
    },
    "testament": {
        "3H": {"startup": "14", "active": "4(2)4", "recovery": "17"},
        "jd": {"startup": "10", "active": "6", "recovery": "20", "land": "5"},
        "236P": {"startup": "30", "active": "-1", "recovery": "30"},
        "236K": {"startup": "31", "active": "-1", "recovery": "18"},
        "Automatic After Curse Feathers": {"startup": "26", "active": "-1", "recovery": "18"},
        "Automatic After Curse Overhead": {"startup": "76", "active": "8", "recovery": "14"},
        "214P": {"startup": "17", "active": "3(6)2", "recovery": "13", "land": "15"},
        "j.214P": {"startup": "12", "active": "3(6)2", "recovery": "0", "land": "12"},
        "41236S": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "41236H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "214K": {"startup": "0", "active": "-1", "recovery": "53"},
        "22P/K": {"startup": "0", "active": "-1", "recovery": "43"},
        "214S": {"startup": "26", "active": "N/A", "recovery": "28"},
        "214S Powered Up": {"startup": "21", "active": "N/A", "recovery": "25"},
        "214H": {"startup": "11", "active": "N/A", "recovery": "30"},
        "j.214H": {"startup": "10", "active": "N/A", "recovery": "29"},
        "214H Powered Up": {"startup": "11", "active": "N/A", "recovery": "30"},
        "j.214H Powered Up": {"startup": "8", "active": "N/A", "recovery": "27"},
        "214D": {"startup": "14", "active": "6", "recovery": "16", "land": "3"},
        "j.214D": {"startup": "12", "active": "6", "recovery": "0", "land": "3"},
        "236D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "632146S": {"startup": "0", "active": "N/A", "recovery": "22"},
    },
    "bridget": {
        "jd": {"startup": "15", "active": "18", "recovery": "16"},
        "8/9/7/6/5/4H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.8/9/7/6/5/4/3/2/1H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > H/[H]": {"startup": "12", "active": "N/A", "recovery": "21"},
        "Air Yo-Yo Set > H/[H]": {"startup": "14", "active": "N/A", "recovery": "23"},
        "236K > K": {"startup": "2", "active": "12", "recovery": "21", "land": "20"},
        "623P": {"startup": "13", "active": "15", "recovery": "25"},
        "j.623P": {"startup": "13", "active": "15", "recovery": "0", "land": "10"},
        "Yo-Yo Set > 236H": {"startup": "28", "active": "N/A", "recovery": "33"},
        "Yo-Yo Set > j.236H": {"startup": "23", "active": "N/A", "recovery": "43"},
        "Yo-Yo Set > 214H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > j.214H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > 623H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > 421H":  {"startup": "19", "active": "1", "recovery": "11"},
        "Yo-Yo Set > j.421H": {"startup": "19", "active": "1", "recovery": "15"},
        "Yo-Yo Set > 421H High": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > j.421H High": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > 236D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > j.236D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > 214D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > j.214D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "4123641236S": {"startup": "4", "active": "N/A", "recovery": "45"},
        "Yo-Yo Set > 632146H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "Yo-Yo Set > 412364H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
    },
    "zappa": {
        "f.S Puddle": {"startup": "1", "active": "0(33)", "recovery": "3"},
        "5H": {"startup": "22", "active": "18", "recovery": "12"},
        "jd": {"startup": "9", "active": "6", "recovery": "18", "land": "5"},
        "D[d]": {"startup": "0", "active": "-1", "recovery": "31"},
        "8D[d]": {"startup": "10", "active": "12", "recovery": "31"},
        "5D[d]": [
            {
                "label": "Initial",
                "startup": "16",
                "active": "8",
                "recovery": "36"
            },
            {
                "label": "Followup",
                "startup": "0",
                "active": "-1",
                "recovery": "61"
            }
        ],
        "6D[d]": [
            {
                "label": "Initial",
                "startup": "17",
                "active": "12",
                "recovery": "17"
            },
            {
                "label": "Followup",
                "startup": "0",
                "active": "-1",
                "recovery": "0",
                "land": "25"
            }
        ],
        "2D[d]": [
            {
                "label": "Initial",
                "startup": "36",
                "active": "4",
                "recovery": "27"
            },
            {
                "label": "Followup",
                "startup": "0",
                "active": "-1",
                "recovery": "52",
            }
        ],
        "4D[d]": [
            {
                "label": "Initial",
                "startup": "0",
                "active": "-1",
                "recovery": "60"
            },
            {
                "label": "Followup",
                "startup": "0",
                "active": "-1",
                "recovery": "0",
                "land": "25"
            }
        ],
        "4DD[d]": [
            {
                "label": "Initial",
                "startup": "13",
                "active": "1",
                "recovery": "40"
            },
            {
                "label": "Followup",
                "startup": "0",
                "active": "-1",
                "recovery": "0",
                "land": "25"
            }
        ],
        "236P[t]": {"startup": "15", "active": "N/A", "recovery": "40"},
        "236K/S/H[t]": {"startup": "9", "active": "N/A", "recovery": "40"},
        "236D[t]": {"startup": "11", "active": "N/A", "recovery": "53"},
        "Automatic While Haunting Banana": {"startup": "0", "active": "99", "recovery": "0"},
        "Automatic While Haunting Golf Ball": {"startup": "39", "active": "-1", "recovery": "0"},
        "Automatic While Haunting Potted Plant": {"startup": "1", "active": "29", "recovery": "0"},
        "214P[t]": {"startup": "0", "active": "-1", "recovery": "33"},
        "6H[s]": {"startup": "13", "active": "30", "recovery": "2"},
        "2H[s]": {"startup": "7", "active": "22", "recovery": "9"},
        "j.236H[s]": {"startup": "12", "active": "1", "recovery": "0", "land": "23"},
        "236S[r] > P/K/S/H or j.236S[r] > P/K/S/H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.214S[r]": {"startup": "4", "active": "12", "recovery": "0", "land": "3"},
        "632146S[r]": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
    },
    "i-no": {
        "jd": {"startup": "16", "active": "5", "recovery": "20", "land": "8"},
        "66": {"startup": "0", "active": "-1", "recovery": "10"},
        "214P/H": {"startup": "19", "active": "N/A", "recovery": "51"},
        "j.214P/H": {"startup": "13", "active": "N/A", "recovery": "0", "land": "6"},
        "j.236P/[P]": {"startup": "13", "active": "1", "recovery": "0", "land": "16"},
        "j.236K/[K]": {"startup": "13", "active": "1", "recovery": "0", "land": "12"},
        "j.236S/[S]": {"startup": "13", "active": "1", "recovery": "0", "land": "14"},
        "j.236H/[H]": {"startup": "10", "active": "32", "recovery": "0", "land": "10"},
        "632146K": {"startup": "11", "active": "11", "recovery": "12", "land": "8"},
        "j.632146K": {"startup": "11", "active": "11", "recovery": "22", "land": "8"},
        "632146S": {"startup": "11", "active": "11", "recovery": "11", "land": "13"},
        "j.632146S": {"startup": "11", "active": "11", "recovery": "20", "land": "13"},
        "214D": {"startup": "15", "active": "N/A", "recovery": "43"},
        "j.214D": {"startup": "13", "active": "N/A", "recovery": "0", "land": "6"},
        "j.236D > X": {"startup": "0", "active": "-1", "recovery": "1"},
        "j.2363214S": {"startup": "7", "active": "9", "recovery": "0"},
    },
    "anji mito": {
        "jd": {"startup": "10", "active": "6", "recovery": "14", "land": "6"},
        "236P": {"startup": "21", "active": "N/A", "recovery": "49"},
        "236S/H > P": {"startup": "36", "active": "N/A", "recovery": "51", "land": "8"},
        "236S/H > K": {"startup": "0", "active": "-1", "recovery": "25", "land": "6"},
        "P During Autoguard": {"startup": "4", "active": "38", "recovery": "11", "land": "8"},
        "K During Autoguard": {"startup": "11", "active": "11(4)5", "recovery": "14"},
        "623H": {"startup": "11", "active": "18", "recovery": "20", "land": "6"},
        "214K": {"startup": "32", "active": "10", "recovery": "0", "land": "8"},
        "236D": {"startup": "21", "active": "N/A", "recovery": "51"},
        "D During Autoguard": {"startup": "4", "active": "26(24)4", "recovery": "24"},
        "623D": {"startup": "21", "active": "18", "recovery": "35", "land": "6"},
        "632146H": {"startup": "10", "active": "56", "recovery": "63"},
        "[2]8K": {"startup": "18", "active": "10", "recovery": "0", "land": "20"},
        "63214S During Autoguard": {"startup": "7", "active": "5(16)5(12)5(20)5", "recovery": "75"},
        "236236H": {"startup": "22", "active": "-1", "recovery": "0"},
    },
    "sol badguy": {
        "5K": {"startup": "3", "active": "8", "recovery": "13"},
        "5K DI": {"startup": "2", "active": "5", "recovery": "7"},
        "6H": {"startup": "13", "active": "6", "recovery": "30"},
        "6H DI": {"startup": "8", "active": "6", "recovery": "16"},
        "j.H": {"startup": "9", "active": "14", "recovery": "0"},
        "j.H DI": {"startup": "8", "active": "8", "recovery": "0"},
        "jd": {"startup": "9", "active": "7", "recovery": "10", "land": "5"},
        "236P": {"startup": "21", "active": "N/A", "recovery": "51"},
        "623S": {"startup": "7", "active": "3(3)11", "recovery": "21", "land": "10"},
        "623H": {"startup": "5", "active": "2(3)18", "recovery": "29", "land": "10"},
        "623S DI": {"startup": "7", "active": "3(1)6", "recovery": "21", "land": "10"},
        "623H DI": {"startup": "7", "active": "57", "recovery": "36", "land": "10"},
        "j.623S": {"startup": "5", "active": "2(3)9", "recovery": "0", "land": "10"},
        "j.623H": {"startup": "5", "active": "2(3)18", "recovery": "0", "land": "10"},
        "j.623S/H DI": {"startup": "7", "active": "3(3)8", "recovery": "0", "land": "10"},
        "j.236H": {"startup": "9", "active": "4", "recovery": "0", "land": "13"},
        "623S/H > 214K": {"startup": "12", "active": "4", "recovery": "0", "land": "10"},
        "236K": {"startup": "9", "active": "5(11)9", "recovery": "2", "land": "7"},
        "j.236K": {"startup": "6", "active": "3(14)6", "recovery": "0", "land": "12"},
        "236K DI": {"startup": "7", "active": "9(9)9", "recovery": "3", "land": "7"},
        "j.236K DI": {"startup": "6", "active": "3(14)6", "recovery": "0", "land": "12"},
        "236[K]": {"startup": "32", "active": "6", "recovery": "9", "land": "4"},
        "214K": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.214K": {"startup": "17", "active": "12", "recovery": "0", "land": "10"},
        "214S": {"startup": "17", "active": "25(20)3", "recovery": "37"},
        "j.236D": {"startup": "9", "active": "4", "recovery": "0", "land": "13"},
        "214214S": {"startup": "21", "active": "-1", "recovery": "1"},
        "214214214214P + H": {"startup": "128", "active": "-1", "recovery": "1"},
    },
    "dizzy": {
        "f.S": {"startup": "8", "active": "14", "recovery": "12"},
        "6H": {"startup": "18", "active": "12", "recovery": "21"},
        "jd": {"startup": "10", "active": "12", "recovery": "15", "land": "5"},
        "214P": [
            {
                "label": "Start",
                "startup": "68",
                "active": "3(32)3",
                "recovery": "12"
            },
            {
                "label": "Fish",
                "startup": "35",
                "active": "-1",
                "recovery": "3",
            }
        ],
        "214K": [
            {
                "label": "Start",
                "startup": "60",
                "active": "15",
                "recovery": "0"
            },
            {
                "label": "Fish",
                "startup": "27",
                "active": "-1",
                "recovery": "11",
            }
        ],
        "214S": [
            {
                "label": "Start",
                "startup": "77",
                "active": "35",
                "recovery": "19"
            },
            {
                "label": "Fish",
                "startup": "42",
                "active": "-1",
                "recovery": "1",
            }
        ],
        "214H": [
            {
                "label": "Start",
                "startup": "77",
                "active": "35",
                "recovery": "19"
            },
            {
                "label": "Fish",
                "startup": "27",
                "active": "-1",
                "recovery": "11",
            }
        ],
        "214D": [
            {
                "label": "Start",
                "startup": "77",
                "active": "3",
                "recovery": "24"
            },
            {
                "label": "Fish",
                "startup": "27",
                "active": "-1",
                "recovery": "11",
            }
        ],
        "421S/[S]": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236K": {"startup": "32", "active": "N/A", "recovery": "52"},
        "236S": {"startup": "32", "active": "N/A", "recovery": "55"},
        "j.214P/K/S": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.214P/K/S Pop": {"startup": "13", "active": "4", "recovery": "0"},
        "j.214D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.214D Pop": {"startup": "13", "active": "6", "recovery": "0"},
        "421D": {"startup": "31", "active": "N/A", "recovery": "48"},
        "632146S": {"startup": "7", "active": "N/A", "recovery": "42"},
        "64641236H": {"startup": "23", "active": "6(24)6(51)46", "recovery": "0"},
    },
    "axl low": {
        "5P": {"startup": "9", "active": "5(2)6", "recovery": "10"},
        "6K": {"startup": "13", "active": "5(2)8", "recovery": "19"},
        "6H": {"startup": "23", "active": "9", "recovery": "0", "land": "9"},
        "2P": {"startup": "12", "active": "5(2)8", "recovery": "10"},
        "2S": {"startup": "8", "active": "15", "recovery": "12"},
        "2H": {"startup": "11", "active": "14", "recovery": "16"},
        "j.6P": {"startup": "7", "active": "6(2)3", "recovery": "14"},
        "j.6[P]": {"startup": "7", "active": "7", "recovery": "18"},
        "j.S": {"startup": "11", "active": "5(2)9", "recovery": "9"},
        "jd": {"startup": "10", "active": "6", "recovery": "18", "land": "5"},
        "623H > 623H": {"startup": "14", "active": "4", "recovery": "45", "land": "10"},
        "j.63214S Or 623H-623H > 63214S": {"startup": "7", "active": "19", "recovery": "0", "land": "12"},
        "[4]6S": {"startup": "12", "active": "12", "recovery": "39"},
        "[4]6S > 2/3": {"startup": "7", "active": "2(5)2(5)2(5)2(5)2", "recovery": "17"},
        "[4]6H > P": {"startup": "0", "active": "-1", "recovery": "13"},
        "214P": {"startup": "0", "active": "-1", "recovery": "32"},
        "214K": {"startup": "0", "active": "-1", "recovery": "32"},
        "63214S": {"startup": "28", "active": "4", "recovery": "13", "land": "6"},
        "63214H/[H]": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.623H": {"startup": "17", "active": "1", "recovery": "0", "land": "18"},
        "623P > 421D": {"startup": "7", "active": "18(13)4", "recovery": "37"},
        "2363214H": {"startup": "15", "active": "8(19)13", "recovery": "41"},
    },
    "millia rage": {
        "c.S": {"startup": "7", "active": "6", "recovery": "17"},
        "6P": {"startup": "7", "active": "12", "recovery": "20"},
        "jd": {"startup": "17", "active": "7", "recovery": "9", "land": "6"},
        "214S > SxN": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.236P": {"startup": "11", "active": "1", "recovery": "0", "land": "22"},
        "j.236K": {"startup": "0", "active": "-1", "recovery": "0", "land": "13"},
        "214K": {"startup": "0", "active": "-1", "recovery": "25"},
        "214P": {"startup": "17", "active": "1", "recovery": "18", "land": "8"},
        "j.214K/S": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.214H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "214H > Direction + H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.236D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "214D > Direction + H/D": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "2141236H": {"startup": "6", "active": "10(10)15", "recovery": "0", "land": "30"},
        "j.2141236H": {"startup": "7", "active": "1", "recovery": "0", "land": "30"},
        "236236S": {"startup": "6", "active": "N/A", "recovery": "76"},
        "236236H": {"startup": "34", "active": "N/A", "recovery": "166"},
    },
    "chipp zanuff": {
        "6K": {"startup": "19", "active": "7", "recovery": "3", "land": "3"},
        "j.K": {"startup": "5", "active": "8", "recovery": "8"},
        "jd": {"startup": "6", "active": "8", "recovery": "18", "land": "5"},
        "236P": {"startup": "18", "active": "15", "recovery": "0", "land": "34"},
        "j.236P": {"startup": "14", "active": "14", "recovery": "0", "land": "21"},
        "623S": {"startup": "5", "active": "22", "recovery": "17", "land": "10"},
        "j.623S": {"startup": "3", "active": "18", "recovery": "0", "land": "8"},
        "22P": {"startup": "0", "active": "-1", "recovery": "26"},
        "22K": {"startup": "0", "active": "-1", "recovery": "31"},
        "22S": {"startup": "0", "active": "-1", "recovery": "32"},
        "22H/D": {"startup": "0", "active": "-1", "recovery": "21"},
        "214K": {"startup": "0", "active": "-1", "recovery": "30"},
        "41236K": {"startup": "29", "active": "12", "recovery": "0", "land": "10"},
        "236S > 236S > 236K or 236S > 236K": {"startup": "25", "active": "6", "recovery": "10", "land": "12"},
        "j.214P Slow": {"startup": "23", "active": "N/A", "recovery": "0", "land": "6"},
        "j.214P Fast": {"startup": "8", "active": "N/A", "recovery": "23", "land": "3"},
        "41236K > D": {"startup": "1", "active": "10", "recovery": "29", "land": "3"},
        "623D": {"startup": "4", "active": "13(7)13", "recovery": "30", "land": "5"},
        "j.623D": {"startup": "2", "active": "13(7)13", "recovery": "0", "land": "5"},
        "632146H": {"startup": "25", "active": "-1", "recovery": "0", "land": "32"},
        "236236K": {"startup": "3", "active": "2(5)4(1)1(4)2(7)2(6)2(5)4(7)2(9)4(4)1(3)1(6)2(11)1(2)1(3)4(4)2(6)1(6)4(5)3(4)21(3)13(7)13", "recovery": "47", "land": "10"},
        "236236H": {"startup": "59", "active": "119", "recovery": "43", "land": "16"},
    },
    "johnny": {
        "jd": {"startup": "8", "active": "7", "recovery": "14", "land": "5"},
        "66": {"startup": "0", "active": "-1", "recovery": "23"},
        "236[P/K/S]": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "236[P/K/S] > 66": {"startup": "0", "active": "-1", "recovery": "15"},
        "236[P/K/S] > 44": {"startup": "0", "active": "-1", "recovery": "15"},
        "236[P/K/S] > H": {"startup": "0", "active": "-1", "recovery": "4"},
        "236]P[ Level 3": {"startup": "8", "active": "4(3)4(3)4(3)3(4)4(3)3(4)4(3)3(4)4", "recovery": "20"},
        "236]K[ Level 3": {"startup": "8", "active": "3(4)4(4)2(4)3(5)2(4)3(4)3(5)2", "recovery": "25"},
        "236]S[ Level 3": {"startup": "9", "active": "2(5)2(5)2(5)2(5)2(5)2(4)3(4)3(5)2", "recovery": "27"},
        "236H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "214H": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "214P": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.41236H": {"startup": "9", "active": "2(2)3", "recovery": "0", "land": "16"},
        "623S": {"startup": "0", "active": "-1", "recovery": "36", "land": "5"},
        "623S > S": {"startup": "12", "active": "10", "recovery": "0", "land": "7"},
        "j.236S": {"startup": "13", "active": "10", "recovery": "0", "land": "13"},
        "421S": {"startup": "N/A", "active": "-1", "recovery": "30", "land": "5"},
        "421S > S": {"startup": "18", "active": "3", "recovery": "0", "land": "14"},
        "j.214S": {"startup": "9", "active": "3", "recovery": "0", "land": "13"},
        "j.236236H": {"startup": "8", "active": "3", "recovery": "0", "land": "24"},
    },
    "may": {
        "j.2H": {"startup": "13", "active": "1", "recovery": "0"},
        "jd": {"startup": "10", "active": "12", "recovery": "24", "land": "5"},
        "236236S": {"startup": "9", "active": "N/A", "recovery": "75"},
        "623S": {"startup": "13", "active": "40", "recovery": "22", "land": "15"},
        "623H": {"startup": "13", "active": "40", "recovery": "24", "land": "15"},
        "j.623S": {"startup": "10", "active": "40", "recovery": "0", "land": "15"},
        "j.623H": {"startup": "16", "active": "40", "recovery": "0", "land": "15"},
        "623H > H": {"startup": "5", "active": "24", "recovery": "0", "land": "15"},
        "41236]X[": {"startup": "49", "active": "N/A", "recovery": "0"},
        "[4]6S > 56D": {"startup": "1", "active": "17", "recovery": "0", "land": "11"},
        "[4]6H > 56D": {"startup": "1", "active": "20", "recovery": "0", "land": "14"},
        "[2]8S/H > 58D": {"startup": "1", "active": "N/A", "recovery": "17"},
        "63214S": {"startup": "15", "active": "2(12)2(12)2(12)2(12)2(12)2(12)2(12)2(12)2(12)", "recovery": "15"},
    },
    "venom": {
        "c.S": {"startup": "5", "active": "11", "recovery": "20"},
        "2H": {"startup": "7", "active": "9", "recovery": "21"},
        "jd": {"startup": "7", "active": "8", "recovery": "13", "land": "6"},
        "214X": {"startup": "11", "active": "-1", "recovery": "17"},
        "j.214X": {"startup": "9", "active": "-1", "recovery": "28"},
        "[4]6S": {"startup": "13", "active": "N/A", "recovery": "38"},
        "[4]6H": {"startup": "9", "active": "N/A", "recovery": "49"},
        "[4]6[S]": {"startup": "6", "active": "N/A", "recovery": "30"},
        "[4]6[H]": {"startup": "5", "active": "N/A", "recovery": "44"},
        "[2]8S": {"startup": "16", "active": "N/A", "recovery": "35"},
        "[2]8H": {"startup": "13", "active": "N/A", "recovery": "49"},
        "[2]8[S]": {"startup": "9", "active": "N/A", "recovery": "27"},
        "[2]8[H]": {"startup": "6", "active": "N/A", "recovery": "41"},
        "[2]8S/H > P or [4]6S/H > P": {"startup": "0", "active": "-1", "recovery": "0", "land": "6"},
        "623H": {"startup": "15", "active": "24", "recovery": "18"},
        "j.236S": {"startup": "18", "active": "1", "recovery": "0", "land": "6"},
        "j.236H": {"startup": "18", "active": "1(5)10", "recovery": "20"},
        "623K": {"startup": "16", "active": "0(5)", "recovery": "2"},
        "214X Hit Ball": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "214X Lightning Ball": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "[4]6D": {"startup": "9", "active": "N/A", "recovery": "39"},
        "[4]6[D]": {"startup": "5", "active": "N/A", "recovery": "40"},
        "[2]8D": {"startup": "13", "active": "N/A", "recovery": "33"},
        "[2]8[D]": {"startup": "6", "active": "N/A", "recovery": "32"},
        "623D": {"startup": "15", "active": "26", "recovery": "22"},
        "2141236S": {"startup": "25", "active": "N/A", "recovery": "36"},
        "j.236236H": {"startup": "10", "active": "N/A", "recovery": "32", "land": "9"},
        "632146X": {"startup": "12", "active": "-1", "recovery": "19"},
    },
    "eddie": {
        "f.S": {"startup": "6", "active": "11", "recovery": "20"},
        "5H": {"startup": "13", "active": "11", "recovery": "15"},
        "6P": {"startup": "13", "active": "8", "recovery": "12"},
        "jd": {"startup": "11", "active": "4", "recovery": "19", "land": "5"},
        "7/8/9 Airborne": {"startup": "0", "active": "-1", "recovery": "92"},
        "22S": {"startup": "18", "active": "N/A", "recovery": "43"},
        "22H": {"startup": "18", "active": "N/A", "recovery": "43"},
        "214[K]": {"startup": "0", "active": "-1", "recovery": "168"},
        "214[K] > 41236S": {"startup": "10", "active": "3", "recovery": "22", "land": "5"},
        "236P/K/S/H[s] or 214H[s]": {"startup": "0", "active": "-1", "recovery": "39"},
        "236P/K/S/H[us] or 214H[us]": {"startup": "0", "active": "-1", "recovery": "30"},
        "]D[ Normal Shadow": {"startup": "28", "active": "N/A", "recovery": "38"},
        "214P": {"startup": "0", "active": "-1", "recovery": "19"},
        "]H[ Vice Shadow": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "22D": {"startup": "20", "active": "N/A", "recovery": "63"},
        "236D": {"startup": "0", "active": "-1", "recovery": "49"},
        "632146H": {"startup": "16", "active": "9", "recovery": "28"}, 
        "j.236236S/[S]": {"startup": "N/A", "active": "N/A", "recovery": "N/A"},
        "j.41236S": {"startup": "7", "active": "6(12)3", "recovery": "24", "land": "7"},
    }
}

def get_move_data(character, move):
    try:
        character = character.lower()
        move_upper = move.upper().strip()  
    
        with open(f"char_data/{character}/move.txt", "r") as f:
            moves = json.load(f)
        matched_moves = []

        for r in moves:
            move_input = r.get("input", "").upper()
            move_name = r.get("move", "").upper()
            full_move_name = f"{move_input} {move_name}".strip()

            if (move_input == move_upper or 
                move_name == move_upper or 
                full_move_name == move_upper):
                matched_moves.append(FormattedMoveData(
                    r.get("input", "N/A"),
                    r.get("move", "N/A"),
                    r.get("damage", "N/A"),
                    r.get("guard", "N/A"),
                    r.get("invincibility", "N/A"),
                    r.get("startup", "N/A"),
                    r.get("block", "N/A"),
                    r.get("active", "N/A"),
                    r.get("recovery", "N/A"),
                    r.get("frc_window", "N/A"),
                    r.get("proration", "N/A"),
                    r.get("guard_bar_plus", "N/A"),
                    r.get("guard_bar_minus", "N/A"),
                    r.get("level", "N/A"),
                    r.get("images", r.get("image", ["N/A"])),
                    r.get("hitboxes_images", r.get("hitboxes_image", ["N/A"])),
                    r.get("meter_images", r.get("meter_image", ["N/A"]))
                ))

            elif (move_input.replace(".", "") == move_upper.replace(".", "") or
                  move_name.replace(".", "") == move_upper.replace(".", "") or
                  full_move_name.replace(".", "") == move_upper.replace(".", "")):
                matched_moves.append(FormattedMoveData(
                    r.get("input", "N/A"),
                    r.get("move", "N/A"),
                    r.get("damage", "N/A"),
                    r.get("guard", "N/A"),
                    r.get("invincibility", "N/A"),
                    r.get("startup", "N/A"),
                    r.get("block", "N/A"),
                    r.get("active", "N/A"),
                    r.get("recovery", "N/A"),
                    r.get("frc_window", "N/A"),
                    r.get("proration", "N/A"),
                    r.get("guard_bar_plus", "N/A"),
                    r.get("guard_bar_minus", "N/A"),
                    r.get("level", "N/A"),
                    r.get("images", r.get("image", ["N/A"])),
                    r.get("hitboxes_images", r.get("hitboxes_image", ["N/A"])),
                    r.get("meter_images", r.get("meter_image", ["N/A"]))
                ))
        return matched_moves if matched_moves else None
    except Exception as e:
        print(f"Error loading move data: {e}")
        return None

def get_move_list_data(character):
    try:
        with open(f"char_data/{character.lower()}/move.txt", "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading movelist: {e}")
        return None

def get_character_info(character):
    try:
        with open(f"char_data/{character.lower()}/info.txt", "r") as f:
            return json.load(f)[0]
    except Exception as e:
        print(f"Error loading character info: {e}")
        return None

def parse_active_sequence(active_str: str) -> str:
    meter = ""
    num = ""
    in_paren = False

    for char in active_str:
        if char.isdigit():
            num += char
        elif char == '(':
            if num:
                meter += "🔴" * int(num)
                num = ""
            in_paren = True
        elif char == ')':
            if num:
                meter += "⬛" * int(num)
                num = ""
            in_paren = False
        else:
            if num:
                if in_paren:
                    meter += "⬛" * int(num)
                else:
                    meter += "🔴" * int(num)
                num = ""

    if num:
        meter += "⬛" * int(num) if in_paren else "🔴" * int(num)

    return meter
        
def generate_frame_meter(startup: str, active: str, recovery: str, character: str = "", move: str = "") -> str:
    try:
        char_key = character.lower()
        move_key = move 
        
        land_recovery = 0
        results = []

        if char_key in frame_override_table:

            for override_move, override_data in frame_override_table[char_key].items():
                if override_move.lower() == move_key.lower():
                    variations = override_data if isinstance(override_data, list) else [override_data]
                    
                    for variation in variations:
                        s = variation.get("startup", "N/A")
                        a = variation.get("active", "N/A")
                        r = variation.get("recovery", "N/A")
                        land = int(variation.get("land", 0))
                        label = variation.get("label", "Frame Meter")
                        
                        if all(val == "N/A" for val in [s, a, r]):
                            return "No frame data available"
                            
                        if s == "N/A" or r == "N/A":
                            continue

                        try:
                            recovery_val = int(r.replace("Total ", "").strip())

                            # Improved startup value handling
                            if "+" in s:
                                parts = [int(p.strip()) for p in s.split("+") if p.strip().isdigit()]
                                startup_val = max(0, sum(parts))
                            else:
                                startup_val = max(0, int(s) - 1)
                            
                            if a in ["N/A", "", None, "0"]:
                                safe_recovery = max(0, recovery_val - startup_val - 1)
                                meter = (
                                    "🟩" * startup_val +
                                    "➖" +
                                    "🔹" * safe_recovery +
                                    "🟪" * land
                                )
                                total = startup_val + safe_recovery + land

                            else:
                                if "(" in a:
                                    active_meter = parse_active_sequence(a)
                                    active_count = active_meter.count("🔴") + active_meter.count("⬛")

                                else:
                                    active_count = int(a)
                                    active_meter = "🔴" * active_count

                                meter = (
                                    "🟩" * startup_val +
                                    active_meter +
                                    "🔹" * recovery_val +
                                    "🟪" * land
                                )
                                total = startup_val + active_count + recovery_val + land

                            if len(variations) > 1:
                                results.append(f"**{label}**\n{meter}\n**Total:** {total}F")
                            else:
                                results.append(f"{meter}\n**Total:** {total}F")
                        except ValueError:
                            continue
                    break  

        if not results:
            if any(val in ["", "N/A", None] for val in [startup, recovery]):
                return "No frame data available"

            try:
                # Handle startup ranges like "19-27" by taking the first value
                if "+" in startup:
                    parts = [int(p.strip()) for p in startup.split("+") if p.strip().isdigit()]
                    startup_val = max(0, sum(parts)) - 1
                else:
                    startup_val = max(0, int(startup.split('-')[0]) - 1)
                
                recovery_val = int(recovery.replace("Total ", "").strip())
                
                if active in ["N/A", "", None, "0"]:
                    safe_recovery = max(0, recovery_val - startup_val - 1)
                    meter = (
                        "🟩" * startup_val +
                        "➖" +
                        "🔹" * safe_recovery +
                        "🟪" * land_recovery
                    )
                    total = startup_val + safe_recovery + land_recovery
                else:
                    if "(" in active:
                        active_meter = parse_active_sequence(active)
                        active_count = active_meter.count("🔴") + active_meter.count("⬛")
                    else:
                        active_count = int(active)
                        active_meter = "🔴" * active_count

                    meter = (
                        "🟩" * startup_val +
                        active_meter +
                        "🔹" * recovery_val +
                        "🟪" * land_recovery
                    )
                    total = startup_val + active_count + recovery_val + land_recovery

                results.append(f"{meter}\n**Total:** {total}F")
            except ValueError as e:
                print(f"ValueError in frame meter generation: {e}")
                return "Invalid frame data"

        return "\n\n".join(results) if results else "No frame data available"

    except Exception as e:
        print(f"Error generating frame meter: {e}")
        return "Invalid frame data."

def char_aliases(character_name: str) -> str:
    characters = {
        "A.B.A": ["aba", "ab", "abba", "paracelsus"],
        "Anji Mito": ["anji", "am", "an"],
        "Axl Low": ["axl", "low", "ax", "al"],
        "Baiken": ["bacon", "samurai", "kenshin", "ba"],
        "Bridget": ["brisket", "br"],
        "Chipp Zanuff": ["chipp", "cz", "zanuff", "ch"],
        "Dizzy": ["necro", "undine", "di"],
        "Eddie": ["zato-1", "zato", "zato one", "eddie", "ed"],
        "Faust": ["baldhead", "dr. baldhead", "doctor baldhead", "doctor", "fa"],
        "I-No": ["ino", "witch", "guitar", "in"],
        "Jam Kuradoberi": ["jam", "kuradoberi", "kenshiro", "ja"],
        "Johnny": ["john", "jo"],
        "Justice": ["aria", "ju"],
        "Kliff Undersn": ["kliff", "undersn", "kl"],
        "Ky Kiske": ["ky", "kyle", "kiske", "kk", "defective orignal"],
        "May": ["dolphin", "ma"],
        "Millia Rage": ["millia", "rage", "mi", "mr"],
        "Order-Sol": ["ordersol", "order sol", "holy order sol", "sol2", "king von", "hos", "or"],
        "Potemkin": ["pot", "po"],
        "Robo-Ky": ["roboky", "robo ky", "robot ky", "robert kyle", "robert", "robo", "robot", "ro"],
        "Slayer": ["dandy", "vampire", "sl"],
        "Sol Badguy": ["sol", "badguy", "fredrick", "so"],
        "Testament": ["testie", "te"],
        "Venom": ["pool", "bakery", "ve"],
        "Zappa": ["S-Ko", "sko", "raoh", "za"]
    }
        
    character_name = character_name.strip().lower()
    character_name_no_spaces = character_name.replace(" ", "")

    for canonical_name, alias_list in characters.items():

        canonical_no_spaces = canonical_name.replace(" ", "").lower()
        if character_name_no_spaces == canonical_no_spaces:
            return canonical_name
        
        for alias in alias_list:
            alias_no_spaces = alias.replace(" ", "").lower()
            if character_name_no_spaces == alias_no_spaces:
                return canonical_name

    return character_name

def move_aliases(character: str, move_name: str) -> str:
    character = character.lower()
    move_name = move_name.strip().lower()

    # Remove spacing
    move_name_no_spaces = move_name.replace(" ", "")

    if character in move_alias_map:
        for canonical, aliases in move_alias_map[character].items():

            # Check without spaces for canonical name
            canonical_no_spaces = canonical.replace(" ", "").lower()
            if move_name_no_spaces == canonical_no_spaces:
                return canonical
            
            # Check all aliases without spaces
            for alias in aliases:
                alias_no_spaces = alias.replace(" ", "").lower()
                if move_name_no_spaces == alias_no_spaces:
                    return canonical
                
    return move_name

# This one is for the frame meter function
def resolve_move_alias(char_key: str, move_name: str) -> str:
    char_key = char_key.lower()
    move_name = move_name.lower().strip()  

    # Remove spacing
    move_name_no_spaces = move_name.replace(" ", "")

    if char_key in move_alias_map:
        for canonical, aliases in move_alias_map[char_key].items():

            # Check without spaces for canonical name
            canonical_no_spaces = canonical.replace(" ", "").lower()
            if move_name_no_spaces == canonical_no_spaces:
                return canonical
            
            # Check all aliases without spaces
            for alias in aliases:
                alias_no_spaces = alias.replace(" ", "").lower()
                if move_name_no_spaces == alias_no_spaces:
                    return canonical
                
    return move_name

def send_email_report(subject: str, body: str):
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_RECIPIENT
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# ========== EVENTS ==========
@bot.event
async def on_ready() -> None:
    print(f'Robo-Data is now running')

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

# ========== SLASH COMMAND LIST ==========

# Commands List
@bot.tree.command(name="commands", description="List all available robo commands.")
async def robo_commands(interaction: discord.Interaction):
    commands = [
        "/commands", "/characters", "/character info", "/movelist", "/frame",
        "/hitboxes", "/meter"
    ]
    embed = Embed(
        title="Command List",
        description="\n".join(commands),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)


# Character List
@bot.tree.command(name="characters", description="List all characters.")
async def robo_chars(interaction: discord.Interaction):
    characters = {
        "A.B.A": ["aba", "ab", "abba", "paracelsus"],
        "Anji Mito": ["anji", "am"],
        "Axl Low": ["axl", "low", "ax"],
        "Baiken": ["bacon", "samurai", "kenshin", "ba"],
        "Bridget": ["brisket", "br"],
        "Chipp Zanuff": ["chipp", "cz", "zanuff", "ch"],
        "Dizzy": ["necro", "undine", "di"],
        "Eddie": ["zato-1", "zato", "zato one", "eddie", "ed"],
        "Faust": ["baldhead", "dr. baldhead", "doctor baldhead", "doctor", "fa"],
        "I-No": ["ino", "witch", "guitar", "fa"],
        "Jam Kuradoberi": ["jam", "kuradoberi", "kenshiro", "ja"],
        "Johnny": ["john", "jo"],
        "Justice": ["aria", "ju"],
        "Kliff Undersn": ["kliff", "undersn", "kl"],
        "Ky Kiske": ["ky", "kyle", "kiske", "kk", "defective orignal"],
        "May": ["dolphin", "ma"],
        "Millia Rage": ["millia", "rage", "mi", "mr"],
        "Order-Sol": ["ordersol", "order sol", "holy order sol", "sol2", "hos", "or"],
        "Potemkin": ["pot", "po"],
        "Robo-Ky": ["roboky", "robo ky", "robot ky", "robert kyle", "robert", "robo", "robot", "ro"],
        "Slayer": ["dandy", "vampire", "sl"],
        "Sol Badguy": ["sol", "badguy", "fredrick", "so"],
        "Testament": ["testie", "te"],
        "Venom": ["pool", "bakery", "ve"],
        "Zappa": ["S-Ko", "sko", "raoh", "za"]
    }

    lines = []
    for char, aliases in characters.items():
        alias_block = ", ".join(f"{name}" for name in aliases)
        lines.append(f"**•** **{char}**\n       → {alias_block}")

    embed = Embed(
        title="Character List",
        description="\n".join(lines),
        color=discord.Color.blue()
    )
    await interaction.response.send_message(embed=embed)

# Character Info
@bot.tree.command(name="info", description="Get detailed info for a character.")
@app_commands.describe(character="Character name")
async def robo_info(interaction: discord.Interaction, character: str):
    char = character.lower()
    char = char_aliases(char)
    bot_msg = get_character_info(char)

    if bot_msg is None:
        await interaction.response.send_message("Not a valid character name.", ephemeral=True)
        return

    display_name = char.replace("-", " ").title()
    wiki_link = f"https://www.dustloop.com/wiki/index.php?title=GGACR/{char.replace(' ', '_')}"

    embed = Embed(
        title=display_name,
        url=wiki_link,
        color=discord.Color.blue()
    )

    embed.add_field(name="Damage Received Mod", value=bot_msg.get("damage_received_mod", "N/A"), inline=True)
    embed.add_field(name="Guts Rating", value=bot_msg.get("guts_rating", "N/A"), inline=True)
    embed.add_field(name="Guard Bar Gain Mod", value=bot_msg.get("guard_bar_gain_mod", "N/A"), inline=True)
    embed.add_field(name="Guard Bar Recovery", value=bot_msg.get("guard_bar_recovery", "N/A"), inline=True)
    embed.add_field(name="Gravity Mod", value=bot_msg.get("gravity_mod", "N/A"), inline=True)
    embed.add_field(name="Stun Resistance", value=bot_msg.get("stun_resistance", "N/A"), inline=True)
    embed.add_field(name="Prejump", value=bot_msg.get("prejump", "N/A"), inline=True)
    embed.add_field(name="Backdash", value=bot_msg.get("backdash", "N/A"), inline=True)

    if bot_msg.get("forwards_dash"):
        embed.add_field(name="Forwards Dash", value=bot_msg["forwards_dash"], inline=True)

    embed.add_field(name="Wakeup Timing", value=bot_msg.get("wakeup_timing", "N/A"), inline=True)
    embed.add_field(name="Jumps", value=bot_msg.get("number_of_jumps", "N/A"), inline=True)
    embed.add_field(name="Air Dashes", value=bot_msg.get("number_of_air_dashes", "N/A"), inline=True)

    if bot_msg.get("unique_movement"):
        embed.add_field(name="Unique Movement", value=bot_msg["unique_movement"], inline=True)

    if "images" in bot_msg and isinstance(bot_msg["images"], list) and bot_msg["images"]:
        embed.set_image(url=bot_msg["images"][0])
        await interaction.response.send_message(embed=embed)

        for image_url in bot_msg["images"][1:]:
            extra_embed = Embed(color=discord.Color.blue())
            extra_embed.set_image(url=image_url)
            await interaction.channel.send(embed=extra_embed)
    else:
        await interaction.response.send_message(embed=embed)

# Character Movelist
@bot.tree.command(name="movelist", description="Get a character's movelist.")
@app_commands.describe(character="Character name")
async def robo_movelist(interaction: discord.Interaction, character: str):
    await interaction.response.defer()  
    char = character.lower()
    char = char_aliases(char)
    move_list = get_move_list_data(char)

    if not move_list:
        await interaction.followup.send("Character not found or has no move data.")
        return

    chunks = [move_list[i:i + 10] for i in range(0, len(move_list), 10)]
    total_pages = len(chunks)
    current_page = 0

    def get_embed(page_index):
        chunk = chunks[page_index]
        display_name = char.replace("-", " ").title()
        wiki_link = f"https://www.dustloop.com/wiki/index.php?title=GGACR/{char.replace(' ', '_')}"

        embed = Embed(
            title=f"{display_name} Move List Page {page_index + 1}/{total_pages}",
            url=wiki_link,
            color=discord.Color.blue()
        )
        
        for move in chunk:
            move_input = move.get("input", "N/A")
            move_name = move.get("move", "N/A")
            embed.add_field(name=f"• {move_input} / {move_name}", value="", inline=False)
        return embed

    message_embed = await interaction.followup.send(embed=get_embed(current_page))
    await message_embed.add_reaction("⬅️")
    await message_embed.add_reaction("➡️")

    def check(reaction, user):
        return (
            user == interaction.user and
            reaction.message.id == message_embed.id and
            str(reaction.emoji) in ["⬅️", "➡️"]
        )

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)
            if str(reaction.emoji) == "➡️":
                current_page = (current_page + 1) % total_pages
            elif str(reaction.emoji) == "⬅️":
                current_page = (current_page - 1) % total_pages

            await message_embed.edit(embed=get_embed(current_page))
            await message_embed.remove_reaction(reaction.emoji, user)
        except asyncio.TimeoutError:
            break


# Frame Data For A Move
@bot.tree.command(name="frame", description="Show frame data for a move.")
@app_commands.describe(character="Character name", move="Move input")
async def robo_frame(interaction: discord.Interaction, character: str, move: str):
    char = character.lower()
    char = char_aliases(char)
    move = move.upper().replace(".", "")
    move_cleaned = move.strip().lower()
    move_resolved = move_aliases(char, move_cleaned)
    bot_msg = get_move_data(char, move_resolved)

    if not bot_msg:
        await interaction.response.send_message("Not a valid input notation or character name.", ephemeral=True)
        return

    bot_msg = bot_msg[0]
    display_name = char.replace("-", " ").title()
    wiki_link = f"https://www.dustloop.com/wiki/index.php?title=GGACR/{char.replace(' ', '_')}"
    valid_images = [url for url in bot_msg.images if url and url != "N/A"]

    def get_frame_embed(index):
        embed = Embed(
            title=f"{display_name} {bot_msg.input} / {bot_msg.move} - Move {index + 1}/{len(valid_images)}",
            url=wiki_link,
            color=discord.Color.blue()
        )
        embed.add_field(name="Damage", value=bot_msg.damage, inline=True)
        embed.add_field(name="Guard", value=bot_msg.guard, inline=True)
        embed.add_field(name="Invincibility", value=bot_msg.invincibility, inline=True)
        embed.add_field(name="Startup", value=bot_msg.startup, inline=True)
        embed.add_field(name="Active", value=bot_msg.active, inline=True)
        embed.add_field(name="Recovery", value=bot_msg.recovery, inline=True)
        embed.add_field(name="Block", value=bot_msg.block, inline=True)
        embed.add_field(name="FRC Window", value=bot_msg.frc_window, inline=True)
        embed.add_field(name="Proration", value=bot_msg.proration, inline=True)
        embed.add_field(name="Guard +", value=bot_msg.guard_bar_plus, inline=True)
        embed.add_field(name="Guard -", value=bot_msg.guard_bar_minus, inline=True)
        embed.add_field(name="Level", value=bot_msg.level, inline=True)

        embed.set_image(url=valid_images[index])
        return embed

    current = 0
    message = await interaction.response.send_message(embed=get_frame_embed(current))
    message = await interaction.original_response()

    if len(valid_images) > 1:
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")


    def check(reaction, user):
        return (
            user == interaction.user and
            str(reaction.emoji) in ["⬅️", "➡️"] and
            reaction.message.id == message.id
        )

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

            if str(reaction.emoji) == "➡️":
                current = (current + 1) % len(valid_images)
            elif str(reaction.emoji) == "⬅️":
                current = (current - 1) % len(valid_images)

            await message.edit(embed=get_frame_embed(current))
            await message.remove_reaction(reaction.emoji, user)
        except asyncio.TimeoutError:
            break

# Hitboxes 
@bot.tree.command(name="hitboxes", description="Show hitboxes for a move.")
@app_commands.describe(character="Character name", move="Move input")
async def robo_hitboxes(interaction: discord.Interaction, character: str, move: str):
    char = character.lower()
    char = char_aliases(char)
    move = move.upper().replace(".", "")
    move_cleaned = move.strip().lower()
    move_resolved = move_aliases(char, move_cleaned)
    bot_msg = get_move_data(char, move_resolved)

    if not bot_msg:
        await interaction.response.send_message("Not a valid input notation or character name.", ephemeral=True)
        return

    bot_msg = bot_msg[0]
    display_name = char.replace("-", " ").title()
    wiki_link = f"https://www.dustloop.com/wiki/index.php?title=GGACR/{char.replace(' ', '_')}"
    valid_hitboxes = [url for url in bot_msg.hitboxes_images if url and url != "N/A"]

    if not valid_hitboxes:
        await interaction.response.send_message("This move has no hitbox.", ephemeral=True)
        return

    # Embed generator
    def get_hitbox_embed(index):
        embed = Embed(
            title=f"{display_name} {bot_msg.input} / {bot_msg.move} - Hitbox {index + 1}/{len(valid_hitboxes)}",
            url=wiki_link,
            color=discord.Color.blue()
        )
        embed.set_image(url=valid_hitboxes[index])
        return embed
    
    current = 0
    message = await interaction.response.send_message(embed=get_hitbox_embed(current))
    message = await interaction.original_response()

    if len(valid_hitboxes) > 1:
        await message.add_reaction("⬅️")
        await message.add_reaction("➡️")

    def check(reaction, user):
        return (
            user == interaction.user and
            str(reaction.emoji) in ["⬅️", "➡️"] and
            reaction.message.id == message.id
        )

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60.0, check=check)

            if str(reaction.emoji) == "➡️":
                current = (current + 1) % len(valid_hitboxes)
            elif str(reaction.emoji) == "⬅️":
                current = (current - 1) % len(valid_hitboxes)

            await message.edit(embed=get_hitbox_embed(current))
            await message.remove_reaction(reaction.emoji, user)
        except asyncio.TimeoutError:
            break

# Move Meter
@bot.tree.command(name="meter", description="Visualize startup, active, and recovery frames.")
@app_commands.describe(character="Character name", move="Move input")
async def robo_meter(interaction: discord.Interaction, character: str, move: str):
    char = character.lower()
    char = char_aliases(char)
    move = move.upper().replace(".", "")
    move_cleaned = move.strip().lower()
    move_resolved = resolve_move_alias(char, move_cleaned)
    bot_msg = get_move_data(char, move_resolved)

    if not bot_msg:
        await interaction.response.send_message("Not a valid input notation or character name.", ephemeral=True)
        return

    bot_msg = bot_msg[0]
    display_name = char.replace("-", " ").title()
    wiki_link = f"https://www.dustloop.com/wiki/index.php?title=GGACR/{char.replace(' ', '_')}"

    embed = Embed(
        title=f"{display_name} {bot_msg.input} / {bot_msg.move}",
        url=wiki_link,
        color=discord.Color.blue()
    )

    embed.add_field(name="Startup", value=bot_msg.startup, inline=True)
    embed.add_field(name="Active", value=bot_msg.active, inline=True)
    embed.add_field(name="Recovery", value=bot_msg.recovery, inline=True)

    frame_meter = generate_frame_meter(bot_msg.startup, bot_msg.active, bot_msg.recovery, char, move_resolved)
    embed.add_field(name="Frame Meter", value=frame_meter, inline=False)

    if bot_msg.images:
        embed.set_image(url=bot_msg.images[0])

    await interaction.response.send_message(embed=embed)

# Report
@bot.tree.command(name="report", description="Submit a bug, feature, or feedback report.")
@app_commands.describe(report_type="Type of report", message="Your report content")
@app_commands.choices(report_type=[
    app_commands.Choice(name="Bug", value="Bug"),
    app_commands.Choice(name="Feature Request", value="Feature Request"),
    app_commands.Choice(name="Other", value="Other"),
])
async def report(interaction: discord.Interaction, report_type: app_commands.Choice[str], message: str):
    user = interaction.user
    subject = f"[{report_type.value}] Report from {user.name}"
    body = f"""
    User: {user.name})
    Type: {report_type.value}
    Report:
    {message}
    """
    success = send_email_report(subject, body)

    if success:
        await interaction.response.send_message("Report sent successfully. Thank you!", ephemeral=True)
    else:
        await interaction.response.send_message("Failed to send report. Please try again later.", ephemeral=True)


# ========== MAIN ==========
def main() -> None:
    bot.run(TOKEN)

if __name__ == '__main__':
    main()