from app import db
from app.models import Tutorial, Question, QuestionAnswer


def add_tutorial_data():
    tutorials = [
        Tutorial(
            tutorial_num=1,
            title="Brief Information",
            subtitle="Arrangement",
            main_content="The board is composed of 9 vertical lines (files) and 10 horizontal lines (ranks) "
                         "with the pieces being played on the intersections. On each side of the board against the "
                         "back edge is a palace, which is 3 by 3 lines (9 positions) with four diagonal lines that "
                         "extend outward from the center forming an “X” shape. Dividing the two opposing sides of the "
                         "board is a river, located between the fifth and sixth ranks. The river is often marked with "
                         "the Chinese characters, 楚河 “Chǔ Hé” meaning \"Chu River\", and 漢界 (汉界 in simplified "
                         "Chinese), “Hàn Jiè”, meaning \"Han border\", a reference to the Chu-Han War. Some boards "
                         "have the starting points of soldiers marked with small crosses.",
            extra_content="The starting positions of the pieces are arranged as shown below.",
            img_url="../static/chess-img/chess-qipan.img.gif",
            question_title="There are totally 32 pieces.",
            answer=0,
            hint="hint=One side are 16 pieces, and totally 32 pieces"
        ),
        Tutorial(
            tutorial_num=2,
            title="Pieces",
            subtitle="Soldier “Bīng” 兵 and “Zú” 卒",
            main_content="The playing pieces are indicated by Chinese characters. The same ranking pieces sometimes "
                         "have different characters for each side and sometimes are written in either traditional or "
                         "Chinese characters. The pieces are identified below by English name, Chinese pronunciation, "
                         "traditional Chinese character, simplified Chinese character if it is different, "
                         "and then the character variation.",
            extra_content="Soldiers move and capture by advancing one point forward. Once a pawn has crossed the "
                          "river it may also move and capture one point horizontally. A pawn may never move backward, "
                          "thus retreating.",
            img_url="../static/chess-img/chess-bing.gif",
            question_title="Soldiers can move down.",
            answer=1,
            hint="Soldiers can move left, right and front, but not move down."
        ),
        Tutorial(
            tutorial_num=3,
            title="Pieces",
            subtitle="Cannons “Pào” 炮 and “Pào” 砲",
            main_content="Cannons move exactly like the chariot. To capture, however, a cannon must jump over exactly "
                         "one piece, friend or foe, along its line of movement.",
            extra_content="",
            img_url="../static/chess-img/chess-pao.gif",
            question_title="A cannon must jump over exactly two pieces, friends or foes, along its line of movement.",
            answer=1,
            hint="A cannon must jump over exactly one piece, friend or foe, along its line of movement."
        ),
        Tutorial(
            tutorial_num=4,
            title="Pieces",
            subtitle="Chariot “Jū” 俥/车 and “Jū” 車/车",
            main_content="Chariots move similarly to the rooks in international chess. The chariot moves as many "
                         "points as it wishes horizontally or vertically. It cannot jump over pieces in its path.",
            extra_content="",
            img_url="../static/chess-img/chess-che.gif",
            question_title="Chariots moves one point diagonally and is confined to the palace.",
            answer=1,
            hint="Chariots move similarly to the rooks in international chess. The chariot moves as many points as it "
                 "wishes horizontally or vertically. "
        ),
        Tutorial(
            tutorial_num=5,
            title="Pieces",
            subtitle="Horse “Mà” 傌/马 and “Mǎ” 馬/马",
            main_content="The horse moves one point horizontally or vertically, and then one point diagonally. It "
                         "cannot move in a direction where there is a piece blocking it along the path of movement.",
            extra_content="",
            img_url="../static/chess-img/chess-ma.gif",
            question_title="Horses moves as many points as it wishes horizontally or vertically.",
            answer=1,
            hint="The horse moves one point horizontally or vertically, and then one point diagonally."
        ),

        Tutorial(
            tutorial_num=6,
            title="Pieces",
            subtitle="Elephant “Xiàng” 相 and “Xiàng” 象",
            main_content="The elephants move exactly two points in any diagonal direction and may not jump over "
                         "intervening pieces or cross the river.",
            extra_content="",
            img_url="../static/chess-img/chess-xiang.gif",
            question_title="Elephants can across the river.",
            answer=1,
            hint="Elephants cannot across the river."
        ),
        Tutorial(
            tutorial_num=7,
            title="Pieces",
            subtitle="Guard / Advisor “Shì” 仕 and “Shì” 士",
            main_content="These are the king’s counselors and guard the king within the palace. The guard moves one "
                         "point diagonally and is confined to the palace.",
            extra_content="",
            img_url="../static/chess-img/chess-shi.gif",
            question_title="Advisor cannot leave the palace.",
            answer=0,
            hint="Advisor can and only move within the palace."
        ),
        Tutorial(
            tutorial_num=8,
            title="Pieces",
            subtitle="General “Shuài” 帥/帅 and “Jiàng” 將/将",
            main_content="Generals may move one point either vertically or horizontally, but not diagonally and is "
                         "confined to the nine points within his palace. A general may not also move into a file, "
                         "which is occupied by the enemy general, unless there is at least one piece positioned "
                         "between the generals in the file.",
            extra_content="",
            img_url="../static/chess-img/chess-shuai.gif",
            question_title="Generals cannot leave the palace.",
            answer=0,
            hint="Generals can and only move within the palace."
        )

    ]
    db.session.add_all(tutorials)
    db.session.commit()


