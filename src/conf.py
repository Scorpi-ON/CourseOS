import hashlib

from . import tools


# Absolute constants
WIN_1251 = '1251'  # Encoding for strings
TRIADE_SIZE = 3
HASH_SIZE = hashlib.sha256().digest_size
BITS_IN_BYTE_DEG = 3                    # log2(8)
BITS_IN_BYTE = 1 << BITS_IN_BYTE_DEG    # 8
MAX_BYTE_VALUE = 1 << BITS_IN_BYTE - 1  # 255


# Config
DRIVE_FILENAME = '../Pyth.OS'
SYSTEM_USER_AND_GROUP_ID = 0  # System (ID = 0) is a group for admins
SYSTEM_GROUP_NAME = 'System'  # UserID = 0 means a system itself, but it is not a real user
ADMIN_LOGIN = 'Scorpi-ON'     # UserID = 1 is a real user, the main admin, the only user created with system
ADMIN_PASSWORD_HASH = tools.hash_password('just pass')

FS_TYPE = 'S5FS'
BLOCK_SIZE = 256

INDIRECT_ADDRESSING_BLOCK_NUM = 7
INODE_BLOCK_COUNT = INDIRECT_ADDRESSING_BLOCK_NUM + 1
BLOCK_ADDRESS_FMT = 'H'
BLOCK_ADDRESS_SIZE = tools.calcsize(BLOCK_ADDRESS_FMT)
assert BLOCK_SIZE % BLOCK_ADDRESS_SIZE == 0
INDIRECT_ADDRESSING_BLOCK_COUNT = BLOCK_SIZE // BLOCK_ADDRESS_SIZE
BLOCK_COUNT_TO_STORE_FILE_OF_MAX_SIZE = INODE_BLOCK_COUNT + INDIRECT_ADDRESSING_BLOCK_COUNT

BLOCK_COUNT = BLOCK_COUNT_TO_STORE_FILE_OF_MAX_SIZE * 100
INODE_COUNT = 1000
FREE_BLOCK_COUNT = BLOCK_COUNT
FREE_INODE_COUNT = INODE_COUNT
