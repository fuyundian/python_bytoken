from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Date, BigInteger, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'  # 确保与数据库表名一致
    id = Column("id", BigInteger, primary_key=True)
    name = Column("name", String)
    email = Column(String)
    mobile = Column(String)
    password = Column("password", String)
    areaCode = Column("area_code", String)
    faceUrl = Column("face_url", String)
    inviteCode = Column("invite_code", String)
    loginCount = Column("login_count", Integer)
    inviteRelationTime = Column("invite_relation_time", Date)
    inviterUserId = Column("inviter_user_id", String)
    lastLoginTime = Column("last_login_time", Date)
    loginIp = Column("login_ip", String)
    loginType = Column("login_type", Integer)
    # logoffTime = Column("logoff_time", Date)
    myInviteCode = Column("my_invite_code", String)
    regFromCode = Column("reg_from_code", String)
    regIp = Column("reg_ip", String)
    regPlatform = Column("reg_platform", String)
    regReceive = Column("reg_receive", Boolean)
    regSource = Column("reg_source", Integer)
    regTime = Column("reg_time", Date)
    userStatus = Column("user_status", Integer)
    userType = Column("user_type", Integer)
    whitelist = Column("whitelist", Boolean)

    def copy(self):
        pass


class UserLoginParam(BaseModel):
    email: str
    password: str
