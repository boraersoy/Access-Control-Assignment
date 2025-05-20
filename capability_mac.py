from typing import List, Set
from dataclasses import dataclass

class PermissionError(Exception):
    """Base class for permission-related errors."""
    pass

class CapabilityPermissionError(PermissionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class AccessPermissionError(PermissionError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Right:
    READ = "read"
    WRITE = "write"
    OWN = "own"

class Object: # Item
    def __init__(self, name):
        self.name = name
        self.owners = set()

    def get_owners(self):
        return self.owners
    
    def __repr__(self):
        return f"Object(name={self.name}, owners={self.owners})"

class Capability: # Rules
    def __init__(self, object : Object, rights: List[Right]):
        self.obj = object
        self.rights = rights

    def __repr__(self):
        return f"Capability(obj={self.obj.name}, rights={self.rights})"

class Subject: # Person
    def __init__(self, name):
        self.name = name
        self.capabilities : Set = set()

    def __repr__(self):
        return f"Subject(name={self.name}, capabilities={self.capabilities})"

    def validate_rights(self, rights: List[Right]):
        for right in rights:
            if right not in [Right.OWN, Right.READ, Right.WRITE]:
                raise CapabilityPermissionError("Invalid right.")

    def _handle_right(self, rights: List[Right], obj: Object, subject: 'Subject'):
        self.validate_rights(rights)
        if Right.OWN in rights:
            obj.owners.add(subject)
            subject.capabilities.add(Capability(obj, [Right.OWN, Right.READ, Right.WRITE]))
        else:
            subject.capabilities.add(Capability(obj, rights))

    def add_capability(self, subject: 'Subject', obj: Object, rights: List[Right]):
        if self in obj.owners:
            self._handle_right(rights, obj, subject)
            return True
        else:
            raise CapabilityPermissionError("The subject does not have permission to add capabilities to this object.")
        
    def _add_capability(self, subject: 'Subject', obj: Object, rights: List[Right]):
        self._handle_right(rights, obj, subject)
        return True

    def remove_capability(self, subject: 'Subject', obj: Object):
        if self in obj.owners:   
            subject.capabilities = set([cap for cap in subject.capabilities if cap.obj != obj])
            try:
                obj.owners.remove(subject)
            finally:
                return True
        else:
            raise CapabilityPermissionError("The subject does not have permission to remove capabilities from this object.")

    def check_access(self, obj: Object, right: Right):
        capability_set = self.capabilities
        if any(right in cap.rights and cap.obj.name == obj.name for cap in capability_set):
            return True
        else:
            raise AccessPermissionError("The subject does not have the required access right to this object.")
        
    def create_object(self, name, owners : List['Subject'] = []):
        obj = Object(name)
        for owner in owners:
            self._add_capability(owner, obj, [Right.OWN])
        return obj
