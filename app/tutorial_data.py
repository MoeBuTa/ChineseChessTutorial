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
            answer=1,
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
            answer=0,
            hint="Soldiers can move left, right and front, but not move down."
        )

    ]
    db.session.add_all(tutorials)
    db.session.commit()
