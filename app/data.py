from app import db
from app.models import Tutorial


def add_tutorial_data():
    tutorials = [
        Tutorial(
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