def addQuestion():
    question1 = Question(
        body="What is the number of pieces does a game require altogether?",
        option_one='20',
        option_two='24',
        option_three='32',
        option_four='30'
    )
    db.session.add(question1)
    db.session.flush()
    answer1 = QuestionAnswer(question_id=question1.id, answer='32', score=20.00)
    db.session.add(answer1)
    # db.session.commit()

    question2 = Question(
        body="How many types of pieces does Xiangqi have?",
        option_one='5',
        option_two='6',
        option_three='7',
        option_four='8'
    )
    db.session.add(question2)
    db.session.flush()
    answer2 = QuestionAnswer(question_id=question2.id, answer='7', score=20.00)
    db.session.add(answer2)
    # db.session.commit()

    question3 = Question(
        body="How big is the board of Xiangqi?",
        option_one='8 by 9',
        option_two='8 by 8',
        option_three='9 by 9',
        option_four='9 by 10'
    )
    db.session.add(question3)
    db.session.flush()
    answer3 = QuestionAnswer(question_id=question3.id, answer='9 by 10', score=20.00)
    db.session.add(answer3)
    # db.session.commit()

    question4 = Question(
        body=" How many spots/spaces does the palace/fortress have?",
        option_one='4',
        option_two='6',
        option_three='8',
        option_four='9'
    )
    db.session.add(question4)
    db.session.flush()
    answer4 = QuestionAnswer(question_id=question4.id, answer='9', score=20.00)
    db.session.add(answer4)
    # db.session.commit()

    question5 = Question(
        body="What type of piece has the most pieces on the board?",
        option_one='Cannon',
        option_two='Soldier',
        option_three='Chariot',
        option_four='Horse'
    )
    db.session.add(question5)
    db.session.flush()
    answer5 = QuestionAnswer(question_id=question5.id, answer='Soldier', score=20.00)
    db.session.add(answer5)
    # db.session.commit()

    question6 = Question(
        body="What piece cannot cross the river?",
        option_one='Horse',
        option_two='Elephant',
        option_three='Chariot',
        option_four='Soldier'
    )
    db.session.add(question6)
    db.session.flush()
    answer6 = QuestionAnswer(question_id=question6.id, answer='Elephant', score=20.00)
    db.session.add(answer6)
    # db.session.commit()

    question7 = Question(
        body="Which piece moves in directions that are different from the other three?",
        option_one='Counselor',
        option_two='General',
        option_three='Chariot',
        option_four='Cannon'
    )
    db.session.add(question7)
    db.session.flush()
    answer7 = QuestionAnswer(question_id=question7.id, answer='Counselor', score=20.00)
    db.session.add(answer7)
    # db.session.commit()

    question8 = Question(
        body="Which piece captures differently from the other three?",
        option_one='Chariot',
        option_two='Cannon',
        option_three='Soldier',
        option_four='Horse'
    )
    db.session.add(question8)
    db.session.flush()
    answer8 = QuestionAnswer(question_id=question8.id, answer='Cannon', score=20.00)
    db.session.add(answer8)
    # db.session.commit()

    question9 = Question(
        body="Which piece cannot leave the palace?",
        option_one='Chariot',
        option_two='Soldier',
        option_three='General',
        option_four='Horse'
    )
    db.session.add(question9)
    db.session.flush()
    answer9 = QuestionAnswer(question_id=question9.id, answer='General', score=20.00)
    db.session.add(answer9)
    db.session.commit()
