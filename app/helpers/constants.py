from enum import Enum


class ERROR_CODE:
    # Admin
    SUCCESS: int = 0
    SERVER_ERROR: int = 1
    FORMAT_ERROR: int = 2
    TOKEN_ERROR: int = 3
    AUTH_ERROR: int = 4
    REQUEST_ERROR: int = 5
    PERMISSION_ERROR: int = 6
    NOTFOUND_ERROR: int = 7
    DUPLICATE_ERROR: int = 8

    TOKEN_EXPIRED: int = 11
    TOKEN_REFRESH: int = 12

    # Document 
    NOT_EXIST: int = 13
    # Upload
    PART_NOT_FOUND: int = 14
    PART_ALREADY_UPLOADED: int = 15
    PART_SIZE_INVALID: int = 17
    UPLOAD_ERROR: int = 18
    UPLOAD_NOT_COMPLETED: int = 19
    FILE_NOT_FOUND: int = 20


class UPLOAD_STATUS():
    DONE: str = "DONE"
    QUEUEING: str = "QUEUEING"
    PROCESSING: str = "PROCESSING"
    UNREGCONIZED: str = "UNREGCONIZED"


class PERMISSIONS(Enum):
    DocumentViewOwn: int = 1
    DocumentViewOther: int = 2
    DocumentUpload: int = 3
    DocumentEditOwn: int = 4
    DocumentEditOther: int = 5
    DocumentDeleteOwn: int = 6
    DoucmentDeleteOther: int = 7
    AccessAll: int = 99
    AccessService: int = 98


class AuthMode(str, Enum):
    LDAP = 'LDAP'
    LEGACY = 'LEGACY'
    OAUTH = 'OAUTH'


class SYSTEM_ROLES(str, Enum):
    ADMIN: str = 'ADMIN'
    SERVICE: str = 'SERVICE'


class UserRole(str, Enum):
    ROLE_USER = "USER"
    ROLE_GUEST = "GUEST"
    ROLE_LEADER = "LEADER"
    ROLE_MANAGER = "MANAGER"
    ROLE_ADMIN = "ADMIN"
    ROLE_AGENCY = "AGENCY"
    ROLE_INDIVIDUAL = "INDIVIDUAL"
    ROLE_ORGANIZATION = "ORGANIZATION"


class NAME_REQUEST(str, Enum):
    SPIN_CONTENT: str = 'Spin Văn bản'
    SEMATIC_SEARCH: str = 'Sematic Search'


class USER_CODE(str, Enum):
    CUSTOMER: str = 'CUSTOMER'
    TEST: str = 'TEST'


class PAYMENT_TYPE(str, Enum):
    CK: str = 'CHUYEN_KHOAN'
    MOMO: str = 'MOMO'
    VNPAY: str = 'VNPAY'
    ZALOPAY: str = 'ZALOPAY'
    PAYPAL: str = 'PAYPAL'


class PAYMENT_STATUS(str, Enum):
    PENDING: str = 'PENDING'
    ACCEPTED: str = 'ACCEPTED'
    CANCELED: str = 'CANCELED'


class CONTRACT_STATUS(str, Enum):
    NOT_SIGNED_CONTRACT: int = 0  # Chưa ký hợp đồng
    SIGNED_CONTRACT: int = 1      # Đã kí hợp đồng
    REMOVE_DEPOSITS: int = 2      # Bỏ cọc giữ phòng
    IN_USE: int = 3               # Đang sử dụng
    EXPRIED: int = 3              # Hết hạn

class ROOM_STATUS(str, Enum):
    VACANT: int = 0      # Còn trống
    WAS_IN: int = 1      # Đã ở

class APARTMENT_STATUS(str, Enum):
    ROOM_AVAILABLE: int = 0         # Còn phòng
    NO_ROOM_AVAILABLE: int = 1      # Hết phòng
    
class MANAGEMENT_EXPENSE_TYPE(str, Enum):
    RENT: int = 0               # Tiền thuê nhà
    ELECTRICITY: int = 1        # Tiền điện
    WATER: int = 2              # Tiền nước
    INTERNET: int = 3           # Tiền mạng
    STAFF_SALARY: int = 4       # Lương nhân viên
    COSTS_INCURRED: int = 5     # Phát sinh khác
    COMMISSION: int = 6         # Hoa hồng lấp khách
    INVESTMENT_COST: int = 7    # Chi phí đầu tư
    
class MANAGEMENT_EXPENSE_TYPE_MONEY(str, Enum):
    REVENUE: int = 0            # Thu
    EXPENSES: int = 1           # Chi

class COSTS_INCURRED_TYPE_MONEY(str, Enum):
    REVENUE: int = 0            # Thu
    EXPENSES: int = 1           # Chi