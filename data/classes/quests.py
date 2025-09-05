quest1_stage = 1  # 1 — дали, 2 — выполнен

def get_quest1_text_guardian():
    if quest1_stage == 1:
        return [
            "Стой!!",
            "Проход закрыт по приказу управляющего деревни!",
            "Я смогу пропустить тебя только когда позволит управляющий"
        ]
    elif quest1_stage == 2:
        return [
            "Управляющий дал добро, теперь я могу тебя пропустить"
        ]
    else:
        return ["..."]
    
def get_quest1_text_questwall():
    if quest1_stage == 1:
        return [
            "Доска обьявлений, есть 1 сообщений!",
            "Пропала фамильная реликвия управляющего!",
            "Нужен тот, кто сможет её вернуть"
        ]
    elif quest1_stage == 2:
        return [
            "Доска обьявлений пуста()"
        ]
    else:
        return ["..."]
    
def get_quest1_text_vilager1():
    if quest1_stage == 1:
        return [
            "Говорят у управляещего похитили чтото ценное",
            "И утащили в пещеру за лесом"
        ]
    elif quest1_stage == 2:
        return [
            "Как я рад что всё разрешилось и теперь у нас мир в деревне"
        ]
    else:
        return ["..."]

def get_quest1_text():
    if quest1_stage == 1:
        return [
            "Эти твари лесные украли моё сокрвище!!!!",
            "Ни один человек не пройдет через восточный пост, пока ко мне не вернется моё золотце!!"
        ]
    elif quest1_stage == 2:
        return [
            "Спасибо тебе добрый человек!!!!",
            "В знак благодарности я даю тебе много много денег!",
            "Теперь ты можешь идти куда хотел"
        ]
    else:
        return ["..."]

def update_quest1_stage(new_stage):
    global quest1_stage
    if new_stage > quest1_stage:
        quest1_stage = new_stage