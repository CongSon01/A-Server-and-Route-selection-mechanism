# Generic
INIT_MIN_LINK_UTILZATION = 0.3
INIT_MAX_LINK_UTILZATION = 0.7

INIT_MIN_PACKET_LOSS_RATE = 0.05
INIT_MAX_PACKET_LOSS_RATE = 0.3

INIT_MIN_DELAY = 20
INIT_MAX_DELAY = 50

# File Transfer SLAs
FILE_MIN_LINK_UTILZATION = 0.3
FILE_MAX_LINK_UTILZATION = 0.7

FILE_MIN_PACKET_LOSS_RATE = 0.05
FILE_MAX_PACKET_LOSS_RATE = 0.3

FILE_MIN_DELAY = 20
FILE_MAX_DELAY = 50

# Music SLAs
MUSIC_MIN_LINK_UTILZATION = 0.3
MUSIC_MAX_LINK_UTILZATION = 0.7

MUSIC_MIN_PACKET_LOSS_RATE = 0.05
MUSIC_MAX_PACKET_LOSS_RATE = 0.3

MUSIC_MIN_DELAY = 20
MUSIC_MAX_DELAY = 50

# VoIP SLAs
VOIP_MIN_LINK_UTILZATION = 0.3
VOIP_MAX_LINK_UTILZATION = 0.7

VOIP_MIN_PACKET_LOSS_RATE = 0.05
VOIP_MAX_PACKET_LOSS_RATE = 0.3

VOIP_MIN_DELAY = 20
VOIP_MAX_DELAY = 50

# Youtube SLAs
YOUTUBE_MIN_LINK_UTILZATION = 0.3
YOUTUBE_MAX_LINK_UTILZATION = 0.7

YOUTUBE_MIN_PACKET_LOSS_RATE = 0.05
YOUTUBE_MAX_PACKET_LOSS_RATE = 0.3

YOUTUBE_MIN_DELAY = 20
YOUTUBE_MAX_DELAY = 50

##################### ALPHA * PACKET LOSS + BETA * DELAY + GAMMA * LINK UTILIZATION
#### SERVICE 0 - File Transfer
ALPHA_FILE_TRANSFER = 0.3
BETA_FILE_TRANSFER = 0.5
GAMMA_FILE_TRANSFER = 1
#### SERVICE 1 - Music
ALPHA_GOOGLE_MUSIC = 0.3
BETA_GOOGLE_MUSIC = 0.5
GAMMA_GOOGLE_MUSIC = 1
#### SERVICE 2 - VoIP
ALPHA_GOOGLEHANGOUT_VOIP = 0.5
BETA_GOOGLEHANGOUT_VOIP = 0.1
GAMMA_GOOGLEHANGOUT_VOIP = 1
#### SERVICE 3 - Youtube
ALPHA_YOUTUBE = 0.4
BETA_YOUTUBE = 0.25
GAMMA_YOUTUBE = 1


