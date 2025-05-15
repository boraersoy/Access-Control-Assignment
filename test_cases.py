from lattice_mac import SecurityLabel, Subject, Object, can_read, can_write, generate_lattice, show_lattice

# Define category universe
CATEGORIES = {"ADMIN", "LECTURERS", "STUDENTS"}

# Define subject-object scenarios
cases = [
    (Subject("S1", SecurityLabel({"STUDENTS"})), Object("O1", SecurityLabel({"STUDENTS"}))),
    (Subject("S2", SecurityLabel({"STUDENTS"})), Object("O2", SecurityLabel({"STUDENTS", "LECTURERS"}))),
    (Subject("S3", SecurityLabel({"STUDENTS"})), Object("O3", SecurityLabel({"LECTURERS"}))),
    (Subject("S4", SecurityLabel(set())), Object("O4", SecurityLabel({"STUDENTS"}))),
    (Subject("S5", SecurityLabel({"STUDENTS"})), Object("O5", SecurityLabel(set()))),
]

print("\n=== Access Tests ===")
for subject, obj in cases:
    print(f"\n{subject.name} vs {obj.name}")
    print(f"  Subject Label: {subject.label}")
    print(f"  Object Label:  {obj.label}")
    print(f"  Can READ?  {'✅' if can_read(subject, obj) else '❌'}")
    print(f"  Can WRITE? {'✅' if can_write(subject, obj) else '❌'}")

# Bonus: Show Lattice
print("\n=== Lattice ===")
labels = generate_lattice(CATEGORIES)
show_lattice(labels)
