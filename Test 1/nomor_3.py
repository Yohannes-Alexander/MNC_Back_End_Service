def validate_string(string: str) -> bool:

    collection_str = {')': '(', '}': '{', ']': '[', '>': '<'}
    

    stack = []
    

    for char in string:
        if char in '<{[(':
           
            stack.append(char)
        elif char in '>}]':

            if not stack or stack[-1] != collection_str[char]:
                return False

            stack.pop()
        else:
            return False 

        
        if len(stack) >= 2:
            top1 = stack[-1]
            top2 = stack[-2]
            if (top1 in '([{<' and top2 in ')]}>'):
                return False
            
    return len(stack) == 0

test1 = "{<{[[{{[]<{{[{[]<>}]}}<>>}}]]}>}"  
test2 = "[{}<[>]"          

print(validate_string(test1))  
# print(validate_string(test2))  
