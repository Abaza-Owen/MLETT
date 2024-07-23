

correct_file = open('T4_MCCa.xyz', 'r')
test_file = open('T4_MCC.xyz', 'r')

c = correct_file.readlines()
t = test_file.readlines()

correct_file.close()
test_file.close()

for i in (range(len(c))):
    try:
        if c[i].strip() != t[i].strip():
            print(f"Mismatch at {i}")
    except Exception as e:
        print(e)
 
print("Done!")
