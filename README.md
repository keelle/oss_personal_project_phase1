# 오픈소스 소프트웨어 실습 personal project phase1

# 참고 사이트
1) https://github.com/pygame/pygame "pygame"
2) https://github.com/mustafa-mun/canyon-defenders

# 타워디펜스
- 타워 디펜스 게임은 몰려오는 적들을 타워를 설치하여 막는 게임이다.
## 게임 설명
### 게임 플레이 방법
- 타워를 마우스로 끌어와서 맵에 배치하면된다.
- 타워를 클릭하여 업그레이드 할 수도 있고 원래있던 타워자리에 새로운 타워를 배치할 수도 있다.
- 타워를 적절히 사용하여 모든 좀비들을 막아내면 된다.
- 15웨이브를 버티면 승리한다.

## 게임 세부내용 설명
### 타워
- 게임에 6종류의 타워가 있다.
- 각각의 타워는 공격력, 공격범위 같은 것이 다르며 비쌀수록 능력치가 더 좋다.
- 타워를 놓으면 그 타워가 어디까지 공격 가능한지 알수 있다.
- 타워를 업그레이드 하면 성능을 올릴 수 있다.

### 게임 스탯

- `Health:` 남은 목숨을 나타내며 좀비 하나가 통과할 때 마다 체력이 1 감소한다
- `Money:` 타워 건설에 필요한 돈이다.
- `Wave Number:` 지금 몇번째 웨이브인지 보여준다

## 점수판
- 게임이 끝나면 자신의 이름을 입력할 수 있다.
- Score 버튼을 통해 자신이 몇 등인지 확인할 수 있다.

## 게임실행방법

Clone the project

```bash
  git clone https://github.com/keelle/oss_personal_project_phase1
```

Go to the project directory

```bash
  cd canyon-defenders
```

Install PyGame

```bash
  python3 -m pip install -U pygame --user
```

Start game

```bash
  python3 game.py
```
## 실행 예시
![게임영상](https://github.com/keelle/oss_personal_project_phase1/assets/82808745/bb920f2a-a46e-40b1-accf-b001bd57e657)

## 코드 설명
- game.py: window 클래스를 이용하여 게임 창 설정 및 초기화를 한다. play함수를 통해서 게임 상태를 관리하고 menu함수로는 게임 초기 화면을 관리한다. 또한, enemy, tower 클래스 등을 이용하여 게임 속 요소들을 표현한다.
- playground.py: 게임 윈도우 설정, 배경 및 플레이어 설정, 적 생성 및 게임 종료를 담당한다.
- __init__.py
- button.py: 버튼이 클릭 가능하도록 관리한다.
- enemy.py: 적과 웨이브를 관리한다.
- player.py: 플레이어의 초기상태를 설정하고 화면에 나타낸다.
- tower.py: 투사체를 초기화하고 투사체의 움직임을 업데이트한다.
- window.py: 타워 배치 및 구매 관리를 담당하며 타워 가격, 공격속도 등의 타워 정보를 저장한다.
