class Error(Exception):
   """Base class for other exceptions"""
   pass

class GroupOrderError(Error):
   """Raised when a group of the wrong order is called"""
   pass

class GroupElementError(Error):
   """Raised when an expected element is not in a group"""
   pass
