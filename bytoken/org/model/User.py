from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String)
    email = Column(String)
    mobile = Column(String)
    password = Column(String)
    password = Column(String)
    areaCode = Column("area_code", String)
    faceUrl = Column("face_url", String)
    inviteCode = Column("invite_code", String)
    loginCount = Column("login_count", Integer)
    inviteRelationTime = Column("invite_relation_time", String)
    inviterUserId = Column("inviter_user_id", String)
    lastLoginTime = Column("last_login_time", String)
    LoginIp = Column("login_ip", String)
    loginType = Column("login_type", Integer)
    logoffTime = Column("logoff_time", String)
    myInviteCode = Column("my_invite_code", String)
    regFromCode = Column("reg_from_code", String)
    regIp = Column("reg_ip", String)
    regPlatform = Column("reg_platform", String)
    regReceive = Column("reg_receive", Integer)
    regSource = Column("reg_source", String)
    regTime = Column("reg_time", String)
    userStatus = Column("user_status", Integer)
    userType = Column("user_type", Integer)
    whitelist = Column("whitelist", Integer)
