from capability_mac import Subject, Right, CapabilityPermissionError, AccessPermissionError

if __name__ == "__main__":
    alice = Subject("Alice")
    bob = Subject("Bob")
    charlie = Subject("Charlie")
    file1 = alice.create_object("file1", [alice])
    alice.add_capability(bob, file1, [Right.READ, Right.WRITE])

    print("\nTest Single Owner Modification:")
    try:
        bob.add_capability(charlie, file1, [Right.READ])
        print("FAIL: Bob should not be able to grant access to Charlie")
    except CapabilityPermissionError:
        print("PASS: Bob cannot grant access to Charlie")

    # Test Multiple Ownership
    print("\nTest Multiple Ownership:")
    file2 = alice.create_object("file2", [alice, bob])
    alice.add_capability(charlie, file2, [Right.READ])
    bob.add_capability(charlie, file2, [Right.WRITE])
    print("PASS: Both Alice and Bob can grant access to Charlie")

    # Test Unauthorized Modification
    print("\nTest Unauthorized Modification:")
    dave = Subject("Dave")
    eve = Subject("Eve")
    try:
        dave.add_capability(eve, file1, [Right.READ])
        print("FAIL: Dave should not be able to grant access to Eve")
    except CapabilityPermissionError:
        print("PASS: Dave cannot grant access to Eve")

    # Test Revocation Scenario
    print("\nTest Revocation Scenario:")
    alice.remove_capability(charlie, file2)
    try:
        charlie.check_access(file2, Right.WRITE)
        print("FAIL: Charlie should not have write access after revocation")
    except AccessPermissionError:
        print("PASS: Charlie's write access was revoked")

    # Test Ownership Removal
    print("\nTest Ownership Removal:")
    alice.remove_capability(bob, file2)
    try:
        bob.add_capability(charlie, file2, [Right.READ])
        print("FAIL: Bob should not be able to grant access after ownership removal")
    except CapabilityPermissionError:
        print("PASS: Bob cannot grant access after ownership removal") 