from extract_activities import extract_json, main

if __name__ == '__main__':
    main('activities.json')

control = extract_json('example/activities_extracted.json')
test = extract_json('activities_extract.json')
data_in = extract_json("activities.json")

if control == test:
    print('TEST PASSED')

if len(control) != len(test):
    print('INEQUAL LENGTH')

errors = 0
for index in range(len(control)):
    if control[index] != test[index]:
        errors += 1
        print('\n'*3+'='*30+'\n')
        print(data_in[index])
        print('='*30+'\n')
        print(control[index])
        print('='*30+'\n')
        print(test[index])
        print("=" * 30 + "\ndiff on line %d"%(index + 1))
        if control[index].keys() != test[index].keys():
            print("key diff")
            print(control[index].keys())
            print(test[index].keys())
        for key, value in control[index].items():
            if value != control[index][key]:
                print("item diff")
                print(value)
                print(control[index][key])

print(errors)