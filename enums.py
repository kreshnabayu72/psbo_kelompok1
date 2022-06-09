from enum import Enum

class Request_Status(str,Enum):
  Pending="PENDING"
  Accepted="ACCEPTED"
  Declined="DECLINED"
  done="done"
  no="no"