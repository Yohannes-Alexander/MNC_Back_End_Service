def matching_string(set_string):
    collection_str = []
    for index, string in enumerate(set_string):
        for index_comp, string_comp in enumerate(set_string[index+1::]):
            if (string.lower()==string_comp.lower()):
                collection_str.append(index+1)
                print(string_comp)
                collection_str.append(index_comp+index+2)
        if(len(collection_str)!=0): return set(collection_str)
    return False

if __name__ == "__main__":
    input_total_string = int(input())
    set_string = []
    for total in range(0, input_total_string):
        set_string.append(input())
    col = matching_string(set_string)
    print(f"Contoh output: {col}")