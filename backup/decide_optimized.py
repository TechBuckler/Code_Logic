def decide(cpu, is_question, is_command):
    
    if is_command:
        return 3
    
    if is_question and cpu < 95:
        return 2
    
    if is_question:
        return 1
    
    if not (is_question):
        return 0
    